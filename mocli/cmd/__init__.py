import os
import glob


def fetch_factories(base_module, base_file_name, function_name='COMMAND'):
    factories = {}
    module_path = os.path.dirname(os.path.abspath(base_file_name))

    for module_path in glob.glob(os.path.join(module_path, '[A-Za-z]*.py')):
        module_file = module_path.split(os.sep)[-1]

        if module_file == base_file_name:
            continue

        module_name = module_file.split(".py")[0]

        try:
            module = __import__(".".join([base_module, module_name]), fromlist=[''])
        except ImportError as e:
            continue

        if hasattr(module, function_name):
            cmd = getattr(module, function_name)

            factories[cmd.name] = cmd

    return factories


commands = fetch_factories('mocli.commands', __file__)
