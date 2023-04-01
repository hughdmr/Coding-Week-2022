## Importations ##

import json
from tweets_collect.search_tweets import *

## Fonctions ##


def to_json(tweets, nom_fichier):
    """
    tweets: liste de tweets en entrée
    Ne renvoie rien (procédure) mais crée un fichier json avec les données associées
    """
    L_json = []
    for k in tweets:
        data = k._json
        L_json.append(data)

    try:
        with open("./projet_w2/InsultBlock/tweets_data/" + nom_fichier, 'r') as file:
            L = json.load(file)
            pass
    except IOError:
        with open("./projet_w2/InsultBlock/tweets_data/" + nom_fichier, "w") as file:
            json.dump(L_json, file)
