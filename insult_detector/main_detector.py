## Importations ##

from insult_detector.detecteur_v1 import detecteur_v1
from insult_detector.detecteur_v2 import detecteur_v2
from insult_detector.detecteur_v3 import detecteur_v3
from insult_detector.cas_particuliers import insulte_cachee

## Fonctions ##


def detecteur(text):
    if detecteur_v1(text) or detecteur_v3(text) or insulte_cachee(text):
        return 1
    return 0

## Test ##


def test_detecteur():
    bool = detecteur('test')
    assert bool != None


if __name__ == '__main__':
    print(detecteur('jk'))
