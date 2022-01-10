from pathlib import Path
from tkinter import filedialog
import argparse, socket, ssl, zen_utils, re, pickle
import tkinter as tk

# Declare font family and sizes
LARGEFONT = ("DejaVu Math TeX Gyre", 35)
MEDIUMFONT = ("Consolas", 22)
SMALLFONT = ("Consolas", 14)

# Define parent class
class tkinterApp(tk.Tk):
    def __init__(self, host, port):
        tk.Tk.__init__(self)
        # Get host and port from command line arguements
        self.host = host
        self.port = port
        # Set user as NULL initially
        self.user = "NULL"
        # Set the dimensions for application window
        self.geometry("500x800")

        # Define all images used in application
        self.login_image = tk.PhotoImage(file = 'img/login.gif')
        self.whoison_image = tk.PhotoImage(file = 'img/whoison.gif')
        self.chat_image = tk.PhotoImage(file = 'img/chat.gif')
        self.franco_image = tk.PhotoImage(file = 'img/franco.gif')
        self.libero_image = tk.PhotoImage(file = 'img/libero.gif')
        self.alan_image = tk.PhotoImage(file = 'img/alan.gif')
        self.john_image = tk.PhotoImage(file = 'img/john.gif')
        self.daniel_image = tk.PhotoImage(file = 'img/daniel.gif')
        self.back_image = tk.PhotoImage(file = 'img/back.gif')
        self.refresh_image = tk.PhotoImage(file = 'img/refresh.gif')
        self.send_image = tk.PhotoImage(file = 'img/send.gif')
        self.go_image = tk.PhotoImage(file = 'img/go.gif')
        self.file_image = tk.PhotoImage(file = 'img/file.gif')
        self.download_image = tk.PhotoImage(file = 'img/download.gif')
        self.daniel2_image = tk.PhotoImage(file = 'img/daniel2.png')
        self.franco2_image = tk.PhotoImage(file = 'img/franco2.png')
        self.libero2_image = tk.PhotoImage(file = 'img/libero2.png')
        self.john2_image = tk.PhotoImage(file = 'img/john2.png')
        self.alan2_image = tk.PhotoImage(file = 'img/alan2.png')

        # Define containers to switch frames (pages)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 
        # Initiate frames
        for F in (start_page, login_page, whoison_page, 
                  message_page, file_page, profile_page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        # Show start page by default
        self.show_frame(start_page)        

    def show_frame(self, cont):
        """Switches frame(page)."""
        frame = self.frames[cont]
        frame.tkraise()

    def get_host(self):
        """Gets host from command line arguements."""
        return self.host

    def get_port(self):
        """Gets port from command line arguements."""
        return self.port

    def get_user(self):
        """Gets currently logged user."""
        return self.user
        
    def set_user(self, user):
        """Sets currently logged user to a new user."""
        self.user = user

    def get_img(self, name):
        """Gets an image depending on the name."""
        if name == 'login':
            return self.login_image
        elif name == 'whoison':
            return self.whoison_image
        elif name == 'chat':
            return self.chat_image
        elif name == 'franco':
            return self.franco_image
        elif name == 'libero':
            return self.libero_image
        elif name == 'alan':
            return self.alan_image
        elif name == 'john':
            return self.john_image
        elif name == 'daniel':
            return self.daniel_image
        elif name == 'refresh':
            return self.refresh_image
        elif name == 'back':
            return self.back_image
        elif name == 'send':
            return self.send_image
        elif name == 'go':
            return self.go_image
        elif name == 'daniel2':
            return self.daniel2_image
        elif name == 'libero2':
            return self.libero2_image
        elif name == 'franco2':
            return self.franco2_image
        elif name == 'alan2':
            return self.alan2_image
        elif name == 'john2':
            return self.john2_image
        elif name == 'file':
            return self.file_image
        elif name == 'download':
            return self.download_image

class start_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome_label = tk.Label(self, text ="Welcome", font = LARGEFONT)
        self.welcome_label.pack(pady = 10)

        self.chatimg = tk.Label(self, image  = self.controller.get_img('chat'))
        self.chatimg.pack(pady = 10)

        self.login_button = tk.Button(self, image = self.controller.get_img('login'),
                                 command = lambda : controller.show_frame(login_page))
        self.login_button.pack(pady = 10) 

        self.whosion_button = tk.Button(self, image = self.controller.get_img('whoison'),
                                   command = lambda : controller.show_frame(whoison_page))
        self.whosion_button.pack(pady = 10)

class login_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Align elements in grid
        self.grid_columnconfigure(0, minsize=100)

        # Login label
        self.login_label = tk.Label(self, text ="Login", font = LARGEFONT)
        self.login_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Username label and text field
        self.user_label = tk.Label(self, text = "Username:", font = MEDIUMFONT)
        self.user_label.grid(row = 1, column = 1, sticky="w")
        self.user_entry = tk.StringVar()
        tk.Entry(self, font = MEDIUMFONT, textvariable = self.user_entry).grid(
            row = 2, column = 1, padx = 5, pady = 5)

        # Password label and text field
        self.pass_label = tk.Label(self, text = "Password:", font = MEDIUMFONT)
        self.pass_label.grid(row = 3, column = 1, sticky="w")
        self.pass_entry = tk.StringVar()
        # Hide password
        tk.Entry(self, show = '*', font = MEDIUMFONT,
            textvariable = self.pass_entry).grid(row = 4, column = 1)

        # Login button
        self.login_button = tk.Button(self, image = self.controller.get_img('login'),
            command = self.login)
        self.login_button.grid(row = 5, column = 1, padx = 10, pady = 10)

        # Feedback label, text will change denpending on the action being preformed
        self.feedback_label = tk.Label(self, text ="",
                                           font = SMALLFONT, foreground='#FF0000')
        self.feedback_label.grid(row = 6, column = 1, padx = 10, pady = 10)

    def login(self):
        """Sends a LOGIN request to the server and changes frame when its
        sucessful."""
        # Get user and password from textfields
        user = self.user_entry.get()
        passw = self.pass_entry.get()
        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        # Format the request header
        request_header = f'100>LOGIN>{user}>{passw}'
        # Initiate the request payload
        request_payload = b''

        # Put the request together
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))

        # Wrap the request in a pickle
        pickled_request = pickle.dumps(request)
        # Send with a delimeter
        sock.sendall(pickled_request + b';')
        # Receive pickled reply
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Unpickle the reply
        reply = pickle.loads(pickled_reply)
        print('The server said', reply)

        # Close socket
        sock.close()

        # Process reply
        if reply[0] == '101>LOGIN>SUCCESS':
            self.controller.set_user(user)
            self.controller.show_frame(message_page)
        elif reply[0] == '102>LOGIN>FAIL': 
            self.feedback_label.config(text = "Invalid username or password")

