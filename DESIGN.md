DESIGN:

We coded our web based project using SQL, Python, Html, and Flask. We used the web microframework Flask because Flask allowed us to easily build a web based application using python and html. Python was our choice due to the Flask functionality in addition to python being coder friendly. Python has a lot of importable packages such as Flask-mail and time import which helped us easily solve problems when coding. The importable features made difficult tasks easier for the coder. We used SQL to store our user credentials and created events because SQL allows the coder to easily query specific data we may need. Also, SQL and python function together which worked perfectly for this project. Also, using Jinja which is enabled using Flask, we were able to communicate with HTML coded web pages with python. Jinja allowed us to pass form html inputs from the user to our python code in order to manipulate and check their input as well as put their events and data in our SQL databases. Flask, HTML, Python, and SQL all working together allowed Ricardo and I to build a comprehensive, detailed webpage - Crimson Connect. Please see below for specific function by function design considerations:

Tables in CrimsonConnect.db:
    These tables allow us to keep track of which users are registered for which events, individual user details, and details of events created.
    createdEvents
        nameEvent = name of event
        location = location of event
        description = what event entails
        startDate = start date and start time of event
        endDate = end date and end time of event
        creatorID = userID of who created the event
        eventID = unique id of event
        maxParticipants = max people able to attend
        currentParticipants = current registered people for event
    eventParticipants
        eventID - eventID of which user is registered for
        userID - userID who is registered for particular event
    users
        userID - unique id to user
        firstName - users first name
        lastName - users last name
        Username - user’s username
        email - user’s email
        hash - hash of user’s password
        numCreatedEvents - number of created events made by user
        numRegisteredEvents - number of events the user is registered for

Login
    The code that routes a user to the login page ensures that any user (logging in from the same computer) is logged out by performing “session.clear()”  which clears old session data. Thereafter, the python renders the login page when the user reaches it via a GET method. 
    The user is then prompted to enter their login credentials: username and password. We retrieve their answers via request.form.get. Our code then checks if the user left either the username or password fields blank. If they left either blank, the login page will be rendered again, with a red, dismissable error message (specific to what field they left blank). 
    In the case they did not leave any field blank, our code will then check if the user inputted a valid username (a username that is registered in our users table) by running a SQL query for the username in the “users” table.
    If the length of the list returned by the query is not equal to one, then the user inputted an invalid username and we render the login page again. If the user inputted a valid username but an incorrect password, we return the login page with the username field filled out for them. This is done by passing in the username they input as a parameter when rendering the “login.html” page. 
    If all of these checks pass, then the user is logged in and sent to the “logged in” homepage.

Logout
    When a user clicks the logout button at the top right of the website, our code ensures that the user is logged out by performing “session.clear()” which clears old session data. This keeps users logged out from accessing our resource because there is a login_required function before rendering any pages which allow users to interact with the application. After they click the logout button it sends the user to the “logged out” homepage.

Register User
    If the user reaches the registration page via a GET method our code will render the registration page with all of the registration information fields (first name, last name, username, Harvard email, password and confirmation) blank. This is made possible by our variable called check which is passed as a parameter when we render “registerUser.html”. If the check variable is equal to 1, then the registration fields are left blank. Furthermore, we flash a dismissible message that tells the user the requirements for password. 
    When the user submits registration information via a POST method our code checks for the following cases: first name, last name, or username left blank; username already registered in our database; Harvard email already registered; valid Harvard email; password and confirmation match. If any of the aforementioned checks do not pass, the registration page is rendered with only valid information that the user has already filled out and a dismissable (specific to failed check) error message. This is done by passing the valid information, such as username (one that is not already taken), first name and last name (if not left blank), and email (valid harvard email address), as parameters when rendering “registerUser.html”.
    Our code then creates a newly registered user into our “users” table by inserting their username, first name, last name, email, and a hash of their password. The table automatically creates the new user a unique “userID”
    The user is then “logged in” by creating a new session and redirected to the “logged” in homepage.

Create Event
    The “Create Event” page allows users to create public events. At the create events page users are required to provide information about “name of event”, “description of event”, “start date”, “end date", “location”, and “max number of participants”. 
    When the user submits event information via a POST method our code checks for the following cases: all fields are filled out; start date of the event has already passed; start date is before end date; number of active events created by user is 10 or less (to prevent spamming). If any of the cases do not pass a dismissable error message (specific to each case) is flashed. 
    We first check to make sure that all fields are filled out. If any field is not filled out we will render the “createEvents.html” page with fields that have already been filled out. This is done by passing the name of the event, the location of the event, and the description of the event, as parameters when rendering “createEvents.html”. If either the location, description, or name of the event was not filled out when the form was submitted, the input box will take the name of the placeholder we have in the “createEvents.html” file. We flash a message telling the user what is incorrect about their input
    We then create a variable called “combined date” which contains the current date and time in eastern time. This variable is used to check that the start date (of the event) is after the current date/time. If this check passes, there is a conditional statement that checks that the start date of the event is before the end date of the event. If either check doesn’t pass, the “createEvents.html” page is rendered with all other fields filled out with a flashed message. 
    If the above-mentioned checks pass we then run a SQL query to get the amount of active events (any events of which the start date has not passed) the user has. If the number of active events is more than 10, then the user cannot create a new event. This prevents the user from spam creating events. 
    If the user is allowed to create an event, then they will receive an email with all the information. This is done using the flask mail package we installed. Additionally, the new event is inserted into the “createdEvents” table with all of the event’s information.

