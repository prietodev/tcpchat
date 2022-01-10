------------------------------------------------------------------------------
                                 Final Project                                
------------------------------------------------------------------------------

Name: Daniel Prieto
Course: CS3130 Winter 2020
Date: 2021-04-23

------------------------------------------------------------------------------
                                  Description                                 
------------------------------------------------------------------------------

This program is a mix of many concepts learned throughout the year in multiple
courses. The program consists of a multi-threaded TCP-based server and a 
graphical client. The program makes use of the SQLite database to store users,
messages, and files. The client consists of many Tkinter frames loaded together
at the start and updated as the user presses a REFRESH button.

Essentially the program is a chat system that uses requests and replies 
exchanged through a socket. The user can log in and use the chat system or they
can see whos online before signing in. Everything goes through the server and
then goes through the database. The user can send messages and files. The
user can also see who is online once they are logged in. The user is 
able to see other user's profiles. Everything is labeled with buttons and 
labels for the textfields and should be easy to navigate.


Files included:
---------------
server.py
client.py
database.lite
README.txt
zen_utils.py

------------------------------------------------------------------------------
                                   Protocol                                   
------------------------------------------------------------------------------

All of the requests and replies are wrapped in a pickle for serialization.
The requests and replies are formatted in a header and a payload

Format:
['header', b'payload'];
Header is a string and payload is a array of bytes
The list is always followed by a delimeter, a semi-colon

Requests:
----

['101>LOGIN>username>password', b'']
Checks username and password and sets user status to online in SQLite database

['104>LOGOUT>username', b'']
Sets user status to offline in SQLite database

['200>WHOISON', b'']
Asks server which users and online and offline

['300>SENDMSG>destination>source>messages', b'']
Sends a message to the desired user

['303>RETRIEVEMSG>user', b'']
Retrieve messages for a particular user

['306>SENDFILE>destination>source>file_name', b'file']
Sends a file to the desired user. The file is in the payload formatted as an
array of bytes

['309>RETRIEVEFILE>user', b'']
Retrieve files for a particular user

['400>PROFILE>user', b'']
Retrieve profile attributes for a particular user 

Replies:
----
['500>INVALID>REQUEST', b'']
Should never get this reply, but it is there incase no valid request is
inputted

['101>LOGIN>SUCCESS', b'']
If the user successfully logs in, the server replies with this message

['102>LOGIN>FAIL', b'']
If the user does not manage to log in, the server replies with this message

['104>LOGOUT>SUCCESS', b'']
If the user successfully logs out, the server replies with this message

['105>LOGOUT>FAIL', b'']
If the user does not manage to log out, the server replies with this message`

['201>OFFLINE>users>ONLINE>users', b'']
List of users offline and online

['202>WHOISON>FAIL', b'']
The WHOISON request failed

['301>SENDMSG>SUCCESS', b'']
When a message is successfully sent to an user, the server replies with this
message

['302>SENDMSG>FAIL', b'']
If a message couldn't be sent, the server replies with this message

['304>RETRIEVEMSG>SUCCESS>messages', b'']
If a message is retrieved succesfully, the server replies with this message

['305>RETRIEVEMSG>FAIL', b'']
If a message couldn't be retrieved, the server replies with this message

['307>SENDFILE>SUCCESS', b'']
If a file is sent successfully, the server replies with this message

['308>SENDFILE>FAIL', b'']
If a file couldn't be sent, the server replies with this message

['310>RETRIEVEFILE>SUCCESS>sources>file_names', b'files']
If a file is retrieved successfully, the server replies with this message. The
sources and file_names are separated by commas and the files are separated by
|*|

['311>RETRIEVEFILE>FAIL', b'']
If a file was not able to be retrieved, the server replies with this message

['401>PROFILE>SUCCESS>fname>lname>email>phone>department', b'']
If a profile was queried successfully, the server replies with this message

['402>PROFILE>FAIL', b'']
If a profile could not be queried, the server replies with this message

------------------------------------------------------------------------------
                                  Limitations                                 
------------------------------------------------------------------------------

All of the users are hardcoded into the program. The way I wrote my program I
was also limited to 1 frame per window. Limiting me in the way I can line up
the columns. If I could have figured out how to implement this, I would have
lined up my smaller buttons (the plain ones) side by side.

This program is also limited in the way that it can only communicate python
to python because of the way the data is serialized before sending it.

------------------------------------------------------------------------------
                              Run Instructions                                
------------------------------------------------------------------------------

Terminal:
----
Type    python3 server.py host              to stat the server application
    eg. python3 server.py localhost

Type    python3 client.py host post         to start the client application
    eg. python3 client.py localhost 1060


Start page:
----
Use the LOGIN button to sign in
Use the WHO IS ON button to see which users are online. You will have to press
the REFRESH button to get the updated list

Login page:
----
Type username and password into the respective fields and press the LOGIN
button when ready

Whoison page:
----
Click the REFRESH button to get the updated list
Click the BACK button to go back to the main page if not logged in, or the
message page if you're logged in

Send Message page:
----
Click the Who is on button to go to the Whoison page
Click the Send File button if you wish to send a file instead of a message
Click the Profiles button to check the user Profiles
Click the Logout button to log out

The inbox textfield shows all of the messages the currently logged user has

The Send message to box holds the message that you will send to the desired
user

Click the SEND button to send the message
Click the REFRESH button to retrieve all of the messages the currently
logged in user has

Send File page:
----
Choose the user you want to send a file to and press the upload file button
to send the file

The My files textfield holds the files that have been sent to the currently
logged in user

Click the BACK button to go back to the Send Message page
Click the REFRESH button to retrieve any files that have been send to the
currently logged in user

Profiles page:
----
You can switch profiles by clicking the drowdown menu options and pressing
the GO button

The picture and the attributes should change as the user is selected

Click the BACK button to go back to the Send Message page