class whoison_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Get host and port from parent class
        self.host = controller.get_host()
        self.port = controller.get_port()
            
        # Align elements in grid
        self.grid_columnconfigure(0, minsize=52)

        # Users Online Label and textfield containing user images
        self.online_label = tk.Label(self, text ="Users Online", font = LARGEFONT)
        self.online_label.pack()
        self.users_online_box = tk.Text(self, width = 37, height = 0, 
                                        font = SMALLFONT, state=tk.DISABLED)
        self.users_online_box.pack()

        # Users Offline Label and textfield containing user images
        self.offline_label = tk.Label(self, text ="Users Offline", font = LARGEFONT)
        self.offline_label.pack()
        self.users_offline_box = tk.Text(self, width = 37, height = 0, 
                                         font = SMALLFONT, state=tk.DISABLED)
        self.users_offline_box.pack()

        # Back button
        self.back_button = tk.Button(self, image = self.controller.get_img('back'),
                                     command = self.go_back)
        self.back_button.pack(pady=10)

        # Refresh button
        self.refresh_button = tk.Button(self, image = self.controller.get_img('refresh'),
                                    command = self.refresh)
        self.refresh_button.pack(pady=10)

    def go_back(self):
        """Goes back to start_page if no user is logged in or goes to
        message_page if there is an user logged in."""
        if self.controller.user == 'NULL':
            self.controller.show_frame(start_page)
        else:
            self.controller.show_frame(message_page)

    def add_image(self, textbox, img):
        """Adds images to the textfield dynamically."""
        position = textbox.index(tk.INSERT)
        textbox.image_create(position, image=img)
    
    def refresh(self):
        """Does a WHOISON request and displays users online/offline."""
        # Switch the state of textfield so it can be edited
        self.users_online_box.config(state=tk.NORMAL)
        self.users_offline_box.config(state=tk.NORMAL)
        # Delete previous data
        self.users_offline_box.delete('1.0', tk.END)
        self.users_online_box.delete('1.0', tk.END)
        # Switch state back
        self.users_online_box.config(state=tk.DISABLED)
        self.users_offline_box.config(state=tk.DISABLED)

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        request_header = '200>WHOISON'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)        
        print("Request: " + repr(request))

        # Wrap request in a pickle
        pickled_request = pickle.dumps(request)
        sock.sendall(pickled_request + b';')
        # Receive pickled reply
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Close socket
        sock.close()
        # Remove delimiter
        pikcled_reply = pickled_reply[:-1]
        # Unpickle reply
        reply = pickle.loads(pickled_reply)

        # Process reply
        reply_header = reply[0].split('>')
        reply_payload = reply[1]

        # Grab online and offline users and store them in lists
        self.online_users = reply_header[4][:-1].split(',')
        self.offline_users = reply_header[2][:-1].split(',')

        # Grab amount of each user to format textfield
        self.num_users_online = len(self.online_users)
        self.num_users_offline = len(self.offline_users)
        self.users_online_box.config(height = (self.num_users_online * 5.4))
        self.users_offline_box.config(height = (self.num_users_offline * 5.4))

        # Iterate through online users, add the corresponding image to the textfield
        for user in self.online_users:
            if user == 'NULL':
                self.users_online_box.config(height = 0)
                break
            self.add_image(self.users_online_box, self.controller.get_img(user))

        # Iterate through online users, add the corresponding image to the textfield
        for user in self.offline_users:
            if user == 'NULL':
                self.users_online_box.config(height = 0)
                break
            self.add_image(self.users_offline_box, self.controller.get_img(user))

