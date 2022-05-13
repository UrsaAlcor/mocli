from io import UnsupportedOperation
import os
import subprocess
import tempfile
import shutil
import logging

from mocli.interface import Command
from mocli.config import update_conf
from mocli.cmd.activate import bash_activation


logger = logging.getLogger(__file__)

LMOD_ARCH = {'aarch64', 'ppc64le', 'riscv64', 'x86_64'}
LMOD_VERSION = "v0.0.0"
LMOD_RELEASE = "https://github.com/UrsaAlcor/Lmod/releases/download/v0.0.0/lmod_x86_64.zip"



def fetch_old_dist(root):
    """Read a lmod lua file to read the expected location of the lua install"""
    addto_file = os.path.join(root, 'lmod/libexec/addto')
    
    with open(addto_file, 'r') as file:
        firstline = file.readline()

    base_lua = "/noarch/lua/v5.4.3/bin/lua"

    # firstline will be like
    #   #!/home/newton/work/Alcor/lmod/dist/noarch/lua/v5.4.3/bin/lua
    old_path = firstline[2:-len(base_lua) - 1]

    return old_path

def fetch_old_root(root):
    old_dist = fetch_old_dist(root)
    return os.path.join(*os.path.split(old_dist)[:-1])


def update_root_path(root):
    old_root = fetch_old_root(root)

    # Update Lmod lua files
    cmd = f'find {root} -type f -print0 | xargs -0 sed -i -e "s@{old_root}@{root}@g"'
    subprocess.run(cmd, shell=True, check=True)


def update_lua_path(root, dist_path):
    """Recursively go through the lmod install and update the expected lua location"""
    old_path = fetch_old_dist(root)

    logger.debug("Updating dist path from %s to %s", old_path, dist_path)

    # Update Lmod lua files
    cmd = f'find {root} -type f -print0 | xargs -0 sed -i -e "s@{old_path}@{dist_path}@g"'
    subprocess.run(cmd, shell=True, check=True)

    # Update noarch lua files
    cmd = f'find {dist_path} -type f -print0 | xargs -0 sed -i -e "s@{old_path}@{dist_path}@g"'
    subprocess.run(cmd, shell=True, check=True)


def update_modules_path(root, old, new):
    """Recursively go through the lmod install and update the expected modules location"""
    pass


def move_content(src, dest):
    """Move all the files contained inside src to dst"""
    os.makedirs(dest, exist_ok=True)

    file_names = os.listdir(src)
    
    for file_name in file_names:
        shutil.move(os.path.join(src, file_name), dest)


def move_dist(root, old_dist, new_dist, force=False):
    # Update distribution
    if old_dist != new_dist:
        move_content(old_dist, new_dist)

    if force:
        # update paths to match
        update_lua_path(root, new_dist)
    

def move_modules(root, old_modules, new_modules, force=False):
    if old_modules != new_modules:
        print('Custom modules folder is not yet implemented')
        move_content(old_modules, new_modules)

    if force:
        # update paths to match
        update_modules_path(root, old_modules, new_modules)


class InstallLmod(Command):
    """Install lmod
    
    Parameters
    ----------
    path: str
        Root to the lmod installation
    
    dist: str
        Path to the binaries (distributables)
    
    modules: str
        Path to lmod module files
    
    arch: str
        name of the arch to install
    
    Examples
    --------
    
    .. code-block:

        alcor init /opt/alcor --dist /opt/alcor/dist --modules /opt/aclor/modules
    
    """
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

        update_conf(root=path, dist=dist, modules=modules)

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            subprocess.run(f'wget {LMOD_RELEASE}', shell=True, check=True)

            filename = (subprocess.run('ls', check=True, stdout=subprocess.PIPE)
                .stdout
                .decode('utf-8')
                .strip()
            )

            # unzip the distribution
            with tempfile.TemporaryDirectory() as dirname:
                subprocess.run(f'unzip {filename} -d {dirname}/', shell=True, check=True)
                shutil.move(f'{dirname}/lmod', path)
                update_root_path(path)

            move_dist(path, os.path.join(path, 'dist'), dist, force=True)
            move_modules(path, os.path.join(path, 'modules'), modules, force=True)

        logging.debug("Finished")
        print(bash_activation(path, modules))

COMMAND = InstallLmod
