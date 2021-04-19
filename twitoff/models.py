"""SQLAlchemy User and Tweet models for out database"""
from flask_sqlalchemy import SQLAlchemy

# creates a DB Object from SQLAlchemy class
DB = SQLAlchemy()


# Making a User table using SQLAlchemy
class User(DB.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):
    """Keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    # id column
    text = DB.Column(DB.Unicode(300))
    # tweet text column - allows for emojis and other characters (only up to 300 characs)
    user_id = DB.Column(DB.BigInteger,
            DB.ForeignKey("user.id"), nullable=False)
            # user_id column (user that corresponds to specific tweet)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))
    # creates link between user and tweets

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
    