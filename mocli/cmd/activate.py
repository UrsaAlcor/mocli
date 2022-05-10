import os

from mocli.interface import Command
from mocli.config import option, update_conf


template = """
function activate_alcor {{
    export MODULEPATH_ROOT={modules}/$(arch)
    export MODULEPATH={modules}/$(arch)
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
        parser.add_argument("--auto", action='store_true')

    @staticmethod
    def execute(args):
        root = option('root')
        modules = option('modules')

        if root is None or modules is None:
            raise RuntimeError(f"alcor is not installed on this system")

        code = bash_activation(root, modules)
        print(code)

        config_base = os.getenv('XDG_CONFIG_HOME', '~/.config')
        bash_file = os.path.join(config_base, "alcor", "bash.rc")                                 

        # Update bashrc if enabled
        if args.auto:
            old_auto = option('auto')
            update_conf(auto=args.auto)

            with open(bash_file, 'w') as file:
                file.write(code)

            if not old_auto:
                with open('~/.bashrc', 'a') as file:
                    file.write('\nsource ${XDG_CONFIG_HOME:~/.config}/alcor/bash.rc\n')
        

COMMAND = Activate



