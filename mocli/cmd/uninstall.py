import os
import shutil

from mocli.interface import Command
from mocli.config import option


class Uninstall(Command):
    name: str = "uninstall"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Uninstall.name, help='Remove a Lmod installation')
        parser.add_argument('package', help='Package to remove')
        parser.add_argument("--user", action='store_true', help='Remove the user installation')

    @staticmethod
    def execute(args):
        package = args.package

        root = option('root')
        
        if args.user:
            root = option('local', None)

        if root is None:
            raise RuntimeError("Installation path is not defined")

        shutil.rmtree(os.path.join(root, package))


COMMAND = Uninstall
