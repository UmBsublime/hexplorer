from collections.abc import Callable
from enum import Enum
from functools import partial
from pydantic import BaseModel
from timeit import default_timer
from typing import get_type_hints, Any, Optional, Type

from rich.markup import escape
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import var
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import Tree, Label, Input, RadioButton, RadioSet, RichLog, Footer, TabbedContent, TabPane
from textual.widgets._tree import TreeNode

from hexplorer.api.exceptions import ApiResourceNotFoundError, ApiBadRequestError, ApiUnauthorizedError
from hexplorer.api.riot import RiotApi
from hexplorer import LolApiDispatch, RiotApiDispatch


class ApiExplorerScreen(Screen):
    BINDINGS = [
        ("c", "clear_log", "Clear Log"),
        ("d", "toggle_debug", "Toggle Debug"),
        ("e", "execute_request", "Execute Request"),
        ("t", "toggle_tree", "Toggle Expand"),
    ]

    def __init__(self, api_dispatch: LolApiDispatch|RiotApiDispatch) -> None:
        super().__init__()
        self.api_dispatch = api_dispatch
        self.border_title = str(api_dispatch.__class__.__name__)

    def compose(self):

        with TabbedContent():
            for i in self.api_dispatch.__dict__.values():
                with TabPane(i.__class__.__name__):
                    yield ApiExplorer(i)

        yield RichLog(id="api-explorer-log")
        yield Footer()

    def action_clear_log(self) -> None:
        self.app.query_one("#api-explorer-log", RichLog).clear()

    def action_toggle_tree(self) -> None:
        for tree in self.query(Tree):
            tree.root.toggle_all()

    def action_toggle_debug(self) -> None:
        """Called in response to key binding."""
        for explorer in self.query(ApiExplorer):
            explorer.show_debug = not explorer.show_debug

class ApiExplorer(Widget):
    show_debug = var(False)

    BINDINGS = [
        ("e", "execute_request", "Execute Request"),
    ]

    def __init__(self, api: RiotApi) -> None:
        super().__init__()
        self.api = api
        self.api_tree = self.gen_api_tree()
        self.border_title = str(api.__class__.__name__)

    def compose(self) -> str:
        with Vertical(id="explorer-debug", ) as vertical:
            vertical.border_title = 'debug'
            yield Label(f"{self.api_tree.name}: {self.api.__class__.__name__}", id="api")
            yield Label(" ", id="endpoint-log")
            yield Label(" ", id="endpoint-data")
        yield self.api_tree
        # yield RichLog()

    @on(Tree.NodeHighlighted)
    def show_route(self, event: Tree.NodeHighlighted):
        if event.node.children:
            self.query_one('#endpoint-log', Label).update(
                f"{event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}"
            )
            self.query_one('#endpoint-data', Label).update(' ')

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
                if not new_value:
                    return
                new_label = event.node.label.split(':')[0] + f' = {new_value}'
                if '=' in event.node.label:
                    new_label = event.node.label.split('=')[0]
                    new_label.rstrip()
                    new_label += f' = {new_value}'
                event.node.label = new_label
                event.node.data['value'] = new_value
            self.app.push_screen(ApiParamPicker(event.node.data), set_value)

    def watch_show_debug(self, show_debug: bool) -> None:
        """Called when show_debug is modified."""
        self.set_class(show_debug, "-show-debug")

    @work(exclusive=True, thread=True)
    async def action_execute_request(self):
        if request := self.get_request():
            start = default_timer()
            self.api_tree.loading = True
            try:
                self.app.query_one("#api-explorer-log", RichLog).write(request())
            except (ApiResourceNotFoundError, ApiUnauthorizedError, ApiBadRequestError) as e:
                self.app.query_one("#api-explorer-log", RichLog).write(
                    Text.from_markup(
                        e.args[0].replace('>',']').replace('<', '[')
                    )
                )
            self.api_tree.loading = False

    def get_request(self) -> Optional[Callable]:
        node = self.api_tree.get_node_at_line(self.api_tree.cursor_line)

        request_node: TreeNode = node
        if not node.children:
            request_node = node.parent

        for param in request_node.children:
            if not param.data['value']:
                self.app.query_one("#api-explorer-log", RichLog).write("\nMissing parameters\n")
                return None

        request = partial(request_node.data.method, *[p.data['value'] for p in request_node.children])
        self.app.query_one("#api-explorer-log", RichLog).write(request)
        return request

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
            with RadioSet()as rs:
                for choice in self.param['type']:
                    rb = RadioButton(choice.value)
                    if choice == self.param['value']:
                        rb.styles.color = "green 50%"
                    yield rb

    @on(RadioSet.Changed)
    def return_enum(self, event: RadioSet.Changed):
        self.dismiss(getattr(self.param['type'], str(event.pressed.label)))

    @on(Input.Submitted)
    def return_input(self, event: Input.Submitted):
        self.dismiss(event.value)

    def key_escape(self):
        self.dismiss(None)


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


class ApiRequestField(BaseModel):
    type: Type
    value: Optional[Any]


class ApiRequest(BaseModel):
    name: str
    method: Callable
    arguments: dict
    returntype: Any