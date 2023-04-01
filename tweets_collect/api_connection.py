## Importations ##

import tweepy
from credentials import *


## Fonctions ##

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with an access keys provided in a file credentials.py
    sortie: l'objet authentified API
    """

    # Authentication and access using keys:

    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:

    api = tweepy.API(auth)
    return api


## Test ##

def test_twitter_setup():
    api = twitter_setup()
    assert api != None
