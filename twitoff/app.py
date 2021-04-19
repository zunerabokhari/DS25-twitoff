"""This is what brings the application together"""

from flask import Flask, render_template
from .models import DB, User


# creates application
def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3" 
    # makes this database in this repo, configuring this app to have this DB
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # if you dont set this to false you'll see a running log of modifications

    DB.init_app(app)
    # initializes the app that was already defined in documentation
   
    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        insert_example_tweets
        return render_template('base.html',
                                title='home',
                                users=User.query.all())
                            # this passes a query so when we call users we get all users
                            # without us having to write a sql query bc of sqlalchemy

    @app.route('/goodbye')
    def goodbye():
        return "Goodbye, Twitoff!"
    
    return app


def insert_example_users():
# inserts hypothetical users that we've made 
    zunera = User(id=1, name="Zunera")
    elon = User(id=2, name="Elon")
    DB.session.add(zunera)
    DB.session.add(elon)
    DB.session.commit() 

def insert_example_tweets():
    zunera = Tweet(id=1, text="Hi, my name is Zunera!", user=Zunera)
    elon = Tweet(id=2, text="Hi, my name is Elon Musk!", user=Elon)