class message_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Get host and port from parent class (controller)
        self.host = controller.get_host()
        self.port = controller.get_port()

        # Align columns by faking column 0
        self.grid_columnconfigure(0, minsize=62)

        # Messaging Label
        self.messaging_label = tk.Label(self, text = "Messaging", font = LARGEFONT)
        self.messaging_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Who Is On button
        whoison_button = tk.Button(self, text="Who is on",
                            command = lambda : controller.show_frame(whoison_page))
        whoison_button.grid(row = 1, column = 1, padx = 10, pady = 3)

        # Send File button
        sendfile_button = tk.Button(self, text="Send File",
                            command = lambda : controller.show_frame(file_page))
        sendfile_button.grid(row = 2, column = 1, padx = 10, pady = 3)

        # Profiles button
        profiles_button = tk.Button(self, text="Profiles",
                            command = lambda : controller.show_frame(profile_page))
        profiles_button.grid(row = 3, column = 1, padx = 10, pady = 3)

        # Log Out button
        logout_button = tk.Button(self, text="Logout",
                            command = self.logout)
        logout_button.grid(row = 4, column = 1, padx = 10, pady = 3)

        # Inbox textfield, display all messages that have been sent to the user
        self.inbox_label = tk.Label(self, text = "Inbox:", font = MEDIUMFONT)
        self.inbox_label.grid(row = 5, column = 1, sticky="w")

        # Inbot text area
        self.inbox = tk.Text(self, width=40, height=10, font = SMALLFONT, state=tk.DISABLED)
        self.inbox.grid(row = 6, column = 1, sticky = "nsew", pady = 2)
        # Scrollbar for text area
        self.inbox_scroll = tk.Scrollbar(self, command=self.inbox.yview)
        self.inbox_scroll.grid(row = 6, column = 2, sticky = "nsew", pady = 2)
        self.inbox['yscrollcommand'] = self.inbox_scroll.set

        # Send message to label
        self.send_label = tk.Label(self, text = "Send message to:", font = MEDIUMFONT)
        self.send_label.grid(row = 7, column = 1, sticky="w")

        # Drop down options
        self.send_to = tk.StringVar(self)
        self.send_to.set("daniel") # default value
        self.who_to_send = tk.OptionMenu(self, self.send_to, "daniel", "franco", "libero", "alan", "john")
        self.who_to_send.grid(row = 8, column = 1, padx = 10, pady = 10, sticky="w")

        # Text area for sending messages
        self.send_box = tk.Text(self, width = 40, height = 5, font = SMALLFONT)
        self.send_box.grid(row = 9, column = 1, sticky = "nsew", pady = 2)
        # Scrollbar for text area
        self.send_box_scroll = tk.Scrollbar(self, command=self.send_box.yview)
        self.send_box_scroll.grid(row = 9, column = 2, sticky = "nsew", pady = 2)
        self.send_box['yscrollcommand'] = self.send_box_scroll.set

        # Send button
        self.send_button = tk.Button(self, image = self.controller.get_img('send'), command = self.send_message)
        self.send_button.grid(row = 10, column = 1, padx = 10, pady = 10)

        # Refresh button
        self.refresh_button = tk.Button(self, image = self.controller.get_img('refresh'), command = self.refresh)
        self.refresh_button.grid(row = 11, column = 1, padx = 10, pady = 10)

    def send_message(self):
        """Does a SEND request to send a message to a desired user."""

        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        # Grab currently logged user from parent class
        user = self.controller.user
        # Grab destination from dropdown menu
        destination = self.send_to.get()
        # Grab message from textfield
        message = self.send_box.get('1.0', 'end-1c')

        # Construct request
        request_header = f'300>SEND>{destination}>{user}>{message}'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))

        # Wrap request in a pickle
        pickled_request = pickle.dumps(request)
        sock.sendall(pickled_request + b';')
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Take delimter out
        pickled_reply = pickled_reply[:-1]
        # Unpickle reply
        reply = pickle.loads(pickled_reply)
        # Close socket
        sock.close()

        print('The server said', repr(reply))

    def refresh(self):
        """Does a RETRIEVEMSG request to get messages inbox for the currently
        logged in user."""

        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Format the request
        request_header = f'303>RETRIEVEMSG>{self.controller.user}'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))
        pickled_request = pickle.dumps(request)
        sock.sendall(pickled_request + b';')
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Take delimeter out
        pickled_reply = pickled_reply[:-1]
        # Close socket
        sock.close()
        
        # Unwrap reply from pickle
        reply = pickle.loads(pickled_reply)

        print('The server said', reply)

        # Format the reply header
        reply_header = reply[0].split('>')

        # Take the last > out
        messages = reply_header[3][:-1]
        # Split messages with |
        messages = messages.split('|')

        # Switch state of inbox textfield so it can be modified
        self.inbox.config(state = tk.NORMAL)
        self.inbox.delete('1.0', tk.END)

        # Iterate through messages and display them in inbox textfield
        for message in messages:
            self.inbox.insert(tk.END, message)
            self.inbox.insert(tk.END, "\n")

        # Switch state back to disabled after being modified
        self.inbox.config(state = tk.DISABLED)

    def logout(self):
        """Does a LOGOUT request. Switches user status to offline in the
        database."""

        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()
        
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Format the request
        request_header = f'103>LOGOUT>{self.controller.user}'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))

        # Wrap request in a pickle
        pickled_request = pickle.dumps(request)
        # Send pickled request and a delimeter
        sock.sendall(pickled_request + b';')
        # Receive reply wrapped in a pickle
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Take delimeter out
        pickled_reply = pickled_reply[:-1]
        # Close socket
        sock.close()
        
        # Get reply from server
        reply = pickle.loads(pickled_reply)
        # Set user to NULL to signify that there is no user logged in this
        # particular client.
        self.controller.user = 'NULL'
        print('The server said', reply)
        # Go to start_page after logging out
        self.controller.show_frame(start_page)

