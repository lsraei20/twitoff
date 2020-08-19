import tweepy


TWITTER_API_KEY = 'fazlckfftbDxNhMskeNb0WAfk'
TWITTER_API_KEY_SECRET = 'bP9uTMaD7BDRUGRACK8bmvAOHZKPVieRmk026fDrSIS6svE9gC'
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

user = 'kingjames'
twitter_user = TWITTER.get_user(user)

tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='Extended')
print(twitter_user.id)
