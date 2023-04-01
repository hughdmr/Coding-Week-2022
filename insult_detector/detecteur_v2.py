## Importation ##

from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


## Fonctions Versions francaise (textblob_fr) ##

def sentiment_text(text):
    '''
    Fonction qui prend un  texte et renvoie sa polarité et son objectivité
    '''
    tweet = TextBlob(text, pos_tagger=PatternTagger(),
                     analyzer=PatternAnalyzer())
    sentiment = tweet.sentiment
    return sentiment


def sentiment_text_eng(text):
    '''
    Fonction qui prend un  texte et renvoie sa polarité et son objectivité
    '''
    tweet = TextBlob(text)
    sentiment = (tweet.sentiment.polarity, tweet.sentiment.subjectivity)
    return sentiment


def detect_negative_text(sentiment):
    '''
    Détecte si un texte est négatif et donc potentiellement contenir une insulte
    '''
    # Cette évaluation a été faite en comparant plusieurs phrases et mots contenant des insultes ou non.
    if sentiment[0] < 0 and sentiment[1] >= 0.4:
        return True
    elif sentiment[0] == 0 and sentiment[1] == 0:
        # l'analyse n'arrive pas à se faire
        return None
    else:
        return False

## Fonction Détecteur ##


def detecteur_v2(text, lang='fr'):
    '''
    Cette fonction utilise la version 1
    '''
    if lang == 'fr':
        if detect_negative_text(sentiment_text(text)):
            return True
        elif detect_negative_text(sentiment_text(text)) == None:
            return None
        else:
            return False
    elif lang == 'en':
        if detect_negative_text(sentiment_text_eng(text)):
            return True
        elif detect_negative_text(sentiment_text_eng(text)) == None:
            return None
        else:
            return False

## Tests ##


def test_detect_negative_text():
    '''
    Fonction qui teste sentiment_text et detect_negative_text
    '''
    text = "You are fucked up"
    assert sentiment_text_eng(text) == (-0.6, 0.7)
    assert detect_negative_text(text) == True
    text = 'Batard'
    assert sentiment_text(text) == (-0.7, 0.9)
    assert detect_negative_text(text) == True
    return

## Execution / Test ##


if __name__ == '__main__':
    a = (detecteur_v2("désolé"))
    print(a)
