from mocli.interface import Command
from mocli.config import save_conf, load_conf


LMOD_VERSION = "v0.0.0"
LMOD_RELEASE = "https://github.com/UrsaAlcor/Lmod/releases/download/v0.0.0/lua_static_x86_64"


class InstallLmod(Command):
    name: str = "init"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(InstallLmod.name, help='Install Lmod on your system')
        parser.add_argument("path", type=str, help='Location of the installation')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = InstallLmod
