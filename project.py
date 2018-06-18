#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Club, TeamPlayer, User

# Importing the Login session

from flask import session as login_session
import random
import string

# imports for gconnect

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# importing the login decorator

from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'
        ]['client_id']
APPLICATION_NAME = 'European Football Clubs'

engine = create_engine('sqlite:///footballclubs.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'
                                 ), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Obtain the authorization code

    code = request.data

    try:

        # upgrade the authorization code in credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade the authorization code'
                          ), 401)
        response.headers['Content-Type'] = 'application-json'
        return response

    # Checking whether the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps("Token's user ID doesn't match given user ID."
                          ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying whether the access tokin is valid or not.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("Token's client ID does not match app's."
                          ), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Access the token within the application

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                          ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Succesfully connected users',
                             200))

    # To get the User Info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # If the user exists ok, or make a new one

    print 'User email is' + str(login_session['email'])
    user_id = getUserID(login_session['email'])
    if user_id:
        print 'Existing user#' + str(user_id) + 'matches this email'
    else:
        user_id = createUser(login_session)
        print 'New user_id#' + str(user_id) + 'created'
    login_session['user_id'] = user_id
    print 'Login session is tied to :id#' + str(login_session['user_id'
            ])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 299px; height: 299px;border-radius:129px;- \
      webkit-border-radius:139px;-moz-border-radius: 139px;">'
    flash('you are now logged in as %s' % login_session['username'])
    print 'done!'
    return output


#  Functions are Written--Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email'
            ]).first()
    return user.id


# Get the user info

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


# Get the user id

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


# DISCONNECT - Revoke the current user's token and reset their login_session.

@app.route('/gdisconnect')
def gdisconnect():

    # for only disconnecting already connected User

    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected'
                                 ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is'
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'
                                 ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = \
            make_response(json.dumps('Failed to revoke token for given user.'
                          , 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('you have succesfully been logout')
        return redirect(url_for('viewClubs'))
    else:
        flash('you were not logged in')
        return redirect(url_for('viewClubs'))


@app.route('/club/<int:club_id>/team/JSON')
def clubTeamJSON(club_id):
    club = session.query(Club).filter_by(id=club_id).one()
    players = session.query(TeamPlayer).filter_by(club_id=club_id).all()
    return jsonify(TeamPlayers=[i.serialize for i in players])


@app.route('/club/<int:club_id>/team/<int:team_id>/JSON')
def teamPlayerJSON(club_id, team_id):
    Team_Player = session.query(TeamPlayer).filter_by(id=team_id).one()
    return jsonify(Team_Player=Team_Player.serialize)


@app.route('/club/JSON')
def clubsJSON():
    clubs = session.query(Club).all()
    return jsonify(clubs=[r.serialize for r in clubs])


# A page to show all my clubs
# Show all clubs

@app.route('/')
@app.route('/club/')
def viewClubs():
    clubs = session.query(Club).all()

    # return "This page will show all my clubs"

    return render_template('clubs.html', clubs=clubs)

# Edit a club
# You can only edit if you are logged in


@app.route('/club/<int:club_id>/edit/', methods=['GET', 'POST'])
def editClub(club_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedClub = session.query(Club).filter_by(id=club_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedClub.name = request.form['name']
            return redirect(url_for('viewClubs'))
    else:
        return render_template('editClub.html', club=editedClub)
    if Club.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this touristplace. please create your own team player in order\
        to edit.');}</script><body onload='myFunction()'>"

    # return 'This page will be for editing club %s' % club_id


# After logging in you can create your new clubs
# Create a new club

@app.route('/club/new/', methods=['GET', 'POST'])
def newClub():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newClub = Club(name=request.form['name'])
        session.add(newClub)
        session.commit()
        return redirect(url_for('viewClubs'))
    else:
        return render_template('newClub.html')

    # return "This page will be for making a new club"

# Edit a club
# You can only edit if you are logged in


@app.route('/club/<int:club_id>/edit/', methods=['GET', 'POST'])
def editClub(club_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedClub = session.query(Club).filter_by(id=club_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedClub.name = request.form['name']
            return redirect(url_for('viewClubs'))
    else:
        return render_template('editClub.html', club=editedClub)
    if editedClub.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this touristplace. please create your own team player in order\
        to edit.');}</script><body onload='myFunction()'>"

    # return 'This page will be for editing club %s' % club_id

# Page for Deleting a team player


@app.route('/club/<int:club_id>/team/<int:team_id>/delete',
           methods=['GET', 'POST'])
def deleteTeamPlayer(club_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    playerToDelete = \
        session.query(TeamPlayer).filter_by(id=team_id).one()
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        return redirect(url_for('showTeam', club_id=club_id))
    else:
        return render_template('deleteteamplayer.html',
                               player=playerToDelete)
    if playerToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this touristplace. please create your own team player in order\
        to delete.');}</script><body onload='myFunction()'>"

    # return "This page is for deleting team players %s" % team_id

# Page for Deleting a club
# Deletion can be done after Successfully logged in


@app.route('/club/<int:club_id>/delete/', methods=['GET', 'POST'])
def deleteClub(club_id):
    if 'username' not in login_session:
        return redirect('/login')
    clubToDelete = session.query(Club).filter_by(id=club_id).one()
    if request.method == 'POST':
        session.delete(clubToDelete)
        session.commit()
        return redirect(url_for('viewClubs', club_id=club_id))
    else:
        return render_template('deleteClub.html', club=clubToDelete)
    if Club.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this touristplace. please create your own team player in order\
        to delete.');}</script><body onload='myFunction()'>"

    # return 'This page will be for deleting a club %s' % club_id


# View can be offline
# Show Players in a club


@app.route('/club/<int:club_id>/')
@app.route('/club/<int:club_id>/team/')
def showTeam(club_id):
    club = session.query(Club).filter_by(id=club_id).one()
    players = session.query(TeamPlayer).filter_by(club_id=club_id).all()
    return render_template('team.html', players=players, club=club)

    # return 'This page is the menu for clubs %s' % club_id


# Page for Editing a team player
# Editing can't be done unless you logged in


@app.route('/club/<int:club_id>/team/<int:team_id>/edit', methods=['GET'
           , 'POST'])
def editTeamPlayer(club_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(TeamPlayer).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        if request.form['description']:
            editedPlayer.description = request.form['description']
        if request.form['price']:
            editedPlayer.price = request.form['price']
        if request.form['course']:
            editedPlayer.course = request.form['course']
        session.add(editedPlayer)
        session.commit()
        return redirect(url_for('showTeam', club_id=club_id))
    else:

        return render_template('editteamplayer.html', club_id=club_id,
                               team_id=team_id, player=editedPlayer)
    if Club.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized to\
        edit this touristplace. please create your own team player in order\
        to edit.');}</script><body onload='myFunction()'>"

    # return 'This page is for editing a team player %s' % team_id

# Page for creating a new team player
# Creation can be done if you are user


@app.route('/club/<int:club_id>/team/new/', methods=['GET', 'POST'])
def newTeamPlayer(club_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newPlayer = TeamPlayer(name=request.form['name'],
                               description=request.form['description'],
                               price=request.form['price'],
                               course=request.form['course'],
                               club_id=club_id)
        session.add(newPlayer)
        session.commit()

        return redirect(url_for('showTeam', club_id=club_id))
    else:
        return render_template('newteamplayer.html', club_id=club_id)

    return render_template('newTeamPlayer.html', club=club)

    # return 'This page is to make a new menu item for club %s'
    # %club_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

