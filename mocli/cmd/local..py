from mocli.interface import Command
from mocli.config import save_conf, load_conf


class LocalLmod(Command):
    name: str = "local"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(LocalLmod.name, help='Create a module path for users')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = LocalLmod
