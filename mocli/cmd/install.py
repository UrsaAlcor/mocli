import os
import subprocess
import tempfile

from mocli.interface import Command
from mocli.config import option


class Install(Command):
    name: str = "install"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Install.name, help='Install a Lmod package')
        parser.add_argument("package", type=str, help='Name of the package to install (lua or lua/v5.4.3)')
        parser.add_argument("--user", action='store_true', help='Make the install in user space')

    @staticmethod
    def execute(args):
        package = args.package

        root = option('root')
        
        if args.user:
            root = option('local', None)

        if root is None:
            raise RuntimeError("Installation path is not defined")

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            # Download package
            # subprocess.run(f'wget {LMOD_RELEASE}', shell=True, check=True)

            filename = (subprocess.run('ls', check=True, stdout=subprocess.PIPE)
                .stdout
                .decode('utf-8')
                .strip()
            )

            subprocess.run(f'unzip {filename} -d {root}', shell=True, check=True)


COMMAND = Install
