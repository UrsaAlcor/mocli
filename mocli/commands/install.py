import glob
import os
import shutil
import subprocess
import tempfile

from mocli.config import option
from mocli.interface import Command

# TODO: find a way to make this dynamic
# maybe we can use github API to query the org and just have a list of the exceptions
#
packages = {
    "lz4": "https://github.com/UrsaAlcor/lz4/releases/download/v0.0.1/lz4_x86_64.zip",
    "link": "https://github.com/UrsaAlcor/link/releases/download/v0.0.1/linker_x86_64.zip",
    "libjpeg": "https://github.com/UrsaAlcor/libjpeg-turbo/releases/download/v0.0.0/lz4_x86_64.zip",
    "nasm": "https://github.com/UrsaAlcor/nasm/releases/download/v0.0.0/nasm_x86_64.zip",
}


def resolve_package(name):
    return packages.get(name)


def merge_folders(src, dst):
    for file in glob.iglob(f"{src}/**/*", recursive=True):
        newpath = file.replace(src, dst)

        if os.path.isdir(file):
            os.makedirs(newpath, exist_ok=True)
        else:
            print(f"Move {file} to {newpath}")
            shutil.move(file, newpath)


class Install(Command):
    name: str = "install"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(Install.name, help="Install a Lmod package")
        parser.add_argument(
            "package",
            type=str,
            help="Name of the package to install (lua or lua/v5.4.3)",
        )
        parser.add_argument(
            "--user", action="store_true", help="Make the install in user space"
        )
        parser.add_argument(
            "--arch", type=str, default=None, help="Specify a specific arch to install"
        )
        parser.add_argument(
            "--url",
            type=str,
            default=None,
            help="Specify a URL override to download the package",
        )

    @staticmethod
    def execute(args):
        package = args.package

        root = option("root")

        if args.user:
            root = option("local", None)

        if root is None:
            raise RuntimeError("Installation path is not defined")

        package_url = args.url

        if not package_url:
            package_url = resolve_package(package)

        if package_url is None:
            raise RuntimeError(f"`{package}` was not found")

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            # Download package
            subprocess.run(f"wget {package_url}", shell=True, check=True)

            filename = (
                subprocess.run("ls", check=True, stdout=subprocess.PIPE)
                .stdout.decode("utf-8")
                .strip()
            )

            # unzip the distribution
            with tempfile.TemporaryDirectory() as dirname:
                subprocess.run(
                    f"unzip {filename} -d {dirname}/", shell=True, check=True
                )
                merge_folders(f"{dirname}/lmod", root)


COMMAND = Install
