from enum import Enum
from functools import partial
from typing import get_type_hints, Callable, Any

from pydantic import BaseModel
from rich.markup import escape
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import Tree, Label, Input, RadioButton, RadioSet, Button, RichLog

from hexplorer.api.exceptions import ApiResourceNotFoundError, ApiBadRequestError
from hexplorer.api.riot import RiotApi


def get_api_route_endpoints(api_route: RiotApi):
    object_methods = []
    for method_name in dir(api_route):
        method = getattr(api_route, method_name)
        if callable(method) and not method_name.startswith('_'):
            if method_name == 'get_object':
                continue

            params = get_type_hints(method)

            returntype = params.pop('return')
            if str(returntype).startswith('<'):
                returntype = returntype.__name__
            else:
                returntype = f"{returntype.__origin__.__name__}[{returntype.__args__[0].__name__}]"

            object_methods.append(
                ApiRequest(name=method_name, method=method, arguments=params, returntype=returntype)
            )

    return object_methods


class ApiRequest(BaseModel):
    name: str
    method: Callable
    arguments: dict
    returntype: Any


class ApiExplorer(Screen):
    BINDINGS = [
        ("e", "gen_request", "Get Request"),
        ("r", "run_request", "Run Request")
    ]

    def __init__(self, api: RiotApi, debug: bool = False) -> None:
        super().__init__()
        self.api = api
        self.api_tree = self.gen_api_tree()
        self.debug = debug

    def compose(self) -> str:

        if self.debug:
            with Vertical(id="explorer-debug"):
                yield Label(f"{self.api_tree.name}: {self.api.__class__.__name__}", id="api")
                yield Label(" ", id="endpoint-log")
                yield Label(" ", id="endpoint-data")
        yield self.api_tree
        yield RichLog()
        #yield Button("quit", id="quit", variant="error")

    @on(Tree.NodeHighlighted)
    def show_route(self, event: Tree.NodeHighlighted):
        if self.debug:
            if event.node.children:
                self.query_one('#endpoint-log', Label).update(
                    f"{event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}"
                )
                self.query_one('#endpoint-data', Label).update(' ')

            # noinspection DuplicatedCode
            else:
                data_label = self.query_one('#endpoint-data', Label)
                if issubclass(event.node.data['type'], Enum):
                    data_label.update(f"{[e.value for e in event.node.data['type']]}")
                else:
                    data_label.update(f"{event.node.data['type']}")

    @on(Tree.NodeSelected)
    def select_param(self, event: Tree.NodeSelected):
        if not event.node.children:
            def set_value(new_value):
                new_label = event.node.label.split(':')[0] + f' = {new_value}'
                if '=' in event.node.label:
                    new_label = event.node.label.split('=')[0]
                    new_label.rstrip()
                    new_label += f' = {new_value}'
                event.node.label = new_label
                event.node.data['value'] = new_value
            self.app.push_screen(ApiParamPicker(event.node.data), set_value)


    def action_gen_request(self) -> callable:
        node = self.api_tree.get_node_at_line(self.api_tree.cursor_line)
        if node.children:
            for param in node.children:
                if not param.data['value']:
                    if self.debug:
                        self.query_one(RichLog).write("\nMissing parameters\n")
                    return None
            request = partial(node.data.method, *[p.data['value'] for p in node.children])
            if self.debug:
                self.query_one('#endpoint-data', Label).update(str(request))
            self.query_one(RichLog).write(request)
            return request



    @work
    async def action_run_request(self):
        if request := self.get_request():
            try:
                self.query_one(RichLog).write(request())
            except ApiResourceNotFoundError:
                self.query_one(RichLog).write("\n404 baby\n")
            except ApiBadRequestError:
                self.query_one(RichLog).write("\n400 baby\n")

    def get_request(self) -> ApiRequest | None:
        return self.action_gen_request()

    def gen_api_tree(self) -> Tree[RiotApi]:
        api_tree = Tree(self.api.__class__.__name__, name="api_tree", data=self.api)
        api_tree.show_root = False
        for endpoint in get_api_route_endpoints(self.api):
            endpoint_node = api_tree.root.add(
                f"[deep_pink4]{endpoint.name}[/deep_pink4] -> "
                f"[medium_purple3]{escape(str(endpoint.returntype))}[/medium_purple3]",
                data=endpoint
            )
            for name, param in endpoint.arguments.items():
                endpoint_node.add_leaf(
                    f"[cyan]{name}[/cyan]: [violet]{escape(str(param.__name__))}[/violet]",
                    data={'type': param, 'value': None}
                )
        return api_tree


class ApiParamPicker(ModalScreen):
    def __init__(self, param: dict) -> None:
        super().__init__()
        self.param = param

    def compose(self) -> ComposeResult:
        if issubclass(self.param['type'], int) or issubclass(self.param['type'], str):
            if self.param['value']:
                yield Input(self.param['value'], placeholder=str(self.param['type'].__name__))
            else:
                yield Input(placeholder=str(self.param['type'].__name__))
        elif issubclass(self.param['type'], Enum):
            with RadioSet():
                for choice in self.param['type']:
                    yield RadioButton(choice.value)

    @on(RadioSet.Changed)
    def return_enum(self, event: RadioSet.Changed):
        self.dismiss(getattr(self.param['type'], str(event.pressed.label)))

    @on(Input.Submitted)
    def return_input(self, event: Input.Submitted):
        self.dismiss(event.value)
