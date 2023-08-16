from collections import defaultdict
import glob
import os
import shutil
import subprocess
import tempfile

import functools
import requests

from mocli.config import option
from mocli.interface import Command



# TODO: find a way to make this dynamic
# maybe we can use github API to query the org and just have a list of the exceptions
#
default_packages = {
    "lz4": "https://github.com/UrsaAlcor/lz4/releases/download/v0.0.1/lz4_x86_64.zip",
    "link": "https://github.com/UrsaAlcor/link/releases/download/v0.0.4/linker_noarch.zip",
    "libjpeg-turbo": "https://github.com/UrsaAlcor/libjpeg-turbo/releases/download/v0.0.0/libjpeg-turbo_x86_64.zip",
    "nasm": "https://github.com/UrsaAlcor/nasm/releases/download/v0.0.0/nasm_x86_64.zip",
    "bzip2": "https://github.com/UrsaAlcor/bzip2/releases/download/v0.0.1/bzip2_x86_64.zip",
    "python": "https://github.com/UrsaAlcor/python/releases/download/v0.0.2/python_x86_64.zip",
}

org = 'UrsaAlcor'

ignore_list = {
    'mocli',
    'cookiewrapper',
    'Lmod',
    'docs'
}


@functools.cache
def get_repos():
    response = requests.get(f'https://api.github.com/orgs/{org}/repos')
    
    if response.status_code == 200:
        repositories = response.json()
        return [repo['name'] for repo in repositories if repo['name'] not in ignore_list]
    else:
        print("Could not query github")
        return []


@functools.cache
def get_release(repo):
    packages = dict()

    response = requests.get(f'https://api.github.com/repos/{org}/{repo}/releases')
    
    if response.status_code == 200:
        releases = response.json()
        
        packages[repo] = []
        for release in releases:
            packages[repo].append({
                'name': release['name'],
                'version': release['tag_name'],
                'assets': release['assets']
            })
    else:
        print("Could not query github")
            
    return packages


def build_package_list():
    package_names = get_repos()
    releases = {}
    
    for name in package_names:
        releases.update(get_release(name))

    return releases


class UnknownPackage(Exception):
    pass


class NoRelease(Exception):
    pass


def resolve_package(name, version=None, arch=None):
    return default_packages.get(name)
    
    packages = build_package_list()
    
    if name not in packages:
        raise UnknownPackage(f"Select from: {', '.join(get_repos())}")
    
    releases = packages[name]
    
    if len(releases) == 0:
        raise NoRelease(f"No release made for {name}")
    
    selected_release = releases[-1]
    if version is not None:
        for release in releases:
            if release['version'] == version:
                selected_release = release
                break
    
    arch = arch or 'x86_64'
    url = None
    
    for asset in selected_release['assets']:
        if arch in asset['name']:
            url = asset[['browser_download_url']] 
            
    return url


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
