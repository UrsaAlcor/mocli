from io import UnsupportedOperation
import os
import subprocess
import tempfile

from mocli.interface import Command
from mocli.config import update_conf


LMOD_ARCH = {'aarch64', 'ppc64le', 'riscv64', 'x86_64'}
LMOD_VERSION = "v0.0.0"
LMOD_RELEASE = "https://github.com/UrsaAlcor/Lmod/releases/download/v0.0.0/lmod_x86_64.zip"


def fetch_old_path(root):
    """Read a lmod lua file to read the expected location of the lua install"""
    addto_file = os.path.join(root, 'lmod/lmod/libexec/addto')
    
    with open(addto_file, 'r') as file:
        firstline = file.readline()

    base_lua = "/noarch/lua/v5.4.3/bin/lua"

    # firstline will be like
    #   #!/home/newton/work/Alcor/lmod/dist/noarch/lua/v5.4.3/bin/lua
    old_path = firstline[2:-len(base_lua)]

    return old_path


def update_lua_path(root, dist_path):
    """Recursively go through the lmod install and update the expected lua location"""
    old_path = fetch_old_path(root)
    cmd = f'find {root} -type f -print0 | xargs -0 sed -i -e "s@{old_path}@{dist_path}@g"'
    subprocess.run(cmd, shell=True, check=True)


class InstallLmod(Command):
    name: str = "init"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(InstallLmod.name, help='Install Lmod on your system')
        parser.add_argument("path", type=str, help='Base root location of the installation')
        parser.add_argument("--dist", type=str, default=None, help='Alternate location for binary distribution')
        parser.add_argument("--modules", type=str, default=None, help='Alternate location for module files')
        parser.add_argument("--arch", type=str, default=None, help='Architecture to install')

    @staticmethod
    def execute(args):
        path = args.path
        dist = args.dist or os.path.join(path, 'dist')
        modules = args.modules or os.path.join(path, 'modules')
        arch = args.arch

        if arch is not None:
            if not arch in LMOD_ARCH:
                raise UnsupportedOperation(f"{arch} is not supported")
            
            print('Other arch are not implemented yet')

        update_conf(root=path)

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            subprocess.run(f'wget {LMOD_RELEASE}', shell=True, check=True)

            filename = (subprocess.run('ls', check=True, stdout=subprocess.PIPE)
                .stdout
                .decode('utf-8')
                .strip()
            )

            # unzip the distribution
            subprocess.run(f'unzip {filename} -d {path}', shell=True, check=True)

            # Update distribution
            if args.dist:
                # Move the distribution folder
                print('Custom distribution folder is not yet implemented')

            # update paths to match
            update_lua_path(path, dist)

            # Update Module files
            if args.modules:
                # Move the module folder
                print('Custom modules folder is not yet implemented')


COMMAND = InstallLmod
