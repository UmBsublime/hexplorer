from pydantic import BaseModel
from typing import Callable, Any

from hexplorer import LolApiDispatch
from hexplorer.config import SETTINGS


class ApiRequest(BaseModel):
    name: str = None
    method: Callable = None
    arguments: dict
    returntype: Any


from typing import get_args, get_type_hints
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


for route in LolApiDispatch('').__dict__.values():
    get_api_route_endpoints(route)
