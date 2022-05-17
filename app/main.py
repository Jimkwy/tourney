from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from. import db

main = Blueprint('main', __name__)

#HTTP error route
@main.errorhandler(404)
def not_found(error):
	return render_template('misc/404.html'), 404

#main routes
@main.route('/', methods=['GET', 'POST']) 
@login_required
def index():

    #TODO

    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return redirect((url_for('main.index'))) #username=current_user.username)

@main.route("/lineup", methods=["GET", "POST"])
@login_required
def lineup():
    
    #TODO
    
    return render_template("main/lineup.html") #, tournament=Tournament, teams=Teams, games=Games, days=Days)

@main.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboard():

    #TODO



    return render_template("main/leaderboard.html") #, tournament=Tournament, teams=Teams, pagecolor=pagecolor)

@main.route("/gameboard", methods=["GET", "POST"])
@login_required
def gameboard():
    
    #TODO
    
    return render_template("main/gameboard.html", game=1) #, tournament=Tournament, game=Game, teams=Teams, vs=Vs)
    
@main.route("/rulebook", methods=["GET", "POST"])
def rulebook():
    
    #TODO
    
    return render_template("main/rulebook.html")

@main.route("/settings", methods=["GET", "POST"])
def settings():

    #TODO

    return render_template("main/settings.html")

@main.route("/faq")
def faq():
    
    #TODO
    
    return render_template("main/faq.html")
