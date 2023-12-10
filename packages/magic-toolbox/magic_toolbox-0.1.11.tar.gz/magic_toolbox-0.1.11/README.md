# Magic Toolbox
Magic toolbox is a framework built off of plac.
When you create a new cli project toolbox creates a new floder, 
adds a tool.py file and main project.py file. 
You put new commands into the tool.py and 
the project.py will automatically add them to 

## Install
```
pip install magic-toolbox 
poety add magic-toolbox
```
## Usage

## How to create a new project
```shell
toolbox create_project foo
ls foo
foo.py  tools.py
```
This creates a new project, by creating a project folder, and two python files;
the project file foo.py, and the tools file tools.py.
The project file is used like`python foo.py args`.
## Add new functions.
```shell
cd foo
toolbox add_function bar
cat tools.py
def foo(self,):
        '''
        This is just a dummy sub command to use as an example.
        You can use this as help message.
        '''

def bar(self):
    '''
    Put your doc string here
    '''
    '''
        
```
Inside the project folder you can run the add_function to create a sub-command.
This adds a function to tools.py which is the entry point into your python code.
## Turns current directory into a magic_toolbox project
```shell
toolbox init
```
You can turn the current directory into a project if you like. 

