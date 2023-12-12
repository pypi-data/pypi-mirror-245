from typing import Callable, Type, Any

class Constant():
    def __init__(self, method: Callable) -> None:
        self.method: Callable = method

    def __get__(self, instance: object, owner: Type) -> Callable:
        return self.method.__get__(instance, owner)

    def __set__(self, instance: object, value: Any) -> None:
        __cannot_override: str = f"\"{self.method.__name__}\" is constant and cannot be overriden"
        raise RuntimeError(__cannot_override)
    
    def __call__(self, *args, **kwargs) -> None:
        __cannot_call: str = f"\"{self.method.__name__}\" is constant and can only be called from within an instance"
        raise RuntimeError(__cannot_call)

def constant(method: Callable) -> Constant:
    return Constant(method)