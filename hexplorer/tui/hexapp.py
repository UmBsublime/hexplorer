from textual import on
from textual.app import App, ComposeResult
from textual.events import Key
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Header, Input, Tree, Label

from rich.markup import escape

class Name(Widget):
    """Generates a greeting."""

    who = reactive("name")

    def render(self) -> str:
        return f"Hello, {self.who}!"


from hexplorer.tui.helper import get_api_route_endpoints
from hexplorer import LolApiDispatch


def get_route_tree(api_dispatch) -> Tree[dict]:
    api_tree = Tree(api_dispatch.__class__.__name__, name="api_tree")
    api_tree.show_root = False
    for api, routes in api_dispatch.__dict__.items():
        route_tree = api_tree.root.add(f"[yellow]{api}[/yellow]")
        route_tree.toggle_all()
        for endpoint in get_api_route_endpoints(routes):
            endpoint_tree = route_tree.add(
                f"[green]{endpoint.name}[/green] -> [violet]{escape(str(endpoint.returntype))}[/violet]"
            )
            for name, param in endpoint.arguments.items():
                endpoint_tree.add_leaf(
                    f"[cyan]{name}[/cyan]: [violet]{escape(str(param.__name__))}[/violet]"
                )

    return api_tree


class HexApp(App[str]):
    CSS_PATH = "hex.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        # yield Label(" ")
        yield get_route_tree(LolApiDispatch(''))

    #def on_key(self, event: Key):
    #    self.title = event.key
    #    self.sub_title = f"You just pressed {event.key}!"

    def on_input_changed(self, event: Input.Changed) -> None:
        # self.query_one(Name).who = event.value
        ...

    @on(Tree.NodeSelected)
    def show_route(self, event: Tree.NodeSelected):
        event.node.toggle()
        # event.node.children
        self.title = event.node.tree.name
        self.sub_title = f"{event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}"
        #self.query_one(Label).update(f"{event.node.tree.name} {event.node.parent.label}{'.' if event.node.children else ' '}{event.node.label}")



    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = self.query_one(Name).who
        # self.exit(result=f"{event.button.id} {name}", return_code=1, message="I'm out")
