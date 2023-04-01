## Importations ##


# Modules
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
import pandas
import numpy as np
import re
import nltk
from sklearn.datasets import load_files


# dataset

def creation_dataset(nom_fichier, debut, fin):
    """
    entree: nom du fichier .csv en chaine de caractères (str)
    sortie: X_data pour les données (type pandas.Series), y_data (type pandas.Series) pour les objectifs de valeurs à atteindre: 1 si insulte et 0 sinon
    """
    data = pandas.read_csv(
        './projet_w2/InsultBlock/insult_detector/train_data/' + nom_fichier, sep=',')
    data = data[['tweet', 'label']][debut:fin]
    data.reset_index(inplace=True)
    X_data = data['tweet']
    y_data = data['label']
    return (X_data, y_data)


## Preprocessing ##

vectorizer = CountVectorizer(
    max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
tfidfconverter = TfidfTransformer()


def preprocessing(X_data):
    """
    entrée: pandas.Series qui regroupe l'ensemble des tweets classés dans le même ordre que leur labels dans y_data;
    sortie: L_tweets est une liste des tweets lemmatizés et classés selon le même ordre qu'au début;
    """

    L_tweets = []
    stemmer = WordNetLemmatizer()

    for i in range(0, len(X_data)):
        # Remove all the special characters
        tweet = re.sub(r'\W', ' ', str(X_data[i]))
        # remove all single characters
        tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', tweet)
        # Remove single characters from the start
        tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', tweet)
        # Substituting multiple spaces with single space
        tweet = re.sub(r'\s+', ' ', tweet, flags=re.I)
        # Removing prefixed 'b' (cas lecture des documents)
        tweet = re.sub(r'^b\s+', '', tweet)
        # Converting to Lowercase
        tweet = tweet.lower()
        # Lemmatization
        tweet = tweet.split()
        tweet = [stemmer.lemmatize(word) for word in tweet]
        tweet = ' '.join(tweet)
        L_tweets.append(tweet)
    return L_tweets

## Creation du modèle de ML ##


def conversion_sklearn_fit_transform(L_tweets):
    """
    entrée: documents, liste des tweets lemmatizés et classés selon le même ordre qu'au début;
    sortie: X, tableau numpy np.ndarray converti pour sklearn (tableaux de nombres);
    """
    # Tri des données en mots et passage en forme lisible par l'algorithme
    X_convert = vectorizer.fit_transform(L_tweets).toarray()

    # Analyse TFIDF for "Term frequency" and "Inverse Tweet Frequency"
    # Term frequency = (Number of Occurrences of a word)/(Total words in the document)
    # IDF(word) = Log((Total number of documents)/(Number of documents containing the word))
    # Cela permet de jauger entre la forte présence d'un mot dans un document par rapport à sa forte présence dans l'ensemble des documents
    X_convert = tfidfconverter.fit_transform(X_convert).toarray()
    return X_convert


def conversion_sklearn_transform(L_tweets, vectorizer, tfidfconverter):
    """
    entrée: documents, liste des tweets lemmatizés et classés selon le même ordre qu'au début;
    sortie: X, tableau numpy np.ndarray converti pour sklearn (tableaux de nombres);
    """
    # Tri des données en mots et passage en forme lisible par l'algorithme
    X_convert = vectorizer.transform(L_tweets).toarray()

    # Analyse TFIDF for "Term frequency" and "Inverse Tweet Frequency"
    # Term frequency = (Number of Occurrences of a word)/(Total words in the document)
    # IDF(word) = Log((Total number of documents)/(Number of documents containing the word))
    X_convert = tfidfconverter.transform(X_convert).toarray()
    return X_convert


def decoupage_dataset(X_convert, y_data):
    """
    Réparition des données dans un set d'entrainement et un set de test pour vérifier l'efficacité du modèle
    entrée: X, np.ndarray fourni par la fonction conversion_sklearn; y, pandas.Series des labels (valeurs 0 ou 1) et indique si les tweets sont insultants(1) ou non (0)
    sortie: X et y découpés chacun un deux sous tableaux numpy et pandas.Series (respectivempent) d'entrainement et de test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X_convert, y_data, test_size=0.2, random_state=0)
    return (X_train, X_test, y_train, y_test)


def entrainement_modele(X_train, y_train):
    """
    Entrainement du modèle
    entrée: tableaux numpy X_train et y_train issus du découpage des tableaux précédents.
    sortie: objet RandomForest, capable d'analyser si un tweet est haineux ou non par la méthode objet.predict(tweet)
    Remarque: y_test est un pandas.Series et y_pred issus de classifier.predict(X_test) est un np.ndarray
    """
    classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
    classifier.fit(X_train, y_train)
    return classifier


## Tests ##

def test_creation_dataframe():
    X_data, y_data = creation_dataset('train.csv', 0, 500)
    assert type(X_data) == pandas.Series
    assert type(y_data) == pandas.Series
    assert 0 in y_data
    assert 1 in y_data


def test_preprocessing():
    X_data, y_data = creation_dataset('train.csv')
    L_tweets = preprocessing(X_data)
    assert type(L_tweets) == list
    assert type(L_tweets[0]) == str


def test_conversion_sklearn():
    X_data, y_data = creation_dataset('train.csv')
    L_tweets = preprocessing(X_data)
    X_convert = conversion_sklearn_fit_transform(L_tweets)
    assert type(X_convert) == np.ndarray


def test_decoupage():
    X_data, y_data = creation_dataset('train.csv')
    L_tweets = preprocessing(X_data)
    X_convert = conversion_sklearn_fit_transform(L_tweets)
    X_train, X_test, y_train, y_test = decoupage_dataset(X_convert, y_data)
    assert type(X_train) == np.ndarray
    assert type(X_test) == np.ndarray
    assert type(y_train) == pandas.Series
    assert type(y_test) == pandas.Series


## Evaluation du modèle ##

if __name__ == '__main__':

    # Creation du modèle de ML
    print("*Creation du dataset en cours* \n")
    X_data, y_data = creation_dataset('train.csv', 0, 4000)
    print("*Preprocessing en cours* \n")
    L_tweets = preprocessing(X_data)
    print("*Creation du modèle en cours* \n")
    X_convert = conversion_sklearn_fit_transform(L_tweets)
    X_train, X_test, y_train, y_test = decoupage_dataset(X_convert, y_data)
    classifier = entrainement_modele(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Affichage des matrices d'efficacité du modèle
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))

    # Sauvegarde dy modèle
    with open('./projet_w2/InsultBlock/insult_detector/train_data/text_classifier', 'wb') as picklefile:
        pickle.dump((classifier, vectorizer, tfidfconverter), picklefile)
