# Welcome To The CHAT APPLICATION

##### **Group Members: Michael Balian and Arin Deravanesian**

### Prerequisites Before Running Application

###### -First you must install python on your machine. You can visit the python website for instructions on how to install: https://www.python.org/downloads/

###### -After installation, you can verify that python has installed successfully by running this command:

```
python --version
or
python3 --version

Note: Depending on the version you installed you will either have to use python or python3 as shown above
```

###### -If python is not found when running the version command then you have to set the system environment variables to point to the python directory on machine.

###### -You can find more information on setting environmental variables in this article: https://docs.python.org/3/using/windows.html

### How To Run Chat Application

###### Open a terminal and CD into the projects root directory

###### Run the main.py file to start application:

```
python main.py
or
python3 main.py

Note: Depending on the version you installed you will either have to use python or python3 as shown above
```

### How to use the Chat Application

###### Once you have ran the main.py file now you will be prompted to enter your server's listening port number

###### After you have entered a valid port number, you will now have access to client side commands to chat with other devices or processes

###### You have access to the following commands:

```
help - This will list all available commands
myip - This will display your devices IPv4 Address
myport - This will display the port you entered at the start of the application
connect <destination ip address> <destingation port number> - This command will etablish a connection with another user
list - This command lists all established connections
terminate <connection id> - Use this command to terminate a connection from the list of established connections
send <connection id> "<message>" - Use this command to send a messge to another user from your list of established connections. (NOTE: MESSAGE MUST BE IN QUOTES)
exit - Use this command to exit the chat application
```

### Group member contributions

#### **Michael Balian**

###### I worked on the client side of this application, my work consisted of:

###### -Creating all client prompts for user to interact with the different client commands

###### -If user enters an invalid command or value I have implemented error handling

###### -I decided to make functions for each shell command to keep the code clean

###### -I also added some utility functions to work with managing client connections on the local machine. This way a user can add and terminate connections as needed

###### -I had to handle invalid cases like trying to establish a self connection, duplicate connections, when a user tries to establish the same connection multiple times it will only register one connection and not try to add mulitiple of the same connection.
