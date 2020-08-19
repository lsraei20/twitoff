"""Retrieve Tweets, embeddings, and persist in the database."""
from os import getenv
import tweepy
import basilica
from .models import DB, User, Tweet


TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)
b = basilica.Connection(getenv('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user an their Tweets, error if not a twitter user."""
    twitter_user = TWITTER.get_user(username)
    db_user = (User.query.get(twitter_user.id) or
               User(id=twitter_user.id, name=username))
    DB.session.add(db_user)
    # get tweets (focusing on primary not retweet or reply)
    tweets = twitter_user.timeline(count=200, exclude_replies=True,
                                   include_rts=False, tweet_mode='Extended')
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.text)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)
    DB.session.commit()


def insert_example_users():
    """Example data to play with."""
    add_or_update_user('austen')
    add_or_update_user('elonmusk')
    add_or_update_user('nasa')
    add_or_update_user('kingjames')
