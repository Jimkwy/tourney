from flask_login import UserMixin
from app import db

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# define base model


class Base(db.Model):

	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
	), onupdate=db.func.current_timestamp())

# Define User


class User(Base, UserMixin):

	__tablename__ = 'user'

	# Username
	username = db.Column(db.String(128), nullable=False, unique=True)

	# ID data: email & password
	email = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(128), nullable=False)

	# store users active/created tournaments to help with lookup and instancing
	tourney = relationship("tourney")
	tourney_num = db.Column(db.Integer)

	# TODO add colomns for user settings, actual name and overall settings (ex: color modes, advertising, etc)

    

# define tournament to keep track of overall tournaments and ownerships
class Tourney(Base):

	__tablename__ = 'tourney'

	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	name = db.Column(db.String(128))
	description = db.Column(db.Text)
	format = db.Column(db.Integer) #denotes the tournament style (elimination, double elimination, swiss, round-robin or no elimination)
	score_style = db.Column(db.Integer) #ranking by most/least score points or wins/losses/ties
	game_num = db.Column(db.Integer) #number of games to be played in the tournament
	games_played = db.Column(db.Integer)
	games_to_play = db.Column(db.Integer)

	#link to list of games for generating lineup/schedule page for interfacing
	lineup_id = relationship("Lineup")


# define schedule and relate them to the overall user, tournament and related games
class Lineup(Base):

	__tablename__ = 'lineup'

	#link parent tournament and user for easy lookup and linkage
	tourney_id = db.Column(db.Integer, db.ForeignKey('tourney.id'), nullable=False)
	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#digit denoting where each individual game lies in the overall lineup (IE: is it first, second last, etc)
	order = db.Column(db.Integer, nullable=False)

	game_name = db.Column(db.String(128), nullable=False)
	type = db.Column(db.Integer, nullable=False) #individual or team(VS)
	score_system = db.Column(db.Integer, nullable=False) #holes, points, duration, distance etc.
	rounds = db.Column(db.Integer, nullable=False) #how many rounds will this game be played
	num_players = db.Column(db.Integer) #number of players to be included in the game
	location = db.Column(db.String(256)) #brief description of the location of the game
	time = db.Column(db.String(128)) #user can input a date for when the game will be played
	description = db.Column(db.Text) #user submited description of the game and how it will be played
	win_value = db.Column(db.Integer) #allows the user to choose how much winning this sub-tournament will be valued at
	gameboard = relationship("Gameboard")
	players = relationship("Players")





# define players for use in the leaderboard and in generating profiles for each user including statistics, tournament history and otherwise
class Player(Base):

	__tablename__ = 'player'

	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	team = db.Column(db.Boolean, nullable=False)
	team_name = db.Column(db.String(128))
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
	player_name = db.Column(db.String(128), nullable=False)
	player_color = db.Column(db.String(32), nullable=False)


# define gameboard to keep track of scores for games in play and delete the entiries when game is completed
class Gameboard(Base):

	__tablename__ = 'gameboard'

#store custom and standardised rulesets created by users
class Rulebook(Base):

	__tablename__ = 'rulebook'

