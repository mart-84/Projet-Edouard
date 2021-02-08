import requests
import datetime
import re #RegEx
import icalendar as calen
from dateutil import tz


# Renvoie un string avec la date au format JJ/MM/AAAA
def formatDate(valeur):
    result = f'{valeur.day:02}' + "/" + f'{valeur.month:02}' + "/" + f'{valeur.year:04}'
    return result


# Renvoie un string avec l'heure au format HH:MM:SS
def formatHeure(valeur):
    result = str('{0:02d}'.format(valeur.hour)) + ":" + str('{0:02d}'.format(
        valeur.minute))
    return result


# Renvoie une date avec le fuseau horaire Europe/Paris
def changerFuseau(valeur):
    fuseau = tz.gettz(
        "Europe/Paris")  #Fuseau qui s'adapte à l'heure d'été/hiver
    result = valeur.replace(tzinfo=datetime.timezone.utc).astimezone(tz=fuseau)
    return result


# Requete vers le site de l'edt
# Renvoie une liste des cours
def getEmploiDuTemps(debut, fin):
    param = {
        "resources": "9303",
        "projectId": "2",
        "calType": "ical",
        "firstDate": debut,
        "lastDate": fin
    }
    requete = requests.get(
        "http://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp",
        params=param)

    result = calen.Calendar().from_ical(requete.text)
    cours = []
    for e in result.walk('vevent'):
        cour = {}
        cour['matiere'] = str(e.get('summary'))
        cour['salle'] = str(e.get('location'))

        description = str(e.get('description')).split("\n")
        descClasse = []
        descProf = []
        for element in description:
            if element != '' and element[0] != '(':
                if len(element) <= 4:
                    descClasse.append(element)
                else:
                    descProf.append(element)
        cour['groupe'] = descClasse
        cour['prof'] = descProf

        cour['debut'] = formatHeure(changerFuseau(e.get('dtstart').dt))
        cour['fin'] = formatHeure(changerFuseau(e.get('dtend').dt))
        cour['date'] = formatDate(changerFuseau(e.get('dtstart').dt))

        cours.append(cour)

    return cours


def trierCours(cours):
    count = 1
    while count != 0:
        count = 0
        for i in range(len(cours) - 1):
            if cours[i]['date'] > cours[i + 1]['date'] or (cours[i]['date'] == cours[i + 1]['date'] and cours[i]['debut'] > cours[i + 1]['debut']):
                count = count + 1
                temp = cours[i]
                cours[i] = cours[i + 1]
                cours[i + 1] = temp


def editCour(cour):
    matiere = cour['matiere']
    p = re.compile("(?:M\d{4,5}(?:.\d)?-?\d?(?:\/M\d{4}-?| ?)?)(?:(?:(.+)(?: G\d|S\d))|(.* DS)|(.+))")
    m = p.match(matiere).groups()
    if m[0] != None:
        matiere = m[0]
    elif m[1] != None:
        matiere = m[1]
    else:
        matiere = m [2]

    debut = cour['debut']
    fin = cour['fin']
    cours = f"De {debut} à {fin} : **{matiere}**"

    salle = cour['salle']
    if salle != "":
        cours += f" en {salle}"

    if cour['prof'] != []:
        prof = ""
        for e in cour['prof']:
            prof += e.title() + ", "
        prof = prof[:-2]
        cours += f" avec *{prof}*"

    cours += "\n"
    return cours


def editMessage(edt, nbrJours=1):
    message = ""
    if nbrJours == 1:
        message += "**" + edt[0]['date'] + "**\n"
        for cour in edt:
            message += editCour(cour)
    else:
        prevDate = None
        for cour in edt:
            if cour['date'] != prevDate:
                prevDate = cour['date']
                message += "\n**" + prevDate + "**\n"
            message += editCour(cour)
    return message


# Fonction principale
def getEdt(args):
    if len(args) == 0:
        debut = datetime.datetime.today()
        fin = debut
        action = formatDate(debut)
    elif args[0] == "demain":
        debut = datetime.datetime.today()
        delta = datetime.timedelta(days=1)
        debut = debut + delta
        fin = debut
        action = formatDate(debut)
    elif len(args) == 1 or args[0] == args[1]:
        try:
            debut = datetime.datetime.strptime(args[0], '%d/%m/%Y')
        except:
            debut = args[0]
        fin = debut
        action = formatDate(debut)
    elif len(args) == 2:
        debut = datetime.datetime.strptime(args[0], '%d/%m/%Y')
        fin = datetime.datetime.strptime(args[1], '%d/%m/%Y')
        if debut > fin:
            debut, fin = fin, debut
        action = formatDate(debut) + " à " + formatDate(fin)

    edt = getEmploiDuTemps(debut, fin)
    trierCours(edt)
    message = ""

    if edt == []:
        message = "Rien de spécial de prévu "
        if len(args) == 0:
            message += "aujourd'hui"
        elif len(args) == 1:
            message += "ce jour là"
        else:
            message += "sur cette période"
    else:
        if len(args) == 2:
            message = editMessage(edt, 2)
        else:
            message = editMessage(edt)

    return message, action
