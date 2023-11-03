from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Button

from hexplorer import LolApiDispatch
from hexplorer.tui.widgets import ApiDispatchExplorer, ApiExplorer


class HexApp(App[str]):
    CSS_PATH = "hex.tcss"

    def __init__(self):
        super().__init__()
        self.explorer = None


    def compose(self) -> ComposeResult:
        yield Header()
        self.explorer = ApiExplorer(LolApiDispatch('').clash, debug=True)
        yield self.explorer
        yield Button("quit", id="quit", variant="error")

    #def on_event(self, event: events.ShutdownRequest) -> None:
        ...
        #self.exit(self.explorer.get_request())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(self.explorer.get_request())

