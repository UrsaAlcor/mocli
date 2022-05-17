import shutil

from mocli.config import option
from mocli.interface import Command


class Remove(Command):
    name: str = "remove"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Remove.name, help="Remove a Lmod installation")
        parser.add_argument(
            "--user", action="store_true", help="Remove the user installation"
        )

    @staticmethod
    def execute(args):
        package = args.package

        root = option("root")

        if args.user:
            root = option("local", None)

        if root is None:
            raise RuntimeError("Installation path is not defined")

        shutil.rmtree(root)


COMMAND = Remove
