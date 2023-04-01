## Importations ##

import tweepy
from tweepy.streaming import StreamingClient
from tweets_collect.api_connection import twitter_setup
from credentials import *

# Fonctions

# Collecte des tweets (SEARCH)


def collect(word, language="fr", nb=100):
    """
    entrée: mot à rechercher, chaine de caractères
    sortie: objet tweepy qui contient tous les tweets
    """
    connexion = twitter_setup()
    tweets = connexion.search_tweets(word, lang=language, count=nb)
    return tweets


# Collecte des données users (USERS)
def collect_by_user(user_name, nb=100):
    """
    entrée: nom d'utilisateur de la personne recherchée. ATTENTION, il s'agit du nom précédé par @ sous le nom du compte twitter
    sortie: objet tweepy qui contient tous les tweets
    """
    connexion = twitter_setup()
    tweets = connexion.user_timeline(screen_name=user_name, count=nb)
    return tweets

# Recherche continue (STREAM)


class IDPrinter(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        # Passage heure d'hiver
        time = str(tweet.created_at)[11:19]
        heure = str(int(time[0:2]) + 1)
        T = list(time)
        T[0] = heure[0]
        T[1] = heure[1]
        time = ''.join(T)
        print(f"{time} : {tweet.text}")
        print("-"*130)

    # Cas d'un erreur
    def on_error(self, status):
        if str(status) == "420":
            print(status)
            print(
                "You exceed a limited number of attempts to connect to the streaming API")
            return False
        else:
            return True


def collect_by_streaming(mot_clef):
    """
    entrée: mot_clef à rechercher, chaine de carcatères sous forme de str
    sortie: flux de tweets continu (stream)
    """
    printer = IDPrinter(BEARER_TOKEN)

    # Clean up pre existing rules
    rule_ids = []
    result = printer.get_rules()
    for rule in result.data:
        rule_ids.append(rule.id)

    if (len(rule_ids) > 0):
        printer.delete_rules(rule_ids)
        printer = IDPrinter(BEARER_TOKEN)

    # Mise en place du streaming
    printer.add_rules(tweepy.StreamRule(mot_clef + " lang:fr"))
    # printer.add_rules(tweepy.StreamRule("-is:retweet"))
    printer.filter(tweet_fields="created_at")
    printer.sample()


# Avec des queries mots-clefs et hashtag définies dans un fichier


file_path_1 = './projet_w2/InsultBlock/tweets_collect/twitter_candidate_data/keywords_candidate_n.txt'
file_path_2 = './projet_w2/InsultBlock/tweets_collect/twitter_candidate_data/hashtag_candidate_n.txt'


def get_queries(candidate_name):
    """
    Generate and return a list of string queries for the search Twitter API from the file file_path_num_candidate.txt
    entrée: nom du candidat (après le @ dans le profil twitter) en chaine de caractères (str)
    sortie: une liste de queries (string) qui peuvent être utilisées par l'API tweepy
    """
    queries = []
    with open(file_path_1, 'r', encoding='utf-8') as f:
        # on utilise read().splitlines() à la place de readlines() pour éviter le caractère <\n> en fin de ligne
        Keywords = f.read().splitlines()
    with open(file_path_2, 'r', encoding='utf-8') as f:
        Hastags = f.read().splitlines()

    # Création des requetes keywords et hashtag liées aux candidats
    for i in Keywords:
        queries.append(candidate_name + " AND " + i)
    for j in Hastags:
        queries.append(candidate_name + " AND " + j)
    return queries


def get_tweets_queries(queries, number=100):
    """
    queries est une liste
    renvoie la liste des tweets T
    """
    T = []
    n = len(queries)
    for i in range(n):
        # On récupère les tweets associés aux queries
        tweets = collect(queries[i], "fr", number)
        for tweet in tweets:
            T.append(tweet)
    return T

# Twitts postés par la personne


def get_tweets_postedby(candidate_name, number=100):
    """
    entrée: chaine de caractère, prend le nom d'utilisateur de la personne (le nom après @ dans le prfil tweeter)
    sortie: liste de tweets (objets tweepy)
    """
    T = []
    tweets = collect_by_user(candidate_name, number)
    for tweet in tweets:
        T.append(tweet)
    return T

# Retweets aux tweets (nombre) de la personne:


def get_retweets(candidate_name):
    """
    entrée: chaine de caractère, prend le nom d'utilisateur de la personne (le nom après @ dans le prfil tweeter)
    sortie: N entier, nombre total de retweets cumulés sur tous les tweets
    """
    L = []
    tweets = collect_by_user(candidate_name)
    print(tweets)
    for tweet in tweets:
        L.append(tweet.retweet_count)
    N = sum(L)
    return N


# Réponses à un tweet:

def get_response(twit_id, user_name):
    """
    entrée: id du tweet ATTENTION en str, nom d'utilisateur de l'user qui a posté ce tweet en str
    sortie: ensemble des réponses au tweet dont l'id a été rentré (objet tweepy)
    """
    rep = []
    api = twitter_setup()
    tweets = tweepy.Cursor(
        api.search_tweets, q='to:'+user_name).items(10000)
    for tweet in tweets:
        # print(tweet)
        # print("\n")
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str == twit_id):
                rep.append((tweet))
    return rep


## Tests ##


def test_collect():
    L = collect("Bitcoin")
    assert L != None
    for k in L:
        assert type(k.text) == str


def test_collect_by_user():
    L = collect_by_user("EmmanuelMacron")
    assert L != None
    for k in L:
        assert type(k.text) == str


def test_get_queries():
    L = get_queries("EmmanuelMacron")
    assert L != None
    for k in L:
        assert type(k) == str
        assert "AND" in k


def test_get_tweets_queries():
    T = get_tweets_queries("EmmanuelMacron")
    assert T != None
    for k in T:
        assert type(k.text) == str


def test_get_tweets_postedby():
    Tweets = get_tweets_postedby("EmmanuelMacron")
    assert Tweets != None
    assert type(Tweets) == list
    assert len(Tweets) >= 0
    for k in Tweets:
        assert type(k.text) == str
        assert k.user.screen_name == "EmmanuelMacron"


def test_get_retweets():
    N = get_retweets("EmmanuelMacron")
    assert N != None
    assert type(N) == int
    assert N >= 0


## Execution du programme ##


if __name__ == '__main__':
    # collect_by_streaming("ethereum")

    # T = collect_by_user("GravereauxDev")
    # print(T[0])
    # R = get_response(T[0].id, "GravereauxDev")

    print("ok")
