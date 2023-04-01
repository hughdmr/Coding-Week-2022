## Importations ##

# Modules
from insult_detector.detecteur_v1 import detecteur_v1
from insult_detector.main_detector import detecteur
from tweets_collect.to_dataframe import to_dataframe
from tweets_collect.main_collect import *


# Import dataframe
data = to_dataframe('data_missile.json')
data_user = to_dataframe('data_sandrousseau.json')


## Fonctions ##


def ajout_colonnes(data):
    """
    entree: le dataframe initial
    sortie: le dataframe modifié
    """
    # Ajout de la colonne insulte
    data['insult'] = data['text'].apply(detecteur_v1)
    # Ajout de colonne 'jour' et heure
    """
    data['jour'] = data['created_at'].apply(lambda x: x[8:10])
    data['heure'] = data['created_at'].apply(lambda x: x[11:13])
    data['mois'] = data['created_at'].apply(lambda x: x[4:7])
    """
    return data


def nb_insultes(data):
    """
    Analyse d'opinion de la plateforme.
    entrée: dataframe pandas data
    sortie: nombres tweets qui sont des insultes et nombre qui le sont pas type int
    """
    pas_insultes = len(data[data['insult'] == False].index)
    insultes = len(data[data['insult'] == True].index)
    total = pas_insultes + insultes
    percentage = insultes/total
    return (insultes, total, percentage)


def drop_duplicate(L):
    """
    Supprime les doublons de L
    """
    return list(set(L))


def insult_jour(data):
    """
    entrée: dataframe pandas data
    sortie: nombres moyen d'insultes par jour dans le dataframe (float)
    """
    jours = drop_duplicate(data['jour'].values)
    nb_jours = len(jours)
    insulte = 0
    for jour in jours:
        insulte += len(data[data['jour'] == True].index)
    moy = insulte/nb_jours
    return moy


def insult_heure(data):
    """
    entrée: dataframe pandas data
    sortie: nombres moyen d'insultes par heure dans le dataframe (float)
    """
    heures = drop_duplicate(data['heure'].values)
    nb_heures = len(heures)
    insulte = 0
    for heure in heures:
        insulte += len(data[data['heure'] == True].index)
    moy = insulte/nb_heures
    return moy


def max_insultes(data):
    users = drop_duplicate(data['user.screen_name'].values)
    insulte_max = 0
    for user in users:
        nb_insulte = len(data[data['user.screen_name'] == user].index)
        if nb_insulte > insulte_max:
            insulte_max = nb_insulte
    return insulte_max


# Statistiques par utilisateur


def nb_user_insult(user_data):
    """
    entrée: dataframe des tweets d'un seul utilisateur
    sortie: nombre d'insultes total de l'user (int) + nb insultes moyen par jour (float)
    """
    nb_insultes = sum(user_data['insult'])
    return (nb_insultes)


def moy_insult_user(data):
    """
    entrée: dataframe des tweets
    sortie: nb d'insultes moy/heure/user, nb insultes moy/jour/user
    """
    users = drop_duplicate(data['user.screen_name'].values)
    nb_users = len(users)
    moy_user = nb_insultes(data)[0]/nb_users
    moy_jour = insult_jour(data)
    moy_heure = insult_heure(data)
    return (moy_user, moy_heure/nb_users, moy_jour/nb_users)

# Insultes par sujet abordé


def insult_subject(subject, nombre=100):

    data = main_subject(subject, nombre)
    nb_insultes = 0

    if len(data.index) > 0:
        for i in range(len(data.index)):
            nb_insultes += len(detecteur(data['text'][i]))

        ratio_insultes_subject = nb_insultes/len(data.index)

        return ratio_insultes_subject
    return 0


# Insultes par système d'exploitation pour un sujet donné

def lis_sysex(data):
    l = []
    for twindex in range(len(data.index)):
        l_sysex = [l[j][0] for j in range(len(l))]
        if data['source'][twindex].split(' ')[-1] not in l_sysex:
            l.append((data['source'][twindex].split(' ')[-1], 1))
        else:
            for j in range(len(l)):
                if data['source'][twindex].split(' ')[-1] == l[j][0]:
                    # print(l[j][1])
                    c = l[j][1] + 1
                    l[j] = (l[j][0], c)

    l_sysex = [l[j][0] for j in range(len(l))]
    l_nbtwi = [l[j][1] for j in range(len(l))]

    return (l_sysex, l_nbtwi)


def nb_insultes_par_sysex(sysex, data_name):
    data = to_dataframe(data_name)
    n = 0
    for twindex in range(len(data.index)):
        if data['source'][twindex].split(' ')[-1] == sysex:
            texte = data['text'][twindex]
            lang = data['lang'][twindex]
            L = detecteur(texte)
            i = 0
            lis = lis_sysex(data)
            for j in range(len(lis)):
                if sysex == lis[j][0]:
                    i = j
            n += len(L)/lis[1][i]
    return n

# RT et Like pour un tweet insultant par rapport à un autre tweet non insultant pour un user donné (twittos par exemple)


def creation_datasets(user_name, nombre):
    data = main_user(user_name, nombre)

    nb_tw_insultant = 0
    nb_tw_noninsultant = 0
    data_tw_insultant = []
    data_tw_noninsultant = []
    print(len(data.index))
    if len(data.index) > 0:
        for i in range(len(data.index)):
            if detecteur(data.iloc[i]['text']) == True:
                # print(det_insultes(data.iloc[i]['text']))
                nb_tw_insultant += 1

                data_tw_insultant.append(data.iloc[i])
            else:
                nb_tw_noninsultant += 1
                data_tw_noninsultant.append(data.iloc[i])

    nb_tw = min(nb_tw_insultant, nb_tw_noninsultant)
    data_tw_insultant = data_tw_insultant[:nb_tw]
    data_tw_noninsultant = data_tw_noninsultant[:nb_tw]

    return (pd.DataFrame(data_tw_insultant), pd.DataFrame(data_tw_noninsultant))


def moyenne_reaction(data):
    moy_retweet = 0
    moy_like = 0
    print(len(data.index))
    if len(data.index) > 0:
        for i in range(len(data.index)):
            moy_retweet += data.iloc[i]['retweet_count']
            moy_like += data.iloc[i]['favorite_count']
        return (moy_retweet/len(data.index), moy_like/len(data.index))
    else:
        return (0, 0)

## Tests ##


def test_nb_insultes():
    nb_insultes = nb_insultes(data)
    assert type(nb_insultes) == int


def test_insult_jour():
    moy = insult_jour(data)
    assert type(moy) == float


def test_max_insultes():
    moy = moy_insult_user(data)
    max = max_insultes(data)
    assert type(moy) == float
    assert type(max) == int
    assert max >= moy
