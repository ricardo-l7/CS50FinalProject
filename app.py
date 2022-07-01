import os
import re

import time
import pytz
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_mail import Mail, Message
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from validate_email import validate_email


from helpers import apology, login_required
from datetime import timedelta, date, datetime


# Configure application
app = Flask(__name__)


app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///CrimsonConnect.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get the username and the password from the login POST request
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if (not username):
            flash("Must input a username!")
            return render_template("login.html")

        # Ensure password was submitted and return form with username filled out
        if (not password):
            flash("Must input a password!")
            return render_template("login.html", username = username)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists 
        if (len(rows) != 1):
            flash("Invalid username")
            return render_template("login.html")

        # Ensure password mathces username and return form with username filled out
        elif (not check_password_hash(rows[0]["hash"], password)):
            flash("Invalid password")
            return render_template("login.html", username=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userID"]

        # Redirect user to logged-in home page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/registerUser", methods=["GET", "POST"])
def registerUser():
    """Register user"""

    # Render register page with blank  values so that we can later fill out the form with valid information for user
    if request.method == "GET":
        check = True
        flash("Password must be at least 8 characters long and contain at least 1 capital and 1 lowercase letter and a number")
        return render_template("registerUser.html", check = check)

    if request.method == "POST":

        # get information from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")

        # Check if firstname is left blank and returns the form with filled out valid information
        if (firstName == ""):
            flash("Please type in your first name")
            return render_template("registerUser.html", username = username, lastName = lastName, email = email)

        # Check if last name is left blank and returns the form with filled out valid information
        if (lastName == ""):
            flash("Please type in your last name")
            return render_template("registerUser.html", username = username, firstName = firstName, email = email)

        # Check if username is left blank and returns the form with filled out valid information
        if (username == "" ):
            flash("Must input a username!")
            return render_template("registerUser.html", firstName = firstName, lastName = lastName, email = email)

        # Check if username already exists and returns the form with filled out valid information
        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            flash("Username already taken!")
            return render_template("registerUser.html", firstName = firstName, lastName = lastName, email = email)

        # Check if email was already registered and returns the form with filled out valid information
        if len(db.execute("SELECT email FROM users WHERE email = ?", email)) > 0:
            flash("Email has already been registered in the database!")
            return render_template("registerUser.html", username = username, firstName = firstName, lastName = lastName)

        # Check if email is valid and returns the form with filled out valid information
        is_valid = validate_email(email,verify=True)
        if (is_valid != True):
            flash("Must be valid Harvard email")
            return render_template("registerUser.html", username = username, firstName = firstName, lastName = lastName)

        # Check if confirmation and password match and returns the form with filled out valid information
        if (confirmation != password):
            flash("Password and Confirmation must match!")
            return render_template("registerUser.html", username = username, firstName = firstName, lastName = lastName, email = email)

        # Hash password to put into database
        hashPassword = generate_password_hash(password)

        # Insert username, hashed password, email, firstName, lastName into database
        db.execute("INSERT INTO users (username, email, hash, firstName, lastName) VALUES(?, ?, ?, ?, ?)", username, email, hashPassword, firstName, lastName)

        # Send the user a email
        message = Message("Thank you for joining Crimson Connect! You are officially registered", recipients=[email])
        message.html = render_template("registrationEmail.html",firstName=firstName, lastName=lastName)
        mail.send(message)

        # Query database for username that was just put in
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userID"]

        # Redirect user to home page
        return redirect("/")


@app.route("/createEvent", methods=["GET", "POST"])
@login_required
def createEvent():

    if request.method == "GET":
        # Render template page
        return render_template("createEvents.html")

    if request.method == "POST":
        # Get all the form information that the user filled out
        event = request.form.get("eventName")
        description = request.form.get("eventDescription")
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        location = request.form.get("location")
        participants = request.form.get("participants")

        # Get current time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        datetime_NY = datetime_NY.strftime("%H:%M")

        # Check that all fields are filled out
        if (event == "" or description == "" or location == "" or participants == "" or endDate == "" or startDate == ""):
            flash("All fields must be filled out!")
            return render_template("createEvents.html", event=event, description=description, location=location)

        # Get current date
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")

        # Combine the current date and current time
        combinedDate = todayDate + "T" + datetime_NY

        # Ensure that the event's start date and time is later tan the current date and time
        if(startDate < combinedDate):
            flash("Event must be today or after today")
            return render_template("createEvents.html",event=event, description=description, location=location)

        # Ensure that the event's start date is before the event's end date
        if (startDate > endDate):
            flash("End Time must be after Start Time")
            return render_template("createEvents.html",event=event, description=description, location=location)

        # Get the current user's first and last name 
        user = db.execute("SELECT email, firstName, lastName FROM users WHERE userID = ?", session["user_id"])
        firstName = user[0]["firstName"]
        lastName = user[0]["lastName"]

        # Get the current number of active created events the user has
        listActiveEvents = db.execute("SELECT COUNT (DISTINCT eventID) as activeEvent FROM createdEvents WHERE startDate >= ? AND creatorID = ?", combinedDate, session["user_id"])
        activeEvents = listActiveEvents[0]['activeEvent']

        # Make sure that the user cannot make more than 10 events that are active (to get rid of possible spamming)
        if (activeEvents > 9):
            flash("Cannot have more than five active events at one time")
            return redirect("/createdEvents")

        # Send the current user an email about the event they created 
        message = Message("Event Created", recipients=[user[0]['email']])
        message.html = render_template("createdEventsEmail.html",firstName=firstName, lastName=lastName, 
        event=event,description=description,startDate=startDate,endDate=endDate,location=location, participants=participants)
        mail.send(message)

        # Insert new event into database
        db.execute("INSERT INTO createdEvents (creatorID, startDate, endDate, description, location, maxParticipants, currentParticipants, nameEvent) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            session["user_id"], startDate, endDate, description, location, participants, 0, event)
        
        # Redirect to page showing created events
        return redirect("/createdEvents")


@app.route("/createdEvents", methods=["GET", "POST"])
@login_required
def createdEvents():

    if request.method == "GET":
        # get Todays date and format 
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")
        tz_NY = pytz.timezone('America/New_York')
        # get eastern timezone time
        datetime_NY = datetime.now(tz_NY)
        datetime_NY = datetime_NY.strftime("%H:%M")
        
        # concatenate string with T for consistent formatting
        fullDate = todayDate + "T" + datetime_NY
        
        # select all user created events
        createdEvents = db.execute("SELECT startDate, endDate, description, location, currentParticipants, nameEvent, eventID FROM createdEvents WHERE creatorID = ? AND startDate >= ? ORDER BY startDate", session["user_id"], fullDate)
        return render_template("createdEvents.html", createdEvents=createdEvents)

    #to check if the user wants to cancel an event they created
    if request.method == "POST":
        # get the event id for which the event they cancelled
        id = request.form.get("eventID")

        # get the cancelled event's details as well as all of the users who registered for the event
        userInfo = db.execute("SELECT email, firstName, lastName FROM users WHERE userID IN (SELECT registrantID FROM eventParticipants WHERE eventID = ?)",id)
        event = db.execute("SELECT startDate, endDate, description, currentParticipants, nameEvent, eventID,location FROM createdEvents WHERE eventID = ?", id)

        # loop thru all registrant's emails and send cancelled email to them
        for row in userInfo:
            message = Message("Cancelled Event Registration", recipients=[row['email']])
            message.html = render_template("cancelledEventEmailForRegistrant.html", firstName = row['firstName'], lastName = row['lastName'],startDate=event[0]['startDate'], endDate= event[0]['endDate']
            ,description=event[0]['description'],nameEvent= event[0]['nameEvent'],location= event[0]['location'],
            currentParticipants = event[0]['currentParticipants'])
            mail.send(message)
        
        #get creator info and send confirmation of cancelled email to creator
        creatorInfo = db.execute("SELECT email, firstName, lastName FROM users WHERE userID = ?", session["user_id"])
        message = Message("Cancelled Event Registration", recipients=[creatorInfo[0]['email']])
        message.html = render_template("cancelledEventEmailForCreator.html", firstName = creatorInfo[0]['firstName'], lastName = creatorInfo[0]['lastName'],startDate=event[0]['startDate'], endDate= event[0]['endDate']
            ,description=event[0]['description'],nameEvent= event[0]['nameEvent'],location= event[0]['location'],
            currentParticipants = event[0]['currentParticipants'])
        mail.send(message)

        # delete event from created events DB and instances of event from eventParticipants
        db.execute("DELETE FROM createdEvents WHERE creatorID = ? AND eventID = ?", session["user_id"], id)
        db.execute("DELETE FROM eventParticipants WHERE eventID = ?", id)

        #redirect to created events
        return redirect("/createdEvents")

@app.route("/registerForEvent", methods=["GET", "POST"])
@login_required
def registerForEvent():
    if request.method == "GET":

        # get Todays date and format 
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")

        # get eastern timezone time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        datetime_NY = datetime_NY.strftime("%H:%M")

        # concatenate string with T for consistent formatting
        fullDate = todayDate + "T" + datetime_NY

        # select all active events
        createdEvents = db.execute("SELECT startDate, endDate, description, currentParticipants, nameEvent, eventID FROM createdEvents WHERE creatorID != ? AND startDate >= ? AND currentParticipants < maxParticipants ORDER BY startDate", session["user_id"], fullDate)

        # render register for event page
        return render_template("registerForEvent.html", createdEvents=createdEvents)

    if request.method == "POST":

        # get Todays date and format 
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")

        # get eastern timezone time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        datetime_NY = datetime_NY.strftime("%H:%M")

        # concatenate string with T for consistent formatting
        fullDate = todayDate + "T" + datetime_NY

        # get id from form
        id = request.form.get("eventID")
        
        # select user id if already registered
        eventParticipants = db.execute("SELECT * FROM eventParticipants WHERE eventID = ? AND registrantID = ?", id, session["user_id"])

        # check if user in event participants
        if (len(eventParticipants) == 1):
            # flash message since already registered
            flash("Already Registered")
            return redirect("/registerForEvent")

        # query count for user active events
        listActiveRegisteredEvents = db.execute("SELECT COUNT (DISTINCT eventID) as activeEvent FROM eventParticipants WHERE eventID IN (SELECT eventID FROM createdEvents WHERE startDate > ?) AND registrantID = ?", fullDate, session["user_id"])
        activeEvents = listActiveRegisteredEvents[0]['activeEvent']
        
        # check if active events over 10, index starts at 0
        if (activeEvents > 9):
            # flash message
            flash("Cannot be registered for more than 10 events at one time")
            return redirect("/registeredEvents")

        #Query values needed for emails
        event = db.execute("SELECT startDate, endDate, description, currentParticipants, nameEvent, eventID,location FROM createdEvents WHERE eventID = ?", id)
        
        #insert and update tables for new registrant
        db.execute("INSERT INTO eventParticipants (registrantID, eventID) VALUES(?,?)", session["user_id"], id)
        db.execute("UPDATE createdEvents SET currentParticipants = currentParticipants + ? WHERE eventID = ?", 1, id)

        # generate successfully registered email
        userInfo = db.execute("SELECT email,firstName,lastName FROM users WHERE userID = ?", session["user_id"])
        message = Message("Registered for Event", recipients=[userInfo[0]['email']])
        message.html = render_template("registeredForEventEmail.html", firstName = userInfo[0]['firstName'], lastName = userInfo[0]['lastName'],startDate=event[0]['startDate'], endDate= event[0]['endDate']
        ,description=event[0]['description'],nameEvent= event[0]['nameEvent'],location= event[0]['location'],
        currentParticipants = event[0]['currentParticipants'])
        mail.send(message)

        # redirct to registered events page
        return redirect("/registeredEvents")

@app.route("/registeredEvents", methods=["GET", "POST"])
@login_required
def registeredEvents():

    if request.method == "GET":

        # get Todays date and format 
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")

        # get eastern timezone time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        datetime_NY = datetime_NY.strftime("%H:%M")

        # concatenate string with T for consistent formatting
        fullDate = todayDate + "T" + datetime_NY

        # select all active events user registered for
        registeredEvents = db.execute("SELECT * FROM createdEvents WHERE eventID IN (SELECT eventID FROM eventParticipants WHERE registrantID = ?) AND startDate > ? ORDER BY startDate", session["user_id"], fullDate)

        # render registered events template
        return render_template("registeredEvents.html", registeredEvents=registeredEvents)

    if request.method == "POST":
        # get event ID from form
        id = request.form.get("eventID")

        # delete user from eventParticipants and update the currentParticipants of an event
        db.execute("DELETE FROM eventParticipants WHERE registrantID = ? AND eventID = ?", session["user_id"], id)
        db.execute("UPDATE createdEvents SET currentParticipants = currentParticipants - ? WHERE eventID = ?", 1, id)

        # get characteristic of user for email cancellation
        event = db.execute("SELECT startDate, endDate, description, currentParticipants, nameEvent, eventID,location FROM createdEvents WHERE eventID = ?", id)
        userInfo = db.execute("SELECT email,firstName,lastName FROM users WHERE userID = ?", session["user_id"])

        # generate email for cancelled event registration
        message = Message("Cancelled Event Registration", recipients=[userInfo[0]['email']])
        message.html = render_template("cancelledEventEmailRegistrant.html", firstName = userInfo[0]['firstName'], lastName = userInfo[0]['lastName'],startDate=event[0]['startDate'], endDate= event[0]['endDate']
        ,description=event[0]['description'],nameEvent= event[0]['nameEvent'],location= event[0]['location'],
        currentParticipants = event[0]['currentParticipants'])
        mail.send(message)

        # redirect to registered events
        return redirect("/registeredEvents")


@app.route("/")
def homePage():
    # render homepage
    return render_template("homepage.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
