import inspect
import ImpedanceUtils

# Get all functions in the module
functions_list = inspect.getmembers(ImpedanceUtils, inspect.isfunction)

# Print function names
for func_name, func in functions_list:
    print(func_name)