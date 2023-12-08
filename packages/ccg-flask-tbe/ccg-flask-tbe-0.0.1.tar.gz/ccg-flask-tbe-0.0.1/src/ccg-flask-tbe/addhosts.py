class AddHosts:
    def __init__(self, donnees, centreonObjets):
        self.data = dict()
        self.data["centreonObjets"] = centreonObjets.data
        list_donnees = list()
        cpt_errors = 0
        for donnee in donnees.split('\n'):
            if donnee.strip() != "":
                if donnee.count(";") != centreonObjets.data["confObjets"].objs[0].actions["ADD"].args[0].parametres.count(";"):
                    list_donnees.append("ERROR : " + donnee.strip())
                    cpt_errors += 1
                else:
                    list_donnees.append(donnee.strip())

        self.data['erreur'] = cpt_errors  
        self.data["donnees"] = list_donnees
        