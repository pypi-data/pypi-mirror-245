from centreonconfig import CentreonConfig
from objconfig import ObjConf

class CentreonObjets:
    def __init__(self, confCentreon, confObjets):
        self.data = dict()
        self.data['confCentreon'] = confCentreon
        self.data['confObjets'] = confObjets
