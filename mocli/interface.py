class Command:
    @staticmethod
    def arguments(subparsers):
        raise NotImplementedError()

    @staticmethod
    def execute(args):
        raise NotImplementedError()
