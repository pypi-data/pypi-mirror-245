import sys
from functools import wraps
from typing import Callable, Any

def private(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        caller: str = sys._getframe(1).f_code.co_name
        if args:
            caller: str = sys._getframe(1).f_code.co_name
            if not hasattr(args[0], caller) and caller != method.__name__:
                raise PermissionError(f"Cannot invoke private method \"{method.__name__}\" from scope {caller}")
        else:
            caller_module = sys.modules[sys._getframe(1).f_globals["__name__"]]
            caller: str = sys._getframe(1).f_code.co_name
            if not hasattr(caller_module, caller):
                raise PermissionError(f"Cannot invoke private function \"{method.__name__}\" from module {caller}")
        return method(*args, **kwargs)
    return wrapper