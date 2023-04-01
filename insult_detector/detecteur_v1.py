## IMPORTS ##
import pandas as pd
from textblob import TextBlob
from textblob import Word
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

## DEFINITIONS ##
chemin = './projet_w2/InsultBlock/insult_detector/'

# Dictionnaire des mots sémantiquement peu importants
dictionnaire_inutile_en = {"ourselves", "hers", "between", "yourself", "again", "there", "about", "once", "during", "out", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above",
                           "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "a", "by", "doing", "it", "how", "further", "was", "here", "than"}
dictionnaire_inutile_fr = {"m", "t", "s", "c", "entre", "encore", "là", "sur", "une fois", "pendant", "dehors", "avoir", "avec", "ils", "propre", "un", "être", "certains", "pour", "faire", "son", "votre", "tel", "dans", "de", "plus", "lui-même", "autre", "hors", "est", "suis", "es", "est", "sommes", "êtes", "or", "qui", "comme", "depuis", "lui", "chaque", "le", "leurs", "jusqu'à", " en dessous", "sont", "ces", "votre", "son", "à travers", "moi", "étaient", "elle", "plus", "lui-même",
                           "ce", "en bas", "devrait", "notre", "leur", "pendant", "au-dessus", "à", "notre", "avait", "avaient", "avais", "avions", "tout", "où", "avant", "eux",  "même", "et", "étais", "été", "était", "étaient", "étions", "étiez", "dans", "on", "alors", "parce", "que", "quoi", "pourquoi", "qui", "aviez", "sur", "donc", "peut", "maintenant", "sous", "il", "vous", "elle-même", "a", "juste", "ou", "aussi", "seulement", "moi-même", "lequel", "ceux", "après", "peu", "qui", "être", "si", "leur", "mon", "par", "faire", "il", "comment", "plus", "ici"}
dictionnaire_inutile = dictionnaire_inutile_en.union(dictionnaire_inutile_fr)

# Dictionnaire des mots abrégés
dictionnaire_jargon_fr = [("mrc", "merci"), ("bjr", "bonjour"), ("dr", "derien"), (
    "tlmt", "tellement"), ("jsp", "je sais pas"), ("cad", "c est à dire"), ("càd", "c est à dire"), ("ptn", "putain")]

# Dictionnaire des insultes
dictionnaire_insultes_en = {"fuck", "shit", "bullshit", "bollocks", "crap", "damn", "goddamn", "dumb", "bastard", "scumbag", "cunt", "pussy", "twat", "ass", "arse", "asshole", "arsehole", "asshat",
                            "badass", "slut", "bitch", "skank", "whore", "hooker", "faggot", "piss", "dick", "dickhead", "cock", "turd", "jeck", "dumbass", "bugger", "wanker", "tosser", "tramp", "nigger", "nigga", "negro"}

with open(chemin + 'insult.txt', 'r') as fichier:
    l = fichier.read().splitlines()

global dic_base
dic_base = [i for i in l]

m = [stemmer.stem(i) for i in l]

global dic_base_radical
dic_base_radical = [stemmer.stem(i) for i in l]

dictionnaire_insultes_fr = set(m)

## FONCTIONS NETTOYAGE ##


def nettoyage(txt):
    """str en entrée // str en sortie
    Enlever ponctuation, sauts de lignes, caractères spéciaux"""

    # On enlève les caractères spéciaux
    s = ""
    for j in txt:
        if (j.isalpha() or j.isspace()):
            s += j.lower()

    # On enlève les sauts de ligne
    b = s.replace('\n', '')
    return b


def nettoyage_semantique(txt):
    """str en entrée // list en sortie
    Enlever les mots sémantiquement peu importants.
    Remplacer le jargon"""

    # On fait les deux en même temps
    b = txt.split(' ')
    di = dictionnaire_inutile
    dj = dictionnaire_jargon_fr
    m = []
    n = ''

    for i in b:
        a = True
        for j in range(len(dj)):
            if i == dj[j][0]:
                n = dj[j][1]
                if i not in di:
                    a = False
                    m.append(n)
        if a == True:
            m.append(i)
    return m

# TextBlob : lemmatisation des mots (on radicalise)


def lemmatization(m, lang):
    """list et str en entrée // list en sortie
    Lemmatisation des mots avec TextBlob (on prend le radical)"""

    # On commence par lemmatiser (les noms, adjectifs, verbes en passant tout les mots au singulier avant)
    l = []
    for i in m:
        if i.isalpha():
            mot = TextBlob(i)
            a = Word(mot)
            b = mot.tags[0][1]
            if b in ('NN', 'VBD', 'VB', 'JJ', 'NNS', 'VBZ'):
                l.append(choisir_dic_et_txtblb(lang, mot, mot.tags[0][1])[1])
            else:
                l.append(i)

    # On a des problèmes de type. On change le type des mots TextBlob
    for i in range(len(l)):
        if type(l[i]) == type(TextBlob(Word('word'))):
            l[i] = l[i].tags[0][0]
    return l

## FONCTIONS DETECTEUR INSULTES V1 ##


def contains(small, big):
    """deux list en entrée // bool en sortie
    Renvoyer si une liste est contenue dans une autre (avec l'ordre des mots qui compte)"""

    for i in range(1 + len(big) - len(small)):
        if small == big[i:i+len(small)]:
            return True
    return False


def choisir_dic_et_txtblb(lang, mot1=TextBlob('home'), mot1_tag='NN'):
    """str en entrée // list en sortie
    Renvoyer le dictionnaire et le textblob à utiliser en fonction de la langue du texte"""

    l = [[dictionnaire_insultes_en, dictionnaire_insultes_fr], ['en', 'fr']]
    m = [[Word(mot1.words.singularize()[0]).lemmatize(
        mot1_tag), stemmer.stem(mot1.tags[0][0])], ['en', 'fr']]
    dic_lang = set()
    lem_lang = 0

    for j in range(len(l[0])):
        if l[1][j] == lang:
            dic_lang = l[0][j]
            lem_lang = m[0][j]

    return [dic_lang, lem_lang]


def list_insultes(txt, lang):
    """str en entrée // list en sortie
    Renvoyer la liste des insultes dans le texte d'entrée"""

    l = lemmatization(nettoyage_semantique(nettoyage(txt)), lang)
    ins = []
    dic_ins = choisir_dic_et_txtblb(lang)[0]

    for i in dic_ins:
        if len(i.split(' ')) <= len(l):
            if contains(i.split(' '), l):
                if lang == 'fr':
                    ins.append(dic_base[dic_base_radical.index(i)])
                else:
                    ins.append(i)
    return ins


def detecteur_v1(insulte, lang='fr'):
    """str en entrée // bool en sortie
    Renvoyer True si le groupe de mot est une insulte
    Renvoyer False si le groupe de mot n'est pas une insulte"""
    a = list_insultes(insulte, lang) != []
    if a:
        return 1
    else:
        return 0

## TESTS ##


def test_texte_insultes():
    texte_fr = "Bjr mesdames, messieurs !\n je m'appelle hugues et j'aime pas les bougnouls et les fils de pute"
    texte_en = "During this scene, I was hungry. Fuck you, i don't like bitches"  # v1 en anglais

    # Tests pour la fonction det_insultes
    assert set(list_insultes(texte_en, 'en')) == set(['fuck', 'bitch'])
    assert set(list_insultes(texte_fr, 'fr')) == set('bougnoul', 'pute')

    # Tests pour la fonction detecteur_V1
    assert detecteur_v1("pute", "fr") == True
    assert detecteur_v1("bonjour", "fr") == False
    assert detecteur_v1("shit", "en") == True
    assert detecteur_v1("hello", "en") == False


if __name__ == "__main__":
    print(detecteur_v1("Impact de foudre sur la tour Eiffel cet après vers 18h pendant le scintillement :) Pris simultanément avec 2 appareils. "))
