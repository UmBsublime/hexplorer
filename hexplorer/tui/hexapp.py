from textual.app import App, ComposeResult
from textual.events import Key
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Header, Input, Tree


class Name(Widget):
    """Generates a greeting."""

    who = reactive("name")

    def render(self) -> str:
        return f"Hello, {self.who}!"


from hexplorer.tui.helper import get_api_route_endpoints
from hexplorer import LolApiDispatch


def get_route_tree(api_dispatch) -> Tree[dict]:
    api_tree = Tree(api_dispatch.__class__.__name__)
    #api_tree.root.toggle_all()
    api_tree.show_root = False
    for api, routes in api_dispatch.__dict__.items():
        route_tree = api_tree.root.add(f"[yellow]{api}[/yellow]")
        route_tree.toggle_all()
        for endpoint in get_api_route_endpoints(routes):
            endpoint_tree = route_tree.add(f"GET [green]{endpoint.name}[/green] -> [violet]{endpoint.returntype.__name__}[/violet]")
            for name, param in endpoint.arguments.items():
                endpoint_tree.add_leaf(f"[cyan]{name}[/cyan]: [violet]{param.__name__}[/violet]")

                # param_tree = endpoint_tree.add(f"{param['name']}: {param['type'].__name__}")
                # param_tree.add_leaf(param['type'].__name__)

    return api_tree


class HexApp(App[str]):
    CSS_PATH = "hex.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield get_route_tree(LolApiDispatch(''))

    def on_key(self, event: Key):
        self.title = event.key
        self.sub_title = f"You just pressed {event.key}!"

    def on_input_changed(self, event: Input.Changed) -> None:
        # self.query_one(Name).who = event.value
        ...

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = self.query_one(Name).who
        # self.exit(result=f"{event.button.id} {name}", return_code=1, message="I'm out")
