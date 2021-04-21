"""This is what brings the application together"""

from os import getenv
from flask import Flask, render_template
from .models import DB, User
from .twitter import update_all_users, add_or_update_user

# creates application
def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI") 
    # makes this database in this repo, configuring this app to have this DB
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # if you dont set this to false you'll see a running log of modifications
    DB.init_app(app)
    # initializes the app that was already defined in documentation
  
    @app.route('/')
    def root():
        """At end point '/'"""
        return render_template('base.html', title='home', users=User.query.all())
                            # this passes a query so when we call users we get all users
                            # without us having to write a sql query bc of sqlalchemy

    @app.route('/update')
    def update():
        """updates each user"""
        update_all_users()
        return render_template('base.html', title='Users Updated!', users=User.query.all())

    @app.route('/reset')
    def reset():
        """Reset DB using drop_all()"""
        DB.drop_all()
        DB.create_all()
        add_or_update_user("elonmusk")
        add_or_update_user("AOC")
        return render_template('base.html', title='RESET', users=User.query.all())
    
    return app
