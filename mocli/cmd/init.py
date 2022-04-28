import os
import subprocess
import tempfile

from mocli.interface import Command
from mocli.config import update_conf


LMOD_VERSION = "v0.0.0"
LMOD_RELEASE = "https://github.com/UrsaAlcor/Lmod/releases/download/v0.0.0/lua_static_x86_64"


class InstallLmod(Command):
    name: str = "init"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(InstallLmod.name, help='Install Lmod on your system')
        parser.add_argument("path", type=str, help='Location of the installation')

    @staticmethod
    def execute(args):
        path = args.path

        update_conf(root=path)

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            subprocess.run(f'wget {LMOD_RELEASE}', shell=True, check=True)

            filename = (subprocess.run('ls', check=True, stdout=subprocess.PIPE)
                .stdout
                .decode('utf-8')
                .strip()
            )

            subprocess.run(f'unzip {filename} -d {path}', shell=True, check=True)


COMMAND = InstallLmod
