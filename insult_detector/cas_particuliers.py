## Fonctions ##

chemin = './projet_w2/InsultBlock/insult_detector/'
caracteres_speciaux = '*!%.^-'
remplacement = {'0': 'o', '3': 'e', '1': 'l'}
voyelles = 'aeiouy'


def creation_liste(nom_fichier):
    """
    Crée une liste d'insultes
    Entrée: insult.txt
    Sortie: liste de string (insultes)
    """
    with open(chemin + nom_fichier, 'r') as fichier:
        insultes = list(fichier.read().splitlines())
    return insultes


def nettoyage_texte(text):
    """
    remplace les caractères d'imitation
    supprime les voyelles redoublées qui trompent la liste
    entrée: chaine de caractère/string
    sortie: chaine de caractère épurée
    """
    # Remplacement des caractères d'imitation comme 0 par o ou 3 par e
    for i in remplacement.keys():
        if i in text:
            text.replace(i, remplacement[i])
    # Supression des voyelles redoublées
    for i in voyelles:
        if i in text:
            L_text = list(text)
            # On calcule la première occurence de la voyelle
            index_0 = L_text.index(i)
            index = index_0
            while (index+1 < len(L_text)) and (L_text[index+1]) == i:
                index += 1
            L_text = L_text[:index_0+1] + L_text[index+1:]
            text = ''.join(L_text)
    return text


def insulte_cachee(text):
    """
    entrée: text de type str
    sortie: boléen True si c'est une insulte cachée, False sinon
    """
    text = nettoyage_texte(text)
    insultes = creation_liste('insult.txt')
    if text in insultes:
        return (True, text)
    for insulte in insultes:
        if len(insulte) == len(text):
            incrementeur = 0
            for i in range(len(insulte)):
                if (text[i] == insulte[i]) or (text[i] in caracteres_speciaux):
                    incrementeur += 1
            if incrementeur == len(insulte):
                return (True, insulte)
    return False

## Tests ##


def test_creation_liste():
    L = creation_liste('insult.txt')
    assert L != None
    assert 'con' in L


def test_nettoyage_texte():
    result = nettoyage_texte("puuuuuuuute")
    assert result == 'pute'


def test_insulte_cachee():
    bool = insulte_cachee('conn**d')[0]
    assert bool == True
    bool = insulte_cachee('bonjour')
    assert bool == False