class file_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Align columns
        self.grid_columnconfigure(0, minsize=62)

        # Send File label
        self.sendfile_label = tk.Label(self, text ="Send File", font = LARGEFONT)
        self.sendfile_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # To Who label
        self.towho_label = tk.Label(self, text = "To who:", font = MEDIUMFONT)
        self.towho_label.grid(row = 1, column = 1, sticky="w")

        # Send to dropdown options
        self.send_to = tk.StringVar(self)
        self.send_to.set("daniel") # default value
        self.who_to_send = tk.OptionMenu(self, self.send_to, "daniel",
                                         "franco", "libero", "alan", "john")
        self.who_to_send.grid(row = 2, column = 1, padx = 10,
                              pady = 10, sticky="w")

        # Upload file button
        self.upload_button = tk.Button(self, text ="upload file",
                                       command = self.file_open)
        self.upload_button.grid(row = 3, column = 1, padx = 10, pady = 10)

        # My files label
        self.inbox_label = tk.Label(self, text = "My files:", font = MEDIUMFONT)
        self.inbox_label.grid(row = 4, column = 1, sticky="w")

        # Text area for files received by currently logged in user
        self.inbox = tk.Text(self, width=40, height=10, font = SMALLFONT, state=tk.DISABLED)
        self.inbox.grid(row = 5, column = 1, sticky = "nsew", pady = 2)
        # scrollbar for text area
        self.inbox_scroll = tk.Scrollbar(self, command=self.inbox.yview)
        self.inbox_scroll.grid(row = 5, column = 2, sticky = "nsew", pady = 2)
        self.inbox['yscrollcommand'] = self.inbox_scroll.set

        # Back button
        self.back_button = tk.Button(self, image=self.controller.get_img('back'),
                            command = lambda : controller.show_frame(message_page))
        self.back_button.grid(row = 6, column = 1, padx = 10, pady = 10)

        # Refresh button
        self.refresh_button = tk.Button(self, image=self.controller.get_img('refresh'),
                            command = self.refresh)
        self.refresh_button.grid(row = 7, column = 1, padx = 10, pady = 10)

        # Feedback label, changes depending on the action
        self.feedback_label = tk.Label(self, text = "", font = SMALLFONT, foreground='#FF0000')
        self.feedback_label.grid(row = 8, column = 1, padx = 10, pady = 10)

    def file_open(self):
        """Does a SENDFILE request to the server. Grabs file from client and
        sends it as a stream of bytes and stores into SQLite database as a blob."""
        
        # Open file dialog
        my_file = filedialog.askopenfilename()

        # If file is selected, send it to the server
        if my_file:
            # Store file in blob_data
            with open(my_file, 'rb') as file:
                blob_data = file.read()

            # Get host and port from parent class
            host = self.controller.get_host()
            port = self.controller.get_port()
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            
            # Grab destination from drop down menu options
            destination = self.send_to.get()
            # Grab path from selected file
            path = Path(my_file)
            # Select only the file name from path
            file_name = path.name

            # Format request
            request_header = f'306>SENDFILE>{destination}>{self.controller.user}>{file_name}'
            request_payload = blob_data

            # Create request list
            # Format: [request_header(string), request_payload(bytearray)]
            request = []
            request.append(request_header)
            request.append(request_payload)
            print("Request: " + repr(request))

            # Wrap request in a pickle
            pickled_request = pickle.dumps(request)
            # Send pickled request and delimiter
            sock.sendall(pickled_request + b';')

            # Receive reply wrapped in a pickle
            pickled_reply = zen_utils.recv_until(sock, b';')
            sock.close()
            # Take delimeter out
            pickled_reply = pickled_reply[:-1]

            # Unpickle reply
            reply = pickle.loads(pickled_reply)
            print('The server said', reply)
            
            # Process reply
            reply_header = reply[0]
            reply_payload = reply[1]
            if reply_header == '307>SENDFILE>SUCCESS':
                self.feedback_label.config(text = "File sent successfully.")
            else:
                self.feedback_label.config(text = "File not sent.")
        else:
            self.feedback_label.config(text = "File not selected.")

    def refresh(self):
        """Does a RETRIEVEFILE request. Gets all of the files that belong to
        the desired user."""

        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()
        
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Format request
        request_header = f'309>RETRIEVEFILE>{self.controller.user}'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))

        # Wrap request in a pickle
        pickled_request = pickle.dumps(request)
        # Send pickled request and a delimeter
        sock.sendall(pickled_request + b';')
        # Receive pickled reply
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Close socket
        sock.close()
        # Take delimeter out of pickled reply
        pickled_reply = pickled_reply[:-1]

        # Unpickle the reply
        reply = pickle.loads(pickled_reply)
        print('The server said', reply)

        # Process reply
        reply_header = reply[0]
        reply_payload = reply[1]
        reply_header = reply_header.split('>')
        sources = reply_header[3].split(',')
        file_names = reply_header[4].split(',')

        # Process reply if there are files present
        if sources[0] != 'NULL':
            files = reply_payload
            # Files are split by b'|*|'
            files = files.split(b'|*|')

            # Switch state of textfield so it can be modified
            self.inbox.config(state = tk.NORMAL)
            # Delete old contents to replace with new data
            self.inbox.delete('1.0', tk.END)
            # Index of the files
            file_num = 0
            # Iterate through files and insert them in a formatted way
            for file in files:
                self.inbox.insert(tk.END, "From {}:".format(sources[file_num]))
                self.inbox.image_create(self.inbox.index("end"), image = self.controller.get_img('file'))
                self.inbox.insert(tk.END, file_names[file_num])
                self.inbox.window_create(self.inbox.index("end"), window = tk.Button(self.inbox, image=self.controller.get_img('download'), command=lambda : self.download(file)))
                self.inbox.insert(tk.END, "\n")
                file_num += 1
            # Switch state back to disabled so that the user can't delete them
            # by mistake
            self.inbox.config(state = tk.DISABLED)
    
    def download(self, data):
        """Downloads a stream of bytes into a file."""

        # Ask user to save file
        file = filedialog.asksaveasfile()

        # Update feedback label based on user action
        if file:
            self.feedback_label.configure(text = 'File saved.')
            file = open(file.name, 'wb')
            file.write(data)
        else:
            self.feedback_label.configure(text = 'File not saved.')

