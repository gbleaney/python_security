class SomeClass:
    def __reduce__(self):
        return (function_to_call, (args, to, provide))

def function_to_call():
    pass

new_object = function_to_call(args, to, provide)


import importlib

def remote_procedure_call(fully_qualified_function: str, argument: str):
    module_name, _, function_name = fully_qualified_function.rpartition(".")
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    function(argument)

remote_procedure_call("builtins.eval", "print('It works')")


{'__builtins__':{}}

eval()
