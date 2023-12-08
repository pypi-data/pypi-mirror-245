"""The flask application"""
#!/usr/bin/env python3

from flask import Flask, Response, render_template, request, flash, url_for  # pylint: disable=import-error
from markupsafe import Markup
from werkzeug.utils import secure_filename
import os
from centreonobjets import CentreonObjets
from centreonconfig import CentreonConfig
from objconfig import ObjConf
from addhosts import AddHosts
from addservices import AddServices
from parsefile import ParseFile

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')  
    confCO = CentreonObjets(confCentreon, confObjets)
    return render_template('index.html', data=confCO.data)

@app.route('/scriptaddhosts', methods = ['GET', 'POST'])
def scriptaddhosts():
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_objet("HOST")
    confCO = CentreonObjets(confCentreon, confObjets)
    if request.method == 'POST':
        if 'formFile' in request.files:
            formFichier = request.files['formFile']
            fichier = secure_filename(formFichier.filename)
            formFichier.save(os.path.join(app.config['UPLOAD_FOLDER'], fichier))
            parsed = ParseFile(os.path.join(app.config['UPLOAD_FOLDER'], fichier))
            confCO.data['filelist'] = parsed.filelist
    return render_template('scriptaddhosts.html', data=confCO.data)

@app.route('/scriptaddservices', methods = ['GET', 'POST'])
def scriptaddservices():
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_objet("SERVICE")
    confCO = CentreonObjets(confCentreon, confObjets)
    if request.method == 'POST':
        if 'formFile' in request.files:
            formFichier = request.files['formFile']
            fichier = secure_filename(formFichier.filename)
            formFichier.save(os.path.join(app.config['UPLOAD_FOLDER'], fichier))
            parsed = ParseFile(os.path.join(app.config['UPLOAD_FOLDER'], fichier))
            confCO.data['filelist'] = parsed.filelist
    return render_template('scriptaddservices.html', data=confCO.data)

@app.get('/clapi/objet/<objet>')
def clapi_get_objet(objet):
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_objet(objet)
    confCO = CentreonObjets(confCentreon, confObjets)
    return render_template('navigation_actions.html', data=confCO.data)

@app.get('/clapi/domaine/<domaine>')
def clapi_get_domaine(domaine):
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_domaine(domaine)
    confCO = CentreonObjets(confCentreon, confObjets)
    return render_template('navigation_objets.html', data=confCO.data)

@app.post('/addhosts')
def addhosts():
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_objet("HOST")
    confCO = CentreonObjets(confCentreon, confObjets)
    donnees = request.form['zoneTexte']
    commandes = AddHosts(donnees, confCO)
    return render_template('addhosts.html', data=commandes.data)

@app.post('/addservices')
def addservices():
    confCentreon = CentreonConfig('centreon.yaml')
    confObjets = ObjConf('ccg-conf.yaml')
    confObjets.get_oc_by_objet("SERVICE")
    confCO = CentreonObjets(confCentreon, confObjets)
    donnees = request.form['zoneTexte']
    commandes = AddServices(donnees, confCO)
    return render_template('addservices.html', data=commandes.data)

@app.errorhandler(500)
def handle_500(error):
    """The error handler"""
    return str(error), 500

if __name__ == '__main__':
    app.run()