class profile_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Defaults
        self.first_name = 'First Name: daniel'
        self.last_name = 'Last Name: prieto'
        self.email = 'Email: d_prieto@outlook.com'
        self.phone = 'Phone: 780-978-2418'
        self.department = 'Department: science'

        # Align columns
        self.grid_columnconfigure(0, minsize=42)

        # Profiles label
        title_label = tk.Label(self, text ="Profiles", font = LARGEFONT)
        title_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Switch profile label
        self.towho_label = tk.Label(self, text = "Switch profile:", font = MEDIUMFONT)
        self.towho_label.grid(row = 1, column = 1, padx = 10, pady = 5, sticky="w")

        # Drop down menu options
        self.send_to = tk.StringVar(self)
        self.send_to.set("daniel") # default value
        self.who_to_send = tk.OptionMenu(self, self.send_to, "daniel", "franco",
                                         "libero", "alan", "john")
        self.who_to_send.grid(row = 2, column = 1, padx = 10, pady = 5, sticky="w")

        # Go button
        self.go_button = tk.Button(self, image = self.controller.get_img('go'),
            command = lambda : self.change_profile(self.send_to.get()))
        self.go_button.grid(row = 3, column = 1, padx = 10, pady = 5, sticky="w")

        # Profile image label
        self.profile_img = tk.Label(self, image  = self.controller.get_img('daniel2'), font = SMALLFONT)
        self.profile_img.grid(row = 4, column = 1, padx = 10, pady = 0)

        # First name label
        self.first_name_label = tk.Label(self, text = self.first_name, font = MEDIUMFONT)
        self.first_name_label.grid(row = 5, column = 1, padx = 10, pady = 3)

        # Last name label
        self.last_name_label = tk.Label(self, text = self.last_name, font = MEDIUMFONT)
        self.last_name_label.grid(row = 6, column = 1, padx = 10, pady = 3)

        # Email label
        self.email_label = tk.Label(self, text = self.email, font = MEDIUMFONT)
        self.email_label.grid(row = 7, column = 1, padx = 10, pady = 3)

        # Phone label
        self.phone_label = tk.Label(self, text = self.phone, font = MEDIUMFONT)
        self.phone_label.grid(row = 8, column = 1, padx = 10, pady = 3)

        # Department label
        self.department_label = tk.Label(self, text = self.department, font = MEDIUMFONT)
        self.department_label.grid(row = 9, column = 1, padx = 10, pady = 3)

        # Back button
        self.back_button = tk.Button(self, image = self.controller.get_img('back'),
                            command = lambda : self.controller.show_frame(message_page))
        self.back_button.grid(row = 10, column = 1, padx = 10, pady = 5)

    def change_profile(self, user):
        """Changes information on the profile page based on which user is
        selected through the drop down menu options."""

        # Get host and port from parent class
        host = self.controller.get_host()
        port = self.controller.get_port()

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server
        sock.connect((host, port))

        # Format request
        request_header = f'400>PROFILE>{user}'
        request_payload = b''

        # Create request list
        # Format: [request_header(string), request_payload(bytearray)]
        request = []
        request.append(request_header)
        request.append(request_payload)
        print("Request: " + repr(request))

        # Wrap request in a pickle
        pickled_request = pickle.dumps(request)
        # Send pickled request and delimeter
        sock.sendall(pickled_request + b';')

        # Receive reply wrapped in a pickle
        pickled_reply = zen_utils.recv_until(sock, b';')
        # Close socket
        sock.close()
        # Take delimeter out
        pickled_reply = pickled_reply[:-1]

        # Unpickle reply
        reply = pickle.loads(pickled_reply)
        print('The server said', reply)

        # Process reply
        reply_header = reply[0]
        reply_payload = reply[1]
        reply_header = reply_header.split('>')
        # construct fields from reply
        fname = reply_header[3]
        lname = reply_header[4]
        email = reply_header[5]
        phone = reply_header[6]
        department = reply_header[7]

        # The profile images are labeled "name2" so I just add a 2 at the end of
        # username
        user_img = fname + '2'

        # Change labels to reflect new user
        self.profile_img.config(image = self.controller.get_img(user_img))
        self.first_name_label.config(text = f'First Name: {fname}')
        self.last_name_label.config(text = f'Last Name: {lname}')
        self.email_label.config(text = f'Email: {email}')
        self.phone_label.config(text = f'Phone: {phone}')
        self.department_label.config(text = f'Department: {department}')

# Main method
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP client')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('port', type=int, help='TCP port number')
    args = parser.parse_args()

    # Pass host and port from arguments
    app = tkinterApp(args.host, args.port)
    app.mainloop()