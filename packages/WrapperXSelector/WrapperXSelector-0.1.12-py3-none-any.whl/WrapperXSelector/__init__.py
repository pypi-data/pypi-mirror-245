# WrapperXSelector/__init__.py

# Import the function from the module where it is defined
from .WrapperXSelector import generateWrapper

# Optionally, you can import other functions or modules to expose
# from .another_module import some_function

# If you want to make the function available directly when the package is imported
__all__ = ['generateWrapper']