from mocli.interface import Command
from mocli.config import option


template = """
function activate_alcor {{
    export MODULEPATH_ROOT={modules}
    export MODULEPATH={modules}
    export LMOD_SYSTEM_DEFAULT_MODULES=${{LMOD_SYSTEM_DEFAULT_MODULES:-"StdEnv"}}

    source {root}/lmod/init/profile

    if [ -z "$__Init_Default_Modules" ]; then
        export __Init_Default_Modules=1;

        ## ability to predefine elsewhere the default list
        LMOD_SYSTEM_DEFAULT_MODULES=${{LMOD_SYSTEM_DEFAULT_MODULES:-"StdEnv"}}
        export LMOD_SYSTEM_DEFAULT_MODULES
        module --initial_load --no_redirect restore
    else
        module refresh
    fi
}}
"""


def bash_activation(root, modules):
    return template.format(
        modules=modules,
        root=root
    )


class Activate(Command):
    name: str = "activate"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Activate.name, help='Show how to activate alcor')

    @staticmethod
    def execute(args):
        root = option('root')
        modules = option('dist')

        if root is None or modules is None:
            raise RuntimeError(f"alcor is not installed on this system")

        print(bash_activation(root, modules))
    

COMMAND = Activate



