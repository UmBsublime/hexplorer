import sys

from loguru import logger
from rich import print

from hexplorer.tui import HexApp

if __name__ == "__main__":

    logger.remove()
    hexapp = HexApp()
    request = hexapp.run()
    print(request)
    #if request:
    #    print(request())
    sys.exit(hexapp.return_code or 0)
