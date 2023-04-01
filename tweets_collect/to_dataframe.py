## Imports ##

import pandas as pd
import json
from pandas import json_normalize

## Fonctions ##

chemin = "./projet_w2/InsultBlock/tweets_data/"


def to_dataframe(nom_fichier):
    """
    entrée: nom de fichier json, en chaine de caractère (string)
    sortie: donée sous forme de dataframe pandas
    """
    with open(chemin+nom_fichier, 'r', encoding='utf-8') as f:
        fichier_json = f.read()
    # Convertir le json en dictionnaire
    info = json.loads(fichier_json)
    # Normalisation
    data_json = json_normalize(info)
    # Création du dataframe à partir du dictionnaire en classant selon les colonnes
    data = pd.DataFrame.from_dict(data_json, orient='columns')
    return data


def epuration_dataframe(data_brut):
    '''
    entrée et sortie: dataframe pandas
    Dataframe simplifié: on ne garde que les attributs (colonnes) intéréssantes
    Amélioration de la date
    '''
    data_twitter = data_brut[['id', 'created_at', 'favorite_count', 'lang', 'retweet_count', 'text', 'user.id', 'user.name', 'user.screen_name',
                              'user.created_at', 'user.description', 'user.favourites_count', 'user.followers_count', 'user.friends_count', 'user.location', 'user.verified', 'entities.user_mentions', 'source']].copy()

    data_twitter['created_at'] = data_twitter['created_at'].apply(
        lambda x: x[0:19])
    return data_twitter


def epuration_dataframe_elevee(data_brut):
    '''
    entrée et sortie: dataframe pandas
    Dataframe simplifié: on ne garde que les attributs (colonnes) intéréssantes
    Amélioration de la date
    '''
    data_twitter = data_brut[['text', 'favorite_count', 'retweet_count', 'user.screen_name',  'user.name', 'created_at', 'user.description',
                              'user.created_at', 'user.followers_count', 'user.friends_count', 'user.location', 'user.verified']].copy()

    data_twitter['created_at'] = data_twitter['created_at'].apply(
        lambda x: x[0:19])
    return data_twitter


## Tests ##


def test_to_dataframe():
    data = to_dataframe('data_test.json')
    assert data["retweet_count"][0] == 3354


def test_epuration_dataframe():
    data = to_dataframe('data_test.json')
    data_simple = epuration_dataframe(data)
    assert data_simple["retweet_count"][0] == 3354
    assert data_simple["created_at"][0] == 'Tue Nov 13 15:22:17'
