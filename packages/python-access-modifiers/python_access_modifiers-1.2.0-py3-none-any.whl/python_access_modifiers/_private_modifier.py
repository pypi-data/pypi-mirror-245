import sys
from functools import wraps
from typing import Callable, Any
from types import FrameType, CodeType, ModuleType, NoneType

def private(method: Callable) -> Callable:
    scope: str | None = sys._getframe(1).f_locals.get("__qualname__")

    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        frame: FrameType = sys._getframe(1)
        frame_code: CodeType = frame.f_code
        caller_name: str = frame_code.co_name
        caller_class: str = frame.f_locals.get("self").__class__
        caller_module: ModuleType = sys.modules[frame.f_globals["__name__"]]

        if scope is None:
            base_module: str = method.__globals__["__name__"]

            if caller_module.__name__ != base_module or not hasattr(caller_module, method.__name__):
                raise RuntimeError(f"Cannot invoke private method \"{base_module}.{method.__name__}\" from module \"{caller_module.__name__}\"")
            
            return method(*args, **kwargs)
        else:
            resolution_order: list[object] = caller_class.mro()
            
            for object_ in resolution_order:
                if caller_name in dir(object_):
                    caller = getattr(object_, caller_name)
                    caller = getattr(caller, "__wrapped__") if hasattr(caller, "__wrapped__") else caller

                    if scope == object_.__qualname__ and caller.__code__ == frame_code:
                        return method(*args, **kwargs)
                    
            if caller_class is NoneType:
                raise RuntimeError(f"Cannot invoke private method \"{scope}.{method.__name__}\" from within the scope of \"{caller_module.__name__}\"")
            else:
                raise RuntimeError(f"Cannot invoke private method \"{scope}.{method.__name__}\" from within the scope of \"{caller_class.__name__}.{caller_name}\"")

    return wrapper