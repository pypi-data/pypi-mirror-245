import sys
from functools import wraps
from typing import Callable, Type, Any
from types import FrameType, CodeType, ModuleType, NoneType
from ._constant_modifier import Constant

def protected(method: Callable) -> Callable:
    scope: str | None = sys._getframe(1).f_locals.get("__qualname__")

    if scope is None:
        __no_scope_context: str = f"Cannot create protected method \"{method.__name__}\" without a scope context"
        raise RuntimeError(__no_scope_context)

    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        frame: FrameType = sys._getframe(1)
        frame_code: CodeType = frame.f_code
        caller_name: str = frame_code.co_name
        caller_func: object = frame.f_locals.get("self")
        caller_class: Type = caller_func.__class__
        caller_module: ModuleType = sys.modules[frame.f_globals["__name__"]]

        if isinstance(method, Constant):
            __wrapper_priority: str = f"@constant must have wrapper priority over @protected"
            raise RuntimeError(__wrapper_priority)

        resolution_order: list[Type] = caller_class.mro()
        
        for object_ in resolution_order:
            if caller_name in dir(object_):
                caller = getattr(object_, caller_name)
                caller = getattr(caller, "__wrapped__", caller)
                
                if scope == object_.__qualname__ and callable(caller) and hasattr(caller, "__code__"):
                    if caller.__code__ == frame_code:
                        return method(*args, **kwargs)
        
        subclass = caller_class
        subclass_method: Callable | None = None

        while subclass:
            if method.__name__ in dir(subclass):
                subclass_method = getattr(subclass, method.__name__)
                break
            subclass = subclass.__bases__[0] if subclass.__bases__ else None

        if subclass_method is not None:
            if subclass_method.__name__ == method.__name__ and isinstance(subclass_method, method.__class__):
                return method(*args, **kwargs)

        if caller_class is NoneType:
            __cannot_invoke: str = f"Cannot invoke protected method \"{scope}.{method.__name__}\" from within the scope of \"{caller_module.__name__}\""
            raise RuntimeError(__cannot_invoke)
        else:
            __cannot_invoke: str = f"Cannot invoke protected method \"{scope}.{method.__name__}\" from within the scope of \"{caller_class.__name__}.{caller_name}\""
            raise RuntimeError(__cannot_invoke)

    return wrapper