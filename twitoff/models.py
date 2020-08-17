"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    """Example user data to play with."""
    austen = User(id=1, name='austen')
    elon = User(id=2, name='elonmusk')
    robert = User(id=3, name='robertdowneyjr')
    trump = User(id=4, name='donaldtrump')
    DB.session.add(austen)
    DB.session.add(elon)
    DB.session.add(robert)
    DB.session.add(trump)
    DB.session.commit()


def insert_example_tweets():
    """Example tweets data to play with."""
    elontweet = Tweet(id=1, text='When space travel becomes as common as air travel, '
                                 'the future of civilization will be assured',
                      user_id=2, user='elon')
    trumptweet = Tweet(id=2, text='WITCH HUNT!', user_id=4, user='trump')
    austentweet = Tweet(id=3, text='If you’re a university actually concerned about '
                                   'equality step one should be getting rid of legacy'
                                   ' admissions', user_id=1, user='austen')
    roberttweet = Tweet(id=2, text="Happy birthday to America's ass. The world's a "
                                   "better place, and I owe you a kiss on the cheek! "
                                   "@ChrisEvans", user_id=3, user='robert')
    DB.session.add(austentweet)
    DB.session.add(elontweet)
    DB.session.add(roberttweet)
    DB.session.add(trumptweet)
    DB.session.commit()
