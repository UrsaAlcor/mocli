from mocli.interface import Command
from mocli.config import save_conf, load_conf


class Apt(Command):
    name: str = "aptinstall"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Apt.name, help='Install a apt package inside lmod')

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf['root'] = path
        save_conf(conf)

        # Install Lmod


COMMAND = Apt
