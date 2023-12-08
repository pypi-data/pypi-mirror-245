import csv
import sys

class ParseFile:
    def __init__(self, file):
        self.filelist = list()
        try:
            fichier = open(file,'r')
            csvreader = csv.reader(fichier)
            for ligne in csvreader:
                self.filelist.append(ligne)
        except Exception as error:
            self.filelist.append(error)