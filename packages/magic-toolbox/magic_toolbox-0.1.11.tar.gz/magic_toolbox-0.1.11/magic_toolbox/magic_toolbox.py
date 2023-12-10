from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction
from pathlib import Path
from InquirerPy.inquirer import text
from magic_cmd.run_cmd import run_cmd

def get_tools() -> list[tuple[str,Callable]]:
    tools = import_module('tools')
    return [ (n,tool) 
            for n,tool in getmembers(tools) 
            if isfunction(tool)]

project_help = ('The name of project/cmd','positional') 
cmd_help = ('The subcommand','positional') 
args_help = ('The args and kw args of the subcomand','positional') 
class MagicToolBox(object):
    
    """
    A CLI framework

    Raises:
        plac.Interpreter.Exit: [signals to exit interactive interpreter]
    """
    
 
    
    commands = (
                'create_project',
                'init',
                'add_function',
                'create_test',
            ) 
    
    def create_project(self,name:('The name of project','positional')):
        '''
        Creates a plac cli project.
        '''
        project= Path(name)
        if name:
            if project.exists():
                raise Exception(f'{name} already exists!')
            project.mkdir()
        tools = project/'tools.py'
        if tools.exists():
            raise Exception(f'{name} already exists!')
        tools.write_text(f"""def {name}(self,):
        '''
        This is just a dummy sub command to use as an example.
        You can use this as help message.
        '''
        """)
        cli:Path = project / f'{name}.py'
        class_name = name.capitalize()
        cli.write_text(f"""from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction


def get_tools() -> list[tuple[str,Callable]]:
    tools = import_module('tools')
    return [ (n,tool) 
            for n,tool in getmembers(tools) 
            if isfunction(tool)]
    
class {class_name}(object):
    
    commands = tuple(n for n,_ in get_tools()) 

for name,tool in get_tools():
    setattr({class_name},name,tool) 
        
if __name__ == '__main__':
    Interpreter.call({class_name})
        """)
        print(f'Created {name}/{name}.py and {name}/tools.py')
        
    def add_function(self,name:('The name of function','positional')):
        '''
        This creates a new function in toolbox.tools
        '''
        tools = Path('tools.py')
        if not tools.exists():
            raise Exception('No toolbox.tools run magic_toolbox init')
        new_function:str=f"""def {name}(self):
    '''
    Put your doc string here
    '''
        """
        tool_box = tools.read_text()
        tool_box = '\n'.join([tool_box,'',new_function])
        tools.write_text(tool_box)
        print('added:\n',new_function)


    def init(self):
        '''
        Add tool.toolbox to this directory.
        '''
        tools:Path = Path('tools.py')
        if tools.exists():
            raise Exception('tools.py already exists')
        self.create_project(self, '') 

    def create_test(self,
                    project:project_help,
                    cmd:cmd_help,
                    *args:args_help,
                    ):
        '''
        Creates test for CLI. The test cmd will be ran, and the
        user will either accept or reject output. If accepted,
        The output will be inserted into a string of python test and 
        written to python test file. 
        '''
        if not Path(f'{project}.py').exists():
            raise Exception(f'{project}.py does not exsit maybe run init')
        help_out = set(run_cmd(f'python {project}.py -h',True)[-1].split('  '))
        if cmd not in help_out:
            raise Exception(f'{cmd} has not been added maybe run add_function {cmd}')
            
        args = ' '.join(args)
        cmd = f'python {project}.py {cmd} {args}'
        print(cmd)

def main():
    Interpreter.call(MagicToolBox)
        
if __name__ == '__main__':
    main()