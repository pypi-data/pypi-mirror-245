from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction


def get_tools() -> list[tuple[str,Callable]]:
    tools = import_module('tools')
    return [ (n,tool) 
            for n,tool in getmembers(tools) 
            if isfunction(tool)]
    
class Foo(object):
    
    commands = tuple(n for n,_ in get_tools()) 

for name,tool in get_tools():
    setattr(Foo,name,tool) 
        
if __name__ == '__main__':
    Interpreter.call(Foo)
        