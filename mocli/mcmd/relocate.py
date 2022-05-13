from mocli.config import load_conf, save_conf
from mocli.interface import Command


class Relocate(Command):
    name: str = "relocate"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(
            Relocate.name, help="Relocate a Lmod installation"
        )

    @staticmethod
    def execute(args):
        path = args.path

        conf = load_conf()
        conf["root"] = path
        save_conf(conf)

        # Install Lmod


COMMAND = Relocate
