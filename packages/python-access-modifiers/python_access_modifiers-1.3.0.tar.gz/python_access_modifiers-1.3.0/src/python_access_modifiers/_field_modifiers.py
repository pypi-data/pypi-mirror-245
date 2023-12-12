import sys
from typing import TypeVar, Generic, Type, List, Any, get_type_hints
from types import FrameType, CodeType
from ._private_modifier import private

T_Protected = TypeVar("T_Protected")

class Protected(Generic[T_Protected]):
    def __init__(self, items: List[T_Protected]) -> None:
        self.items: List[T_Protected] = items

    @staticmethod
    def _is_protected(type_: Type) -> bool:
        return (hasattr(type_, "__origin__") and getattr(type_, "__origin__") is Protected) or type_ is Protected
    
def field_access_modifiers(cls):
    scope: str | None = sys._getframe(1).f_locals.get("__qualname__")

    class FieldAccessModifiersWrapper(cls):
        def __init__(self, *args, **kwargs):
            self.__protected_fields: set[str] = set()
            super().__init__(*args, **kwargs)

            for field, field_type in get_type_hints(cls).items():
                if Protected._is_protected(field_type):
                    self.__protect(field)

        @private
        def __protect(self, __name: str) -> None:
            if hasattr(self, __name):
                __is_callable: str = f"Cannot make \"{__name}\" protected. It is callable and should be made protected using the @protected decorator"
                assert not callable(object.__getattribute__(self, __name)), __is_callable
            __already_protected: str = f"{__name} is already a protected field"
            assert __name not in self.__protected_fields, __already_protected
            self.__protected_fields.add(__name)

        def __getattribute__(self, __name: str) -> Any:
            cls_name: str = FieldAccessModifiersWrapper.__name__
            if __name in object.__getattribute__(self, f"_{cls_name}__protected_fields"):
                __is_callable: str = f"Cannot make \"{__name}\" protected. It is callable and should be made protected using the @protected decorator"
                assert not callable(object.__getattribute__(self, __name)), __is_callable
                frame: FrameType = sys._getframe(1)
                frame_code: CodeType = frame.f_code
                caller_name: str = frame_code.co_name
                caller_class: str = frame.f_locals.get("self")

                if not isinstance(caller_class, cls):
                    field: str = f"{cls.__name__}.{__name}"
                    caller_scope: str = f"{caller_class.__class__.__name__}.{caller_name}"

                    if scope is not None:
                        field = f"{scope}.{cls.__name__}.{__name}"
                        caller_scope = caller_name
                        if caller_class is not None:
                            caller_scope = f"{caller_class.__class__.__name__}." + caller_scope
                    elif caller_class is None:
                        field = f"{cls.__name__}.{__name}"
                        caller_scope = caller_name

                    __cannot_access: str = f"Cannot access protected field \"{field}\" from within \"{caller_scope}\""
                    raise RuntimeError(__cannot_access)

            return object.__getattribute__(self, __name)
    
    cls_type: cls = FieldAccessModifiersWrapper
    return cls_type