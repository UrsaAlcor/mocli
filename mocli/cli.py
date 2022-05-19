import logging
from argparse import ArgumentParser

from mocli.commands import commands


def parse_args():
    parser = ArgumentParser()
    # Root Arguments

    # --
    subparsers = parser.add_subparsers(dest="command")

    for _, command in commands.items():
        command.arguments(subparsers)

    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    cmd_name = args.command
    command = commands.get(cmd_name)

    if command is None:
        print(f"Action `{cmd_name}` not implemented")
        return

    command.execute(args)


if __name__ == "__main__":
    main()
