"""Handles connection to Twitter API using Tweepy"""

from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"),
    getenv("TWITTER_API_KEY_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)


# loads word2vect Model
nlp = spacy.load("my_model/")

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

 
def add_or_update_user(username):
    """Takes username and pulls frorm Twitter API"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode='extended', 
            since_id=db_user.newest_tweet_id
            )
        
        if tweets:
            db_user.newest_tweets_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text[:300],
                vect=tweet_vector
            )
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    
    except Exception as e:
        print("Error Processing {}: {}".format(username, e))
        raise e
    
    else:
        DB.session.commit()


def update_all_users():
    Users = User.query.all()
    for user in Users:
        add_or_update_user(user.name)


