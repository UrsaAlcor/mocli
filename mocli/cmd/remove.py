from mocli.interface import Command
from mocli.config import save_conf, load_conf


class Remove(Command):
    name: str = "remove"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Remove.name, help='Remove a Lmod installation')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = Remove
