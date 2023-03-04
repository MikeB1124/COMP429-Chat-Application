import threading
import socket

serverPort = 0
userConnections = []
validServerPort = False

#Server to listen for messages
def server():
    global validServerPort
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('', int(serverPort)))
        serverSocket.listen(1)
        print("\n\nThe server is ready to receive messages")
        print("-------------------------------------------")
        print("Press ENTER to use the chat application!")
        print("-------------------------------------------")
        while True:
            connectionSocket, addr = serverSocket.accept()
            message = connectionSocket.recv(1024).decode()
            action = message.split(":")[0]
            ip = message.split(":")[1]
            port = message.split(":")[2]
            messageBody = message.split(":")[3]
            if action == "Connection":
                addConnectionToLocal(ip, port)
            elif action == "Termination":
                removeConnectionFromLocal(ip, port)
                print(f"\n{ip}:{port} has terminated the connection with you.")
            elif action == "Message":
                print(f"\n\nMessage received from {ip}")
                print(f"Sender's Port: {port}")
                print(f'Message: "{messageBody}"')
                
            connectionSocket.close()
    except:
        validServerPort = False
        print("\n\nPORT IS ALREADY BEING USED - RESTART APPLICATION")



#Client Side

#Check for duplicate connections
def checkForDuplicateConnection(ip, port):
    for user in userConnections:
        if(user["ip"] == ip and int(user["port"]) == int(port)):
            return True
    return False
    
#Get IP and Port number from table ID
def getConnectionDetailsFromId(id):
    global userConnections
    ip = None
    port = None
    for user in userConnections:
        if(user["id"] == int(id)):
            ip = user["ip"]
            port = user["port"]
    return {"ip": ip, "port": port}

#Add connection to local memory
def addConnectionToLocal(ip, port):
    if(not checkForDuplicateConnection(ip, port)):
        userId = len(userConnections)
        userConnections.append({"id": userId, "ip": ip, "port": port})
        print(f"\nConnection established to {ip}:{port}")
    else:
        print(f"\nConnection reestablished to {ip}:{port}")

#Remove connection from local memory
def removeConnectionFromLocal(ip, port):
    global userConnections
    updatedConnections = []
    index = 0
    for user in userConnections:
        if(user["ip"] != ip or int(user["port"]) != int(port)):
            updatedConnections.append({"id": index, "ip": user["ip"], "port": user["port"]})
            index += 1
    userConnections = updatedConnections


#Shell Commands
def help():
    print("\nWelcome to the chat application")
    print("-----------------------------------------------")
    print('help\nmyip\nmyport\nconnect <destination ip address> <destingation port number>\nlist\nterminate <connection id>\nsend <connection id> "<message>"\nexit')
    print("-----------------------------------------------\n")

def myip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def connectToPeer(ip, port):
    #Check for self connection or existing connection
    if(ip == myip() and int(port) == int(serverPort)):
        print("Self connections are not valid")
        return
    
    if(checkForDuplicateConnection(ip, port)):
        print("Connection already exists for specified ip and port")
        return
        
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ip, int(port)))
        message = f"Connection:{ip}:{serverPort}:Connection established"
        clientSocket.send(message.encode())
        addConnectionToLocal(ip, port)
        listConnections()
    except:
        print(f"Unable to connect to {ip}:{port}")   
    
    
def listConnections():
    global userConnections
    print("\n")
    print("       Existing Connections        ")
    print("-----------------------------------")
    print(" ID:   IP address      Port No.")
    print("-----------------------------------")
    for user in userConnections:
        userId = user["id"]
        userIp = user["ip"]
        userPort = user["port"]
        print(f" {userId}   {userIp}       {userPort}")
    print("\n")
        
def terminateConnection(id):
    userConnection = getConnectionDetailsFromId(id)
    ip = userConnection["ip"]
    port = userConnection["port"]
    if(ip == None):
        print("Invalid connection ID")
        return        
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ip, int(port)))
        message = f"Termination:{ip}:{serverPort}:Connection terminated"
        clientSocket.send(message.encode())
        removeConnectionFromLocal(ip, port)
        listConnections()
    except:
        print(f"Unable to terminate connection with {ip}:{port}.")
    
    
def sendMessage(id, messageBody):
    userConnection = getConnectionDetailsFromId(id)
    ip = userConnection["ip"]
    port = userConnection["port"]
    if(ip == None):
        print("Invalid connection ID")
        return 
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ip, int(port)))
        message = f"Message:{ip}:{serverPort}:{messageBody}"
        clientSocket.send(message.encode())
    except:
        print(f"Unable to connect to {ip}:{port}")
        
def exitApp():
    for user in userConnections:
        ip = user["ip"]
        port = user["port"]
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((ip, int(port)))
            message = f"Termination:{ip}:{serverPort}:Connection terminated"
            clientSocket.send(message.encode())
        except:
            print(f"Unable to terminate connection with {ip}:{port}.")
    exit()
        
        
        
#Prompt user for port number before starting application
while not validServerPort:
    serverPort = input("Choose listenting port number (port number > 1024): ")
    if(serverPort != ""):
        if(int(serverPort) > 1024):
            validServerPort = True
        else:
            print("Port number must be greater then 1024")
threading.Thread(target=server, daemon=True).start()       


#Run Client Application if a Valid Port is Entered
while True and validServerPort:
    userInput = input("\nChoose from menu options or enter help for to see options: ")
    try:
        if(userInput == "help"):
            help()
        elif(userInput == "myip"):
            ip = myip()
            print(f"The devices ip address is {ip}")
        elif(userInput == "myport"):
            print(f"The program runs on port number {serverPort}")
        elif(userInput.split(" ")[0] == "connect"):
            ipInput = userInput.split(" ")[1]
            portInput = userInput.split(" ")[2]
            connectToPeer(ipInput, portInput)
        elif(userInput == "list"):
            listConnections()
        elif(userInput.split(" ")[0] == "terminate"):
            id = userInput.split(" ")[1]
            terminateConnection(id)
        elif(userInput.split(" ")[0] == "send"):
            userId = userInput.split(" ")[1]
            message = userInput.split('"')[1]
            if(len(message) <= 100):
                sendMessage(userId, message)
            else:
                print("\nMessage cannot be longer then 100 characters.")
        elif(userInput == "exit"):
            exitApp()
        else:
            if(userInput != ""):
                print("Invalid option")
    except:
        print("Invalid input format please look at instructions on README file")