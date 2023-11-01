from textual.app import App, ComposeResult
from textual.events import Key
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Label, Header, Input


class Name(Widget):
    """Generates a greeting."""

    who = reactive("name")

    def render(self) -> str:
        return f"Hello, {self.who}!"

class HexApp(App[str]):
    CSS_PATH = "hex.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter your name")
        yield Name()
        yield Label("Do you love Textual?", id="question")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")



    def on_key(self, event: Key):
        self.title = event.key
        self.sub_title = f"You just pressed {event.key}!"

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Name).who = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        name = self.query_one(Name).who
        self.exit(result=f"{event.button.id} {name}", return_code=1, message="I'm out")
