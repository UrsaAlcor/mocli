import os
import subprocess
import tempfile

from mocli.config import option, update_conf
from mocli.interface import Command


class LocalLmod(Command):
    name: str = "local"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(
            LocalLmod.name, help="Create a module path for users"
        )
        parser.add_argument("path", help="Lmod module user path")

    @staticmethod
    def execute(args):
        path = args.path
        update_conf(local=path)

        # if bash.rc
        auto = option("auto")


COMMAND = LocalLmod
