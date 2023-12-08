from argsconfig import ArgsConfig

class ActionsConfig:
    def __init__(self, command):
        self.command = command
        self.args = list()

    def add_ac_args(self, args):
        Args = ArgsConfig(args)
        self.args.append(Args)
