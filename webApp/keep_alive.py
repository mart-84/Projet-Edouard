from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging


def create_app():
    app = Flask("Ed0uard")
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.config["SECRET_KEY"] = "12345"
    socketio.init_app(app)
    print("Démarrage de l'application web")
    return app


socketio = SocketIO(async_mode='threading', debug=False)
app = create_app()


def getTypeOfLog(texte):
    test = texte[:12]
    if test == "Erreur levée":
        type_ = "erreur"
    elif test in "Commande activée":
        type_ = "commande"
    elif test == "Bot connecté":
        type_ = "connexion"
    else:
        type_ = "autre"
    return type_


@app.route('/')
def home():
    with open("discord.log") as file:
        rawTxt = file.readlines()
    if rawTxt == []:
        content = [{"message": "Aucun log enregistré", "type": ""}]
    else:
        content = []
        for line in rawTxt:
            newLine = {}
            newLine["message"] = line
            newLine["type"] = getTypeOfLog(line[23:])
            content.insert(0, newLine)
    return render_template("page.html", content=content)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@socketio.on('connexion', namespace='/')
def connexion(arg):
    print("Nouvelle connexion à l'interface web")
    emit('reponseConnexion', {"data": "ok"})


def updateLogs(message, time_):
    test = message[:12]
    if test == "Erreur levée":
        type_ = "erreur"
    elif test in "Commande activée":
        type_ = "commande"
    elif test == "Bot connecté":
        type_ = "connexion"
    else:
        type_ = "autre"

    data = {
        "time": time_,
        "msg": message.replace("<", "&lt").replace(">", "&gt"),
        "type": type_
    }
    socketio.emit('nouveauteBis', data, namespace='/')


@socketio.on('clearLog', namespace='/')
def clearLog(arg):
    file = open("discord.log", "w")
    file.close()
    print("Logs effacés depuis l'interface web")


def keep_alive():
    socketio.run(app, host='0.0.0.0')
