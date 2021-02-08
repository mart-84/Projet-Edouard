def categorieAfficher(listCategorie: list):
    message = "Les catégories déjà existantes sont :\n"
    for cat in listCategorie:
        message += " →  " + cat.capitalize() + "\n"
    return message


def changeCategorie(data: list, nouvelle: str, index: int) -> list:
    message = "Catégorie modifiée"
    nData = data
    nData[index - 1]["categorie"] = nouvelle.lower()
    return nData, message


def categorieSupprimer(data: list, categorie: str) -> list:
    nData = data
    for todo in nData:
        if todo["categorie"] == categorie:
            todo["categorie"] = "autre"
    return nData


def categorieAide():
    return "Pas encore fait :/"
