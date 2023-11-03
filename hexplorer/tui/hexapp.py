from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Button

from hexplorer import LolApiDispatch
from hexplorer.tui.widgets import ApiExplorer


class HexApp(App[str]):
    CSS_PATH = "hex.tcss"

    def __init__(self):
        super().__init__()
        self.explorer = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.explorer = ApiExplorer(
            LolApiDispatch('RGAPI-23bb8333-3946-47e5-8a60-446964e46d7e').summoner,
            debug=False
        )

        self.push_screen(self.explorer)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(self.explorer.get_request())

