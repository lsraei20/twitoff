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
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user an their Tweets, error if not a twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # get tweets (focusing on primary not retweet or reply)

        tweets = twitter_user.timeline(count=200, exclude_replies=True,
                                       include_rts=False, tweet_mode='Extended',
                                       since_id=db_user.newest_tweet_id, page=1)
        # page = 1
        # while len(tweets) < 200:
        #     page += 1
        #     temp = twitter_user.timeline(count=200, exclude_replies=True,
        #                                  include_rts=False, tweet_mode='Extended',
        #                                  since_id=db_user.newest_tweet_id, page=page)
        #     tweets = tweets + temp

        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.text, embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()


def insert_example_users():
    """Example data to play with."""
    add_or_update_user('elonmusk')
    add_or_update_user('realDonaldTrump')
