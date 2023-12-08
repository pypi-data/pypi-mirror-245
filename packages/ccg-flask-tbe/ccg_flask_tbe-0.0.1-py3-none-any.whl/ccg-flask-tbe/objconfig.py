from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from domaineconfig import DomaineConfig

class ObjConf:
    def __init__(self, fichier):
        self.objs = list()
        
        file = load(open(fichier), Loader=Loader)
        for domaine in file['domaine']:
            for subdomaine in domaine:
                for objet in domaine[subdomaine]:
                    obj = DomaineConfig(domaine = subdomaine, name = objet['name'], command = objet['command'])
                    for action in objet['actions']:
                        for kaction, vaction in action.items():
                            obj.add_dc_actions(kaction)
                            if vaction == None:
                                pass
                            else:
                                for item in action[kaction]:
                                    arguments = dict()
                                    for subitem in item.items():
                                        arguments[subitem[0]] = subitem[1]
                                    obj.actions[kaction].add_ac_args(arguments)
                    self.objs.append(obj)
        
    def get_oc_by_domaine(self, domaine):
        new_objs = list()
        for dom in self.objs:
            if dom.domaine == domaine: new_objs.append(dom)
        self.objs = new_objs

    def get_oc_by_objet(self, objet):
        new_objs = list()
        for obj in self.objs:
            if obj.command == objet: new_objs.append(obj)
        self.objs = new_objs