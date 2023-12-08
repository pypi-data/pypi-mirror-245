import socket # import the socket module 
from threading import Thread as T # import the Thread class from the threading module
import random # import the random module
from itertools import cycle # import the cycle function from the itertools module

teams = cycle(['lynx', 'wolf']) # create a cycle object with the two teams

posiible_x_positions = [87, 69, 53, 37, 22, 5] # list of possible x positions for players

Ip = '127.0.0.1' # set the IP address
Port = 4544 # set the port number

ADDR = (Ip, Port) # create a tuple with the IP and port

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object
Server.bind(ADDR) # bind the socket to the address

everything = {} # create an empty dictionary

def handle_client(conn, addr): # define a function to handle each client connection
    global redFlagPos, blueFlagPos # declare the global variables
    password = conn.recv(52000).decode('utf-8') # receive the password from the client
    if password != 'Capture the red-and-blue special flags that are available for capture.': # check if the password is correct
        conn.close() # close the connection if the password is incorrect
        print('Hacker alert') # print a message
        return # end the function
    team = next(teams) # get the next team in the cycle
    x = random.choice(posiible_x_positions) # choose a random x position
    z = -3 if team == 'wolf' else 3 # set the z position based on the team
    dir = 4.754 if team == 'wolf' else 1.654 # set the direction based on the team
    conn.send((str({'Everything': everything,  'RedFlagPos': redFlagPos, 'BlueFlagPos': blueFlagPos, 'MyInfo': {'team': team, 'x': x, 'z': z, 'dir': dir, 'id': str(addr)}})+'A@^!').encode('utf-8')) # send the data to the client
    everything[str(addr)] = {'pos': [x, 0, z], 'dir': dir, 'team': team, 'touching': False, 'carrying': None, 'prisoner': False} # add the client's data to the dictionary
    notify() # call the notify function
    notifing_list.append(conn) # add the connection to the list

    while True: # loop forever
        try: # try to execute the following code
            message = eval(conn.recv(58000).decode('utf-8')) # receive a message from the client
            if message[0] == 'Updating prisoner': # check if the message is about updating the prisoner
                everything[str(addr)]['prisoner'] = message[1]['prisoner'] # update the prisoner value
            if message[0] == 'Updating pos': # check if the message is about updating the position
                everything[str(addr)]['pos'] = message[1]['pos'] # update the position
            if message[0] == 'Updating dir': # check if the message is about updating the direction
                everything[str(addr)]['dir'] = message[1]['dir'] # update the direction
            if message[0] == 'Updating touching': # check if the message is about updating the touching value
                everything[str(addr)]['touching'] = message[1]['touching'] # update the touching value
            if message[0] == 'Updating carrying': # check if the message is about updating the carrying value
                everything[str(addr)]['carrying'] = message[1]['carrying'] # update the carrying value
            if message[0] == 'drop': # check if the message is about dropping a flag
                everything[str(addr)]['carrying'] = None # set the carrying value to None
                if message[1]['flag'] == 'red': # check if the flag is red
                    redFlagPos = everything[str(addr)]['pos'] # update the red flag position
                if message[1]['flag'] == 'blue': # check if the flag is blue
                    blueFlagPos = everything[str(addr)]['pos'] # update the blue flag position
            notify() # call the notify function
        except ConnectionAbortedError: # catch the ConnectionAbortedError exception
            print('Some one disconnected') # print a message
            notifing_list.remove(conn) # remove the connection from the list
            del everything[str(addr)] # delete the client's data from the dictionary
            return # end the function
        except ConnectionRefusedError: # catch the ConnectionRefusedError exception
            print('Some one disconnected') # print a message
            notifing_list.remove(conn) # remove the connection from the list
            del everything[str(addr)] # delete the client's data from the dictionary
            return # end the function
        except ConnectionResetError: # catch the ConnectionResetError exception
            print('Some one disconnected') # print a message
            notifing_list.remove(conn) # remove the connection from the list
            del everything[str(addr)] # delete the client's data from the dictionary
            return # end the function
        except Exception: # catch any other exceptions
            pass # do nothing

def notify(): # define a function to notify all clients
    for connection in notifing_list: # loop through all connections in the list
        connection.send((str(everything)+'A@^!').encode('utf-8')) # send the data to the client

redFlagPos = random.choice([[4, 0, 58], [88, 0, 58]]) # choose a random position for the red flag
blueFlagPos = random.choice([[4, 0, -58], [88, 0, -58]]) # choose a random position for the blue flag
notifing_list = [] # create an empty list

def start(): # define a function to start the server
    print('[[Server is listening]]') # print a message
    Server.listen() # listen for incoming connections
    while True: # loop forever
        conn, addr = Server.accept() # accept a connection
        print(f'[[New Connection]] {addr} has connected!!') # print a message
        T(target=handle_client, args=(conn, addr)).start() # start a new thread to handle the client

print('[[Server is Starting]]') # print a message
start()