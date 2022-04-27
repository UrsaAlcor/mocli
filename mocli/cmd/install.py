from mocli.interface import Command
from mocli.config import save_conf, load_conf


class Install(Command):
    name: str = "install"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Install.name, help='Install a Lmod package')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = Install
