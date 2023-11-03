import sys

from hexplorer.tui import HexApp

if __name__ == "__main__":
    from hexplorer.tui.widgets.api_explorer import get_api_route_endpoints
    from hexplorer import LolApiDispatch

    #for api, routes in LolApiDispatch('').__dict__.items():
        #for i in get_api_route_endpoints(routes):
            #print(i.returntype)
    hexapp = HexApp()
    print(hexapp.run())
    sys.exit(hexapp.return_code or 0)
