from mocli.interface import Command
from mocli.config import save_conf, load_conf


class Uninstall(Command):
    name: str = "uninstall"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Uninstall.name, help='Remove a Lmod installation')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = Uninstall
