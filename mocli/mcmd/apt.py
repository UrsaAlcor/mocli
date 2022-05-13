import os
import subprocess
import tempfile

import pkg_resources

from mocli.config import option
from mocli.interface import Command


class Apt(Command):
    name: str = "aptinstall"

    @staticmethod
    def arguments(subparsers):
        parser = subparsers.add_parser(
            Apt.name, help="Install a apt package inside lmod"
        )
        parser.add_argument("package", type=str, help="package name used by aptitude")

    @staticmethod
    def execute(args):
        package = args.package
        version = "default"

        dist_all = option("dist")
        dist_arch = os.path.join(dist_all, "x86_64")
        dist_dest = os.path.join(dist_arch, package, version)

        module_all = option("modules")
        module_arch = os.path.join(module_all, "x86_64")
        module_dest = os.path.join(module_arch, package)
        module_file = os.path.join(module_dest, f"{version}.lua")

        with tempfile.TemporaryDirectory() as dirname:
            os.chdir(dirname)

            subprocess.run(f"apt download {package}", shell=True, check=True)

            filename = (
                subprocess.run("ls", check=True, stdout=subprocess.PIPE)
                .stdout.decode("utf-8")
                .strip()
            )

            # opt/alcor/dist/x86_64/libsdl2-dev
            os.makedirs(dist_dest, exist_ok=True)
            subprocess.run(
                f"dpkg-deb -xv {dirname}/{filename} {dist_dest}", shell=True, check=True
            )

        # Create the new module file
        template = pkg_resources.resource_filename(__name__, "templates/ModuleFile.lua")

        with open(template, "r") as template_file:
            template = template_file.read()

        os.makedirs(module_dest, exist_ok=True)
        with open(module_file, "w") as file:
            file.write(
                template.format(
                    package=package,
                    version=version,
                )
            )


COMMAND = Apt
