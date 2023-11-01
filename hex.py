import sys

from hexplorer.tui import HexApp

if __name__ == "__main__":
    hexapp = HexApp()
    print(hexapp.run())
    sys.exit(hexapp.return_code or 0)
