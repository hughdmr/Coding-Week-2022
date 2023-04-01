## Importations ##

import pickle
import numpy as np
import pandas as pd
from insult_detector.sklearn_entrainement import *

## Fonctions ##

X_data, y = creation_dataset('train2.csv', 0, 500)


def chargement(nom_modele):
    """
    charge le modèle de ML entraîné précédemment
    entrée: nom du modèle de machine learning (str)
    sortie: objets ML: modèle, réduction en vecteur et fréquencisation dans les variables "model", 'vectorizer" et "tfidfconverter"
    """
    with open('./projet_w2/InsultBlock/insult_detector/train_data/' + nom_modele, 'rb') as training_model:
        model, vectorizer, tfidfconverter = pickle.load(training_model)
    return model, vectorizer, tfidfconverter


def detecteur_ML(X_data, model, vectorizer, tfidfconverter):
    """
    détecte si un set de tweets sont des insultes ou non;
    entrée: X_data, pandas.Series de tweets (chaine de caractère/str), model RandomForest entraîné, et 2 objets sklearn
    sortie: np.ndarray tq 1 pour les tweets haineux, 0 sinon (ordre conservé);
    """
    L_Tweets = preprocessing(X_data)
    X_convert = conversion_sklearn_transform(
        L_Tweets, vectorizer, tfidfconverter)
    y_result = model.predict(X_convert)
    return y_result


def detecteur_v3(text):
    model, vectorizer, tfidfconverter = chargement('text_classifier')
    X_data = pd.Series(text)
    y_result = detecteur_ML(X_data, model, vectorizer, tfidfconverter)
    return (y_result[0] == 1)

## Tests ##


def test_chargement():
    model = chargement('text_classifier')
    assert model != None


def test_detecteur_ML():
    model = chargement('text_classifier')
    b = detecteur_ML(X_data, model)
    assert type(b) == np.ndarray

## Execution ##


if __name__ == '__main__':
    model, vectorizer, tfidfconverter = chargement('text_classifier')
    print(X_data[37])
    y_result = detecteur_ML(X_data, model, vectorizer, tfidfconverter)
    print(np.where(y_result == 1))
    print(detecteur_v3(
        "katie hopkins: why wonât the left admit the #truth about islam?  @user #islam #political   #jealous #hate"))