Created Events
    The created events page allows users to see upcoming events that they have created. It is ordered by the date of the events - with the more recent events on top. Additionally, the page has the functionality for the user to cancel any event. 
    When the user clicks on the “Created Events” tab (GET method) our code gets the current date and time and puts it into a variable called full date. The full date variable is later used in a SQL query.
    We SQL query the “createdEvents” table that gets the following information for upcoming events that the user has created: name, location, description, start date, end date, current number of participants registered, and event id. We then pass this list as a parameter when rendering the “createdEvents.html” page and display all of the events as a table. 
    We also allow the user to cancel any event they have made. If the cancel button is clicked, a POST request is sent, along with the event ID for whatever event was cancelled. 
    Emails are sent to all of the registrants informing them of the cancelled event. This is done by getting a list of all the registrants' emails using SQL queries. Additionally, the user is sent an email informing them about the event they cancelled.
    Once emails are sent, the cancelled event is deleted from the “createdEvents” table and all instances of the event are removed from the “eventParticipants” table. This is done using SQL queries based on event id. 
    Lastly, the user is redirected back to their Created Events page.

Register for Events 
    The Register for Event page allows users to register for public events. The Register for Events page shows users upcoming events they can register for along with the following information:  “name of event”, “description of event”, “start date”, “end date”, and “current number of participants attending”
    When the user clicks on the “Register for Events” tab (GET method) our code gets the current date and time and puts it into a variable called full date. The “full date” variable is later used in a SQL query.
    To display only upcoming events (and not past events) the user can register for, we have a SQL query that selects events from “createdEvents'' where the start date has not passed “full date” (the current date and time) and the events that the user has not created. The following information: name, location, description, start date, end date, current number of participants registered, and event id is then put into a list. We then pass this list as a parameter when rendering the “registerForEvents.html” page and display all of the events as a table. 
    When the user registers for an event a POST request is sent, along with the event id for whatever event they want to attend. 
    After the POST request is sent, the code gets the current date and time and puts it into a variable called full date.This will be used for a SQL query that determines the number of active registrations the user has. 
    After obtaining the current date and time, a SQL query is performed in the “eventParticipant” table  to ensure that the user is not already registered for an event. If the user is already registered, an error message is flashed and the user is not allowed to register again. 
    If the above-mentioned check passes we then run a SQL query to get the amount of active registered events (any events of which the start date has not passed) the user has. 
    If the number of active events is more than 10, then the user cannot register for a new event. This prevents the user from possibly “fake registering” for multiple events. 
    We then insert into “eventParticipants” the event id of the event the user registered for and the user’s id. We also update the currentParticipants column in the “createdEvents” table for the event the user registered for.
    Lastly, if the user is allowed to register for an event, they will receive an email with all the information. This is done using the flask mail package we installed.

Registered Events
    The registered events page allows users to see upcoming events that they have registered for. It is ordered by the date of the events - with the more recent events on top. Additionally, the page has the functionality for the user to cancel any event they can no longer attend. 
    When the user clicks on the “Registered Events” tab (GET method) our code gets the current date and time and puts it into a variable called full date. The full date variable is later used in a SQL query.
    To display only upcoming events that the user has registered for we have a SQL query that selects events from the “createdEvents” table that the user has registered for, and the start date of registered events is past “full date” (current date). We then pass this list as a parameter when rendering the “registeredEvents.html” page and display all of the registered events as a table. 
    We also allow the user to cancel any event they have registered for. If the cancel button is clicked, a POST request is sent with the event id for whatever event they can no longer attend. 
    We update the “createdEvents” table to decrease the number of currentParticipants by one. This is done by using a SQL query to UPDATE the event in “createdEvents”.
    We then delete the instance of the user being registered for that event from the “eventParticipants” table. This is done by using a SQL query to DELETE based on event id and user id. 
    An email is sent to the registrant informing them of their cancellation. This is done by getting the registrant’s emails from the “users” table. We use a SQL query to select the emails, first name, and last name of the registrant. 
    Lastly, the user is redirected back to their Registered Events page.
