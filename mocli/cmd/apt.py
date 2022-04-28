import os
import tempfile
import subprocess

from mocli.interface import Command
from mocli.config import option


class Apt(Command):
    name: str = "aptinstall"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Apt.name, help='Install a apt package inside lmod')
        parser.add_argument("package", type=str, help='package name used by aptitude')

    @staticmethod
    def execute(args):
        package = args.package

        root = option('root')

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            subprocess.run(f'apt download {package}', shell=True, check=True)

            filename = (subprocess.run('ls', check=True, stdout=subprocess.PIPE)
                .stdout
                .decode('utf-8')
                .strip()
            )

            dest = os.path.join(root, package, 'apt')
            subprocess.run(f'dpkg-deb -xv {filename} {dest}')


COMMAND = Apt
