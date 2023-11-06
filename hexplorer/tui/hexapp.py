from textual.app import App

from hexplorer import LolApiDispatch
from hexplorer.tui.widgets import ApiExplorerScreen


class HexApp(App[str]):
    CSS_PATH = "hex.tcss"
    ENABLE_COMMAND_PALETTE = True
    COMMANDS = App.COMMANDS | ApiExplorerScreen.COMMANDS

    def __init__(self):
        super().__init__()
        self.explorer = None

    def on_mount(self):
        self.explorer = ApiExplorerScreen(
            LolApiDispatch('')
        )

        self.push_screen(self.explorer)

    # def on_exit_app(self, event: Button.Pressed) -> None:
    #     self.exit(self.explorer.get_request())

