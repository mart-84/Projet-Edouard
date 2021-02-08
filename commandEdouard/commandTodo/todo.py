import json
# Fichier perso
from .categorie import categorieAfficher, changeCategorie, categorieSupprimer, categorieAide


def loadTodos(userId):
    try:
        with open("commandEdouard/commandTodo/dataTodo/" + str(userId) + ".json") as jsonFile:
            return json.load(jsonFile)
    except:
        return []


def countTodo(data):
    count = len(data)
    return count


def saveTodos(todos, userId):
    jsonFile = open("commandEdouard/commandTodo/dataTodo/" + str(userId) + ".json", 'w')
    json.dump(todos, jsonFile, indent=2)
    jsonFile.close()


def listCategoriesTodo(data: list) -> list:
    categories = []
    for todo in data:
        if not todo["categorie"] in categories:
            categories.append(todo["categorie"])
    return categories


def displayTodo(args: list, data: list):
    message = ""
    action = ""
    if len(args) <= 1:
        if data == []:
            message += "Aucun Todo enregistré"
        else:
            message += "Todo enregistrés :\n\n"
            for categorie in listCategoriesTodo(data):
                message += "  --- **" + categorie.capitalize() + "** ---\n"
                for dat in data:
                    if categorie == dat["categorie"]:
                        message += "N°" + str(
                            dat["number"]) + "\t- " + dat["content"] + "\n"
        action = "Affichage de tous les Todo"
    else:
        try:
            index = int(args[1])
            if index <= len(data):
                todo = data[index - 1]
                message += "Todo N°" + str(
                    todo["number"]) + "\t- " + todo["content"]
            else:
                message = "Ce Todo n'existe pas !"
            action = "Affichage du Todo n°" + str(todo["number"])
        except:
            index = args[1]
            categorie = args[1]
            if categorie in listCategoriesTodo(data):
                message += "Todo dans la catégorie : **" + categorie.capitalize(
                ) + "**\n"
                for dat in data:
                    if dat["categorie"] == categorie:
                        message += "N°" + str(
                            dat["number"]) + "\t- " + dat["content"] + "\n"
            else:
                message = "Cette catégorie n'existe pas."
            action = "Affichage des Todo de la catégorie " + categorie.capitalize(
            )

    return message, action


def addTodo(args: list, data: list, index: int) -> list:
    message = ""
    content = ""
    if len(args) >= 2:
        for i in range(1, len(args)):
            content += args[i] + " "
    else:
        raise

    message += "Todo n°" + str(index + 1) + " ajouté :\n" + content
    newTodo = dict()
    newTodo["number"] = index + 1
    newTodo["categorie"] = "autre"
    newTodo["content"] = content

    data.append(newTodo)
    return data, message, content


def categorieTodo(data, args, userId):
    message = ""
    if len(args) >= 2:
        if args[1].lower() == "help":
            message = categorieAide()

        elif args[1].lower() == "afficher" or args[1].lower() == "aff":
            message = categorieAfficher(listCategoriesTodo(data))

        elif args[1].lower() == "ajouter" or args[1].lower() == "aj":
            if len(args) < 4:
                raise

            index = ""
            for i in range(3, len(args)):
                index += args[i] + ","

            categorie = args[2]

            index = index.split(",")
            index.pop()
            nData = data
            for i in index:
                result = changeCategorie(nData, categorie, int(i))
                nData = result[0]
                message = result[1]
            saveTodos(nData, userId)

        elif args[1].lower() == "retirer" or args[1].lower() == "ret":
            if len(args) < 3:
                raise
            else:
                index = int(args[3])

            nData, message = changeCategorie(data, "autre", index)
            saveTodos(nData, userId)

        elif args[1].lower() == "supprimer" or args[1].lower() == "sup":
            if len(args) < 3:
                raise

            categorie = args[2]
            if categorie in listCategoriesTodo(data):
                nData, message = categorieSupprimer(data, categorie)
                saveTodos(nData, userId)
            else:
                message = "Cette catégorie n'existe pas."

        else:
            message = "Commande inconnue\n"
            message += categorieAide()
    else:
        message = "Essayer 'todo categorie help' pour plus d'information sur la commande"

    return message


def deleteTodo(args, data):
    if len(args) >= 2:
        index = args[1]
    else:
        raise

    message = ""

    if index == "tout":
        message = "Tous les Todos supprimés"
        return [], message

    index = int(index)
    if index <= len(data):
        message = "Suppression du Todo N°" + str(index)
        data.pop(index - 1)
        i = 1
        for todo in data:
            todo["number"] = i
            i += 1
        return data, message
    else:
        message = "Ce Todo n'existe pas !"
        return None, message


def mainTodo(args, userId):
    data = loadTodos(userId)
    todoNumber = countTodo(data)
    message = ""
    action = ""
    if len(args) == 0:

        message, action = displayTodo(args, data)

    else:
        command = args[0].lower()

        if command == 'afficher' or command == 'aff':

            message, action = displayTodo(args, data)

        elif command == 'ajouter' or command == 'aj':

            newData, message, content = addTodo(args, data, todoNumber)
            saveTodos(newData, userId)
            action = f"Ajout du Todo"

        elif command == 'categorie' or command == 'cat':

            message = categorieTodo(data, args, userId)
            action = "Changement de catégories de Todo"

        elif command == 'supprimer' or command == 'sup':

            newData, message = deleteTodo(args, data)
            action = "Suppression "
            if args[1] == "tout":
                action += "de tous les Todo"
            else:
                action += f"du Todo {args[1]}"

            if newData != None:
                saveTodos(newData, userId)

        elif command == 'help' or command == '?':

            message = "Pas encore fait :/"
            action = "Affichage du message d'aide"

        else:
            raise

    return message, action
