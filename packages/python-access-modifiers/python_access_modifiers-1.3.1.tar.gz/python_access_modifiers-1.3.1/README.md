![Version]
![SupportedVersions]
![License]

[Version]: https://img.shields.io/pypi/v/python-access-modifiers
[SupportedVersions]: https://img.shields.io/badge/python-3.12-orange
[License]: https://img.shields.io/badge/license-MIT-yellow

# Installation
Built and tested on Python 3.12.<br>
No requirements other than the module itself.
```
pip install python-access-modifiers
```
# Introduction
`python-access-modifiers` is a lightweight Python package designed to enhance access control of methods within classes and modules.

### Decorators
`@private` - Defines a method as private, controlling the accessibility of the method based on the calling context. Private methods can only be invoked from inside of the same scope as the defining method.<br>
`@protected` - Defines a method as protected, allowing the method to be invoked from the defining class and any classes that inherit from it.<br>
`@constant` - Defines a method as constant, removing the ability for the method to be overriden. Note that this decorator can only be used within a class.<br>
`@field_access_modifiers` - Allows a class to modify the accessibility of fields, defining them as public or protected.

# Example Usage
### Creating a private method inside of a class
```py
from python_access_modifiers import private

class MyClass():
    @private
    def my_private_method(self) -> None:
        print("This is a private method")

    def my_public_method(self) -> None:
        print("This is a public method")
        self.my_private_method()

my_class = MyClass()
my_class.my_public_method()
```
### Output
No exception is raised because `my_private_method` is called from within `MyClass`, not from outside of the accessible scope.
```
This is a public method
This is a private method
```
### Calling a private method outside of the accessible scope
```py
from python_access_modifiers import private

class MyClass():
    @private
    def my_private_method(self) -> None:
        print("This is a private method")

    def my_public_method(self) -> None:
        print("This is a public method")
        self.my_private_method()

my_class = MyClass()
my_class.my_private_method()
```
### Output
```
RuntimeError: Cannot invoke private method "MyClass.my_private_method" from within the scope of "__main__"
```
### Creating classes that inherit private methods
```py
from python_access_modifiers import private

class Base():
    @private
    def my_private_method(self) -> None:
        print("This is a private method")

    def my_public_method(self) -> None:
        print("This is a public method")
        self.my_private_method()

class Child(Base):
    ...

child = Child()
child.my_public_method()
```
### Output
`my_private_method` is called from within the `Base` class, therefore no exception is raised.
```
This is a public method
This is a private method
```
However, if `my_private_method` was called directly from outside of the accessible scope of the `Base` class, a `RuntimeError` would be raised.
```py
child = Child()
child.my_private_method()
```
### Output
```
RuntimeError: Cannot invoke private method "Base.my_private_method" from within the scope of "__main__"
```
### Creating a private method from inside of a module
`my_module.py`
```py
from python_access_modifiers import private

@private
def my_private_method() -> None:
    print("This method is private to my_module")
```
`main.py`
```py
from my_module import my_private_method

my_private_method()
```
### Output
```
RuntimeError: Cannot invoke private method "my_module.my_private_method" from module "__main__"
```
# Creating a protected method
```py
from python_access_modifiers import protected

class MyBaseClass():
    @protected
    def my_protected_method(self) -> None:
        print("This method is protected inside of MyBaseClass")

    def call_protected_method(self) -> None:
        self.my_protected_method()

class MySubClass(MyBaseClass):
    def call_protected_method_from_subclass(self) -> None:
        self.my_protected_method()
        
subclass = MySubClass()

subclass.call_protected_method()
subclass.call_protected_method_from_subclass()
```
### Output
If `my_protected_method` is called from within `MyBaseClass` or from within one of it's subclasses (i.e: `MySubClass`), the method gets called normally.
```
This method is protected inside of MyBaseClass
This method is protected inside of MyBaseClass
```
However, if `my_protected_method` is called from outside of the accessible scope of the base class and it's subclasses, an exception will be raised.
```py
subclass.my_protected_method()
```
### Output
```
RuntimeError: Cannot invoke protected method "MyBaseClass.my_protected_method" from within the scope of "__main__"
```
# Creating a constant method
Constant methods can only be created from inside of a class
```py
from python_access_modifiers import constant

class MyClass():
    @constant
    def my_constant_method(self) -> None:
        print("This method is constant")

my_class = MyClass()
my_class.my_constant_method()
```
### Output
```
This method is constant
```
### Attempting to modify a constant method
```py
def modified_method(self) -> None:
    print("This method has been modified")

my_class.my_constant_method = modified_method
```
### Output
```
RuntimeError: "my_constant_method" is constant and cannot be overriden
```
# Modifying the accessibility of fields
The accessibility of fields can only be modified from within classes. Currently, you can only create `Protected` fields. Fields are public by default.
### Creating a protected field
```py
from python_access_modifiers import field_access_modifiers, Protected

@field_access_modifiers
class MyClass():
    protected_field: Protected[int]
    
    def __init__(self, value: int) -> None:
        self.protected_field: int = value

    def show_protected_value(self) -> None:
        print(self.protected_field)

my_class = MyClass(7)
my_class.show_protected_value()
```
### Output
```
7
```
Field access modifiers can be used with or without a type generic.
```py
>>> field: Protected
>>> bool_field: Protected[bool]
>>> int_or_float_field: Protected[int | float]
```
### Attempting to access a protected field
```py
print(my_class.protected_field)
```
### Output
```
RuntimeError: Cannot access protected field "MyClass.protected_field" from within "<module>"
```