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
            from inspect import signature
            s = signature(method)
            #help(s)
            print("TITI", s.return_annotation)

            params = get_type_hints(method)

            returntype = params.pop('return')

            request = ApiRequest(name=method_name, method=method, arguments=params, returntype=s.return_annotation)
            #print(repr(returntype))
            object_methods.append(request)

            #params = []
            #for param in s.parameters.values():
            #    new_s = {'name': param.name, 'type': param.annotation}
            #    params.append(new_s)
            #print("HEELO", str(s.return_annotation))
            #print(get_type_hints(method))

    return object_methods


for route in LolApiDispatch('').__dict__.values():
    get_api_route_endpoints(route)
