## Importations ##

from tweets_collect.to_json import *
from tweets_collect.to_dataframe import *

## Programme ##


def main_user(username, nombre=100):
    Tweets = get_tweets_postedby(username, nombre)
    nom_fichier = 'data_' + username + '.json'
    to_json(Tweets, nom_fichier)
    data = to_dataframe(nom_fichier)
    data = epuration_dataframe(data)
    return data


def main_subject(subject, nombre=100):
    Tweets = get_tweets_queries([subject], nombre)
    nom_fichier = 'data_' + subject + '.json'
    to_json(Tweets, nom_fichier)
    data = to_dataframe(nom_fichier)
    data = epuration_dataframe(data)
    return data

## Tests ##


def test_main_user():
    data = main_user("EmmanuelMacron", 100)
    assert data.empty == False
    assert data['text'].empty == False
    assert type(data['text'][0]) == str


def test_main_subject():
    data = main_subject("agriculture", 100)
    assert data.empty == False
    assert data['text'].empty == False
    assert type(data['text'][0]) == str

## Execution ##


if __name__ == '__main__':
    data = main_subject("G20", 300)
