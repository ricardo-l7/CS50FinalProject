# CS50FinalProject
DOCUMENTATION:

Crimson Connect is a web page application that is specifically designed for Harvard Students looking to make friends. Crimson Connect only allows Harvard students to create accounts on the website. Once registered, students can post events and register for events that other Harvard students posted and will receive an email confirming registration. When posting an event, the user sets a maximum participant amount, and our site does not allow more than that set number of registrants for that event.  However, if you can no longer go, don’t worry. You can easily cancel registered and created events with a click of a button - under the created and registered events respective tabs. After cancelling an event as a creator, every registrant will receive an email informing them of the event cancellation. Furthermore, if you cancel as a registrant, you will receive a confirmation email of that cancellation. Crimson Connect promotes engagement amongst the student body, and our mission is to foster community and friend making in the Harvard community.

To run our project, the user needs to upload our files of code to vs code space which we used for all of the CS50 problem sets. Within the final project directory (cd project), the user needs to execute the following commands in order to install the packages you need in addition to the packages CS50 has given us.

Packages specifically to install in the terminal for this project : pip install Flask-Mail, pip install -U python-dotenv, pip install validate_email, pip install py3dns

In case of a package error, please see the view of all packages we have on our account-  files (piplist_1.png and piplist_2.png) within the project folder of our submission. I assume we may have installed packages over the past couple of months that you may not have installed on our accounts.

In order for the emails to work, you need to create a .env file. The .env file is an encrypted file that contains the username and password to the gmail account associated with our project we created. We have a .env to secure our data so that our sensitive data is not in our source code. To do so, navigate to the cd project directory. Once there execute the command,
code .env . This will display the file. Within the file, the first line should be

MAIL_DEFAULT_SENDER = crimsonconnectboard@gmail.com
MAIL_USERNAME = crimsonconnectboard@gmail.com
MAIL_PASSWORD = Finalproject123!

Please see the envExample.png file for a visual picture of what the env file should look like.

Once the packages are installed and the .env file is created, you should be able to run. Execute the command, flask run, to run the program within the project directory. Once the instance is created, the user will need to open the link from the terminal window in vscode in a separate browser.

After opening up the application in a different tab, you need to register an account. To register, click the register tab in the top right corner. All fields must be filled out and importantly you must use your harvard email (...@college.harvard.edu) when registering. Our code confirms that all fields are filled out and the email is a Harvard email before creating the user’s account. Once registered, you will receive an email confirming registration.

After registering, you will be logged in and you can navigate the tabs(register for events, create events, created events, and registered events). To create an event, navigate to the create events tab, and fill out all of the fields of the form, and the start date must be before the end date. There are many checks to ensure the event is valid and accurate such as time considerations. However, if there is a typo, we will render the form with your correct results in order to make the process quicker and more user friendly. After registering for an event (register for events tab), the user can cancel their registration. To do so, navigate to the registered events tab and click cancel on the respective event. The user will receive an email for all registration confirmations for events, for user cancelled events, and for creator cancellations of posted events. Once done, you can log out of your account(tab top right corner) and easily log back in with your username and password created.

Typical Questions:

What to do if I run into an error when running? Please confirm you have every package downloaded on our account. If the error is email related, please confirm you created a .env file and the username and password are correct.

How do you prevent non Harvard email from registering? We require a particular pattern within our html in order to submit a form, and then check via an imported class if the email is valid. If the email is an invalid Harvard email, we prevent the user from registering. 

Why did we use the .env file instead of hardcoding email and password into source code? We did this to maintain security on the email we created. We do not want sensitive information within our code and accessible to the public.

Where do we store user information and created event information?
We store all information within three SQLite created tables within our database that we created: CrimsonConnect.db. We have a users table which stores characteristics of each user, a created events table which stores each unique created events, and an event participants table which maps registrants to each event.

In the case of persistent errors, feel free to call Zach Stack at (708)-378-8216 or email  at zstack@college.harvard.edu at any time or Ricardo Linares at (708)-906-5722 or email at ricardolinares@college.harvard.edu

Link to youtube video - https://youtu.be/aV-95HIy7MI
