from enum import Enum
from typing import get_type_hints, Callable, Any

from pydantic import BaseModel
from rich.markup import escape
from textual import on
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Tree, Label

from hexplorer.api.riot import RiotApi


class ApiRequest(BaseModel):
    name: str
    method: Callable
    arguments: dict
    returntype: Any


class ApiExplorer(Widget):
    BINDINGS = [
        ("e", "get_request", "Get Request"),
    ]

    def __init__(self, api: RiotApi, debug: bool = False) -> None:
        super().__init__()
        self.api = api
        self.api_tree = get_api_tree(self.api)
        self.debug = debug
        self.request = None

    def compose(self) -> str:

        if self.debug:
            with Vertical(id="explorer-debug"):
                yield Label(f"{self.api_tree.name}: {self.api.__class__.__name__}", id="api")
                yield Label(" ", id="endpoint-log")
                yield Label(" ", id="endpoint-data")
        yield self.api_tree

    @on(Tree.NodeHighlighted)
    def show_route(self, event: Tree.NodeHighlighted):
        if self.debug:
            self.query_one('#endpoint-log', Label).update(
                f"{event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}"
            )
            data_label = self.query_one('#endpoint-data', Label)
            # noinspection DuplicatedCode
            if not event.node.children:
                if issubclass(event.node.data, Enum):
                    data_label.update(f"{[e.value for e in event.node.data]}")
                else:
                    data_label.update(f"{event.node.data}")
            else:
                data_label.update(f"{event.node.data.name}")

    def action_get_request(self) -> ApiRequest|None:
        node = self.api_tree.get_node_at_line(self.api_tree.cursor_line)
        if node.children:
            if self.debug:
                self.query_one('#endpoint-data', Label).update(str(node.data))
            self.request = node.data
            return self.request

    def get_request(self) -> ApiRequest|None:
        return self.request

class ApiDispatchExplorer(Widget):
    DEFAULT_CSS = """
    """

    def __init__(self, api_dispatch: object, debug: bool = False) -> None:
        super().__init__()
        self.api_dispatch = api_dispatch
        self.debug = debug

    def compose(self) -> str:
        api_tree = get_route_tree(self.api_dispatch)
        if self.debug:
            with Vertical(id="explorer-debug"):
                yield Label(f"{api_tree.name}: {self.api_dispatch.__class__.__name__}", id="api")
                yield Label(" ", id="log")
                yield Label(" ", id="data")
        yield api_tree

    @on(Tree.NodeHighlighted)
    def show_route(self, event: Tree.NodeHighlighted):
        if self.debug:
            self.query_one('#log', Label).update(
                f"{event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}"
            )
            data_label = self.query_one('#data', Label)
            if not event.node.children:
                if issubclass(event.node.data, Enum):
                    data_label.update(f"{[e.value for e in event.node.data]}")
                else:
                    data_label.update(f"{event.node.data}")
            else:
                data_label.update(f"{event.node.data}")

    @on(Tree.NodeSelected)
    def set_argument(self, event: Tree.NodeSelected):
        # Spawn modal screen to select enum ?
        ...




def get_api_tree(api) -> Tree[dict]:
    api_tree = Tree(api.__class__.__name__, name="api_tree", data=api)
    api_tree.show_root = False
    for endpoint in get_api_route_endpoints(api):
        endpoint_node = api_tree.root.add(
            f"[deep_pink4]{endpoint.name}[/deep_pink4] -> [medium_purple3]{escape(str(endpoint.returntype))}[/medium_purple3]",
            data=endpoint
        )
        for name, param in endpoint.arguments.items():
            endpoint_node.add_leaf(
                f"[cyan]{name}[/cyan]: [violet]{escape(str(param.__name__))}[/violet]",
                data=param
            )
    return api_tree

def get_route_tree(api_dispatch) -> Tree[dict]:
    api_tree = Tree(api_dispatch.__class__.__name__, name="api_tree", data=api_dispatch)
    api_tree.show_root = False
    for api, routes in api_dispatch.__dict__.items():
        route_tree = api_tree.root.add(f"[yellow]{api}[/yellow]", data=routes)
        route_tree.toggle_all()
        for endpoint in get_api_route_endpoints(routes):
            endpoint_tree = route_tree.add(
                f"[deep_pink4]{endpoint.name}[/deep_pink4] -> [medium_purple3]{escape(str(endpoint.returntype))}[/medium_purple3]",
                data=endpoint.method
            )
            for name, param in endpoint.arguments.items():
                endpoint_tree.add_leaf(
                    f"[cyan]{name}[/cyan]: [violet]{escape(str(param.__name__))}[/violet]",
                    data=param
                )
    return api_tree


def get_api_route_endpoints(api_route):
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
                #print(returntype.__dict__)
                returntype = f"{returntype.__origin__.__name__}[{returntype.__args__[0].__name__}]"

            request = ApiRequest(name=method_name, method=method, arguments=params, returntype=returntype)
            # print(returntype)
            object_methods.append(request)

    return object_methods


