# This is a modified version of zen_utils.py given to us by the book

import argparse, socket, ssl, subprocess, sqlite3
import re
from datetime import datetime
import pickle

def accept_connections_forever(listener):
    """Forever answer incoming connections on a listening socket."""
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address)

def check_user_or_pass(user, passw):
    """Checks if the user or pass is valid in the SQL database."""
    con = sqlite3.connect('database.lite')
    # Create SQLite3 cursor to query database
    cur = con.cursor()
    # Execute SQL statement
    cur.execute('SELECT USER FROM AUTHORIZED_USERS WHERE PASSWORD IS \'{}\';'.format(passw))
    # Fetch tuple matching statement
    username = cur.fetchall()
    # Execute SQL statement
    cur.execute('SELECT PASSWORD FROM AUTHORIZED_USERS WHERE USER IS \'{}\';'.format(user))
    # Fetch tuple matching statement
    password = cur.fetchall()
    # Close connection without making any changes since we are only reading data
    con.close()

    # If either username or password is empty, then the query failed, meaning
    # the username or password was not input properly
    if not username or not password:
        return False
    else:
        return True

def create_srv_socket(address):
    """Build and return a listening server socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def server_request_handler(pickled_request, address):
    """Receives a request and returns an returns reply based on what the
       request is"""

    # Take the delimeter off the request
    pikcled_request = pickled_request[:-1]

    # Unpickle request
    request = pickle.loads(pickled_request)
    print(f'Received from {address}: {request}')

    # Format request
    request_header = request[0]
    request_payload = request[1]
    # Split request header by >
    request_header = request_header.split('>')
    # Connect to database
    con = sqlite3.connect('database.lite')
    # Create SQLite3 cursor to query database
    cur = con.cursor()    

    # If none of the following conditions are met, then request will be invalid
    # by default 
    reply_header = '500>INVALID>REQUEST'
    reply_payload = b''
    if len(request_header) == 1:
        reply_header = '500>INVALID>REQUEST'
    elif request_header[0] == '100':
        # LOGIN request
        # 100>LOGIN>user>pass
        try:
            # Extract username and password from request
            user = request_header[2]
            passw = request_header[3]
            if check_user_or_pass(user, passw):
                reply_header = '101>LOGIN>SUCCESS'
                # Set the status of user in database to 'online'
                cur.execute(f'UPDATE AUTHORIZED_USERS SET status = \'online\' WHERE user=\'{user}\';')
                # Save changes to the database
                con.commit()
            else:
                reply_header = '102>LOGIN>FAIL'
        except Exception as e:
            reply_header = '102>LOGIN>FAIL'
    elif request_header[0] == '103':
        # LOGOUT request
        # 103>LOGOUT>user
        try:
            user = request_header[2]
            reply_header = '104>LOGOUT>SUCCESS'
            cur.execute(f'UPDATE AUTHORIZED_USERS SET status = \'offline\' WHERE user=\'{user}\';')
            con.commit()
        except Exception as e:
            reply_header = '105>LOGOUT>FAIL'

    elif request_header[0] == '200':
        # WHOISON request
        # 200>WHOISON
        try:
            # Execute SQL statement
            cur.execute('SELECT USER FROM AUTHORIZED_USERS WHERE status IS \'offline\';')
            # Fetch tuple matching statement
            offline = cur.fetchall()

            # Format reply
            reply_header  = '201>OFFLINE>'

            # Iterate through offline users
            for word in offline:
                # Trim the string using regular expression and add a comma at the end
                reply_header = reply_header + re.sub('[^A-Za-z0-9]+', '', str(word)) + ','
            # If no users then store NULL value
            if not offline:
                reply_header = reply_header + 'NULL,'

            # Execute SQL statement
            cur.execute('SELECT USER FROM AUTHORIZED_USERS WHERE status IS \'online\';')
            # Fetch tuple matching statement
            online = cur.fetchall()

            # Format reply
            reply_header = reply_header + '>ONLINE>'
            # Iterate through online users
            for word in online:
                # Trim the string using regular expression and add a comma at the end
                reply_header = reply_header + re.sub('[^A-Za-z0-9]+', '', str(word)) + ','
            # If no users then store NULL value
            if not online:
                reply_header = reply_header + 'NULL,'
        except Exception as e:
            reply_header = '202>WHOISON>FAIL'
    elif request_header[0] == '300':
        # SENDMSG request
        # 300>SENDMSG>destination>source>messages
        try:
            # Grab destination and source from request_header
            destination = request_header[2]
            source = request_header[3]
            # Create a datetime object
            now = datetime.now()
            # # Format the date/time
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            # Grab message from request_header
            message = request_header[4]
            # Execute SQL statement
            cur.execute(f"""INSERT INTO MESSAGE_LOGS VALUES (\'{destination}\', 
                \'{source}\', \'{date}\', \'{message}\');""")
            # Save (commit) the changes
            con.commit()
            # Close connection
            con.close()
            # Format reply
            reply_header = '301>SENDMSG>SUCCESS'
        except Exception as e:
            reply_header = '302>SENDMSG>FAIL'
    elif request_header[0] == '303':
        # RETRIEVE request
        # 303>RETRIEVEMSG>user
        try:
            user = request_header[2]
            # Execute SQL statement
            cur.execute(f"""SELECT source, message from MESSAGE_LOGS WHERE destination=\'{user}\';""")
            # Save (commit) the changes
            con.commit()
            # Close connection
            messages = cur.fetchall()
            con.close()
            formatted_messages = ""
            for message in messages:
                formatted_messages = formatted_messages + message[0] + ":" + message[1] + "|"
            reply_header = f'304>RETRIEVEMSG>SUCCESS>{formatted_messages}'
        except Exception as e:
            reply_header = '305>RETRIEVEMSG>FAIL'
    elif request_header[0] == '306':
        # SENDFILE request
        # 306>SENDFILE>destination>source>file_name
        # b'file'
        try:
            # Get fields from request_header
            destination = request_header[2]
            source = request_header[3]
            file_name = request_header[4]
            file = request_payload

            # Create a datetime object
            now = datetime.now()
            # # Format the date/time
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            # Execute SQL statement
            cur.execute("INSERT INTO FILE_LOGS VALUES (?, ?, ?, ?, ?)", (destination, source, date, file_name, file))
            print("test", flush=True)
            # Save (commit) the changes
            con.commit()
            # Close connection
            con.close()
            # Format reply
            reply_header = '307>SENDFILE>SUCCESS'
        except Exception as e:
            reply_header = '308>SENDFILE>FAIL'
    elif request_header[0] == '309':
        # RETRIEVEFILE request
        # 309>RETRIEVEFILE>user'
        try:
            user = request_header[2]
            # Execute SQL statement
            cur.execute(f"""SELECT source, name, file FROM FILE_LOGS WHERE destination=\'{user}\';""")
            # Save (commit) the changes
            con.commit()
            # Close connection
            queries = cur.fetchall()
            con.close()
            reply_payload = b''
            sources = ''
            file_names = ''

            # If no files then load reply with NULL values
            if not queries:
                sources = 'NULL'
                file_names = 'NULL'

            # If there are files for the user, format sources, file_names, and
            # reply_payload with their respective elements
            for elements in queries:
                sources = sources + elements[0] + ','
                file_names = file_names + elements[1] + ','
                reply_payload = reply_payload + elements[2] + b'|*|'

            # trim the last comma from sources and file_names if there are files present
            if queries:
                sources = sources[:-1]            
                file_names = file_names[:-1]
                reply_payload = reply_payload[:-3]

            # Format reply header
            reply_header = f'310>RETRIEVEFILE>SUCCESS>{sources}>{file_names}'
        except Exception as e:
            reply_header = '311>RETRIEVEFILE>FAIL'
    elif request_header[0] == '400':
        # PROFILE request
        # eg. 400>PROFILE>user
        try:
            # Grab user from request_header
            user = request_header[2]
            cur.execute(f"""SELECT * FROM PROFILE WHERE fname=\'{user}\';""")
            # Save (commit) the changes
            con.commit()
            # Close connection
            query = cur.fetchall()

            # Format reply_header
            reply_header = '401>PROFILE>SUCCESS>'

            # Grab values for profile
            for tuple in query:
                for value in tuple:
                    reply_header = reply_header + value + '>'
            # Trim last >
            reply_header = reply_header[:-1]
        except Exception as e:
            reply_header = '402>PROFILE>FAIL'
    
    # Format reply
    reply = []
    reply.append(reply_header)
    reply.append(reply_payload)

    # Wrap reply in a pickle and send back to client
    pickled_reply = pickle.dumps(reply)
    # Add delimeter
    pickled_reply = pickled_reply + b';'
    print(f'Sending to {address}: {repr(reply)} ')
    return pickled_reply
    
def handle_conversation(sock, address):
    """Converse with a client over `sock` until they are done talking."""
    try:
        while True:
            # Changed this to pass the address as well
            handle_request(sock, address)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client hello {} error: {}'.format(address, e))
    finally:
        sock.close()

def handle_request(sock, address):
    """Receive a single client request on `sock` and send the answer."""
    request = recv_until(sock, b';') # Delimeter is ;
    reply = server_request_handler(request, address)
    sock.sendall(reply)

def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

def recv_until(sock, suffix):
    """Receive bytes over socket `sock` until we receive the `suffix`."""
    message = sock.recv(32768)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data = sock.recv(32768)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message