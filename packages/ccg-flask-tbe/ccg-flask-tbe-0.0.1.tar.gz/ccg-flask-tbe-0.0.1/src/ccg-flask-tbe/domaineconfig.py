from actionsconfig import ActionsConfig

class DomaineConfig:
    def __init__(self, domaine, name, command):
        self.domaine = domaine
        self.name = name
        self.command = command
        self.actions = dict()

    def add_dc_actions(self, action):
        Action = ActionsConfig(action)
        self.actions[action] = Action

    