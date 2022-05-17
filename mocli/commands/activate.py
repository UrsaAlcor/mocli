import os

from mocli.config import CONFIG, option, update_conf
from mocli.interface import Command

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
    return template.format(modules=modules, root=root)


class Activate(Command):
    name: str = "activate"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Activate.name, help="Show how to activate alcor")
        parser.add_argument("--auto", action="store_true")
        parser.add_argument("--force", action="store_true")

    @staticmethod
    def execute(args):
        root = option("root")
        modules = option("modules")

        if root is None or modules is None:
            raise RuntimeError(f"alcor is not installed on this system")

        code = bash_activation(root, modules)
        print(code)

        home = os.path.expanduser("~")
        bash_file = os.path.join(CONFIG, "bashrc")
        os.makedirs(CONFIG, exist_ok=True)

        # Update bashrc if enabled
        if args.auto:
            print(f"Activation code written to {bash_file}")
            print(f"    `exec bash` to update environment")

            old_auto = option("auto")
            update_conf(auto=args.auto)

            with open(bash_file, "w") as file:
                file.write(code)

            if not old_auto or args.force:
                with open(f"{home}/.bashrc", "a") as file:
                    file.write(f"\nsource {CONFIG}/bashrc\nactivate_alcor\n")


COMMAND = Activate
