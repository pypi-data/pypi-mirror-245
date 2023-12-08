from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class CentreonConfig:
    def __init__(self, fichier):
        file = load(open(fichier), Loader=Loader)
        self.command = file['command']
        self.user = file['user']
        self.password = file['password']
        self.sha = file['sha']
        self.objet = file['objet']
        self.action = file['action']

    def get_command(self):
        return self.command
    
    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_sha(self):
        return self.sha
    
    def get_objet(self):
        return self.objet

    def get_action(self):
        return self.action
    
    def get_all(self):
        return self.command, self.user, self.password, self.sha, self.objet, self.action

    def to_text(self):
        text = self.command + " " + self.user + " " + self.password + " " + self.sha + " " + self.objet + " " + self.action
        return text