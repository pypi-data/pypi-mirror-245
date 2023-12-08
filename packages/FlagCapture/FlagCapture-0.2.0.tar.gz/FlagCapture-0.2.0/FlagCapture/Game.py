
import socket
import gymnasium as gym
import math
import pyglet
from pyglet.window import key
from FlagCapture.entity import MeshEnt
from FlagCapture.miniworld import MiniWorldEnv
from FlagCapture.utils import get_file_path
from  FlagCapture.build import BUILD
from threading import Thread as T

# Building the environment
BUILD()

# Setting up the IP address and port number
Ip = '68.60.238.141'
Port = 4544
ADDR = (Ip, Port)

# Connecting to the server
cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl.connect(ADDR)

# Sending a message to the server
cl.send('Capture the red-and-blue special flags that are available for capture.'.encode('utf-8'))

# Receiving information from the server
start_info = eval(cl.recv(58000).decode('utf-8').split('A@^!')[0])

# Creating a Scene class which inherits from MiniWorldEnv
class Scene(MiniWorldEnv):
    def __init__(self, **kwargs):
        MiniWorldEnv.__init__(self, **kwargs)
    # Generating the world
    def _gen_world(self):
        self.mainroom = self.add_rect_room(min_x=0, max_x=92, min_z=-60, max_z=60)
        self.add_rect_room(min_x=2, max_x=2.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=10, max_x=10.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=18, max_x=18.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=26, max_x=26.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=42, max_x=42.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=50, max_x=50.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=58, max_x=58.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=74, max_x=74.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=82, max_x=82.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=90, max_x=90.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=2, max_x=10, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=18, max_x=26, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=34, max_x=42, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=50, max_x=58, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=66, max_x=74, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=82, max_x=90, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')

        self.add_rect_room(min_x=2, max_x=22, min_z=28, max_z=28.01, wall_tex='redColor')
        self.add_rect_room(min_x=22, max_x=22.01, min_z=6, max_z=28, wall_tex='redColor')
        self.add_rect_room(min_x=78, max_x=90, min_z=28, max_z=28.01, wall_tex='redColor')
        self.add_rect_room(min_x=78, max_x=78.01, min_z=6, max_z=28, wall_tex='redColor')
        self.add_rect_room(min_x=26, max_x=26.01, min_z=20, max_z=36, wall_tex='redColor')
        self.add_rect_room(min_x=74, max_x=74.01, min_z=20, max_z=36, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=66, min_z=10, max_z=10.01, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=10, max_z=22, wall_tex='redColor')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=10, max_z=22, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=34, max_z=42, wall_tex='redColor')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=34, max_z=42, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=44, min_z=42, max_z=42.01, wall_tex='redColor')
        self.add_rect_room(min_x=54, max_x=66, min_z=42, max_z=42.01, wall_tex='redColor')
        self.add_rect_room(min_x=0, max_x=42, min_z=45, max_z=45.01, wall_tex='redColor')
        self.add_rect_room(min_x=56, max_x=92, min_z=45, max_z=45.01, wall_tex='redColor')
        self.add_rect_room(min_x=42.5, max_x=53.5, min_z=47, max_z=47.01, wall_tex='redColor')
        self.add_rect_room(min_x=40, max_x=46.5, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=49.5, max_x=56, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=40, max_x=40.01, min_z=49, max_z=60, wall_tex='redColor')
        self.add_rect_room(min_x=56, max_x=56.01, min_z=49, max_z=60, wall_tex='redColor')
        self.add_rect_room(min_x=18, max_x=35, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=0, max_x=2, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=4, max_x=10, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=10, max_x=10.01, min_z=49, max_z=58, wall_tex='redColor')
        self.add_rect_room(min_x=61, max_x=74, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=90, max_x=92, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=82, max_x=88, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=82, max_x=82.01, min_z=49, max_z=58, wall_tex='redColor')

        self.add_rect_room(min_x=2, max_x=22, max_z=-28, min_z=-28.01, wall_tex='blueColor')
        self.add_rect_room(min_x=22, max_x=22.01, max_z=-6, min_z=-28, wall_tex='blueColor')
        self.add_rect_room(min_x=78, max_x=90, max_z=-28, min_z=-28.01, wall_tex='blueColor')
        self.add_rect_room(min_x=78, max_x=78.01, max_z=-6, min_z=-28, wall_tex='blueColor')
        self.add_rect_room(min_x=26, max_x=26.01, max_z=-20, min_z=-36, wall_tex='blueColor')
        self.add_rect_room(min_x=74, max_x=74.01, max_z=-20, min_z=-36, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=66, max_z=-10, min_z=-10.01, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=34.01, max_z=-10, min_z=-22, wall_tex='blueColor')
        self.add_rect_room(min_x=66, max_x=66.01, max_z=-10, min_z=-22, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=34.01, max_z=-34, min_z=-42, wall_tex='blueColor')
        self.add_rect_room(min_x=66, max_x=66.01, max_z=-34, min_z=-42, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=44, max_z=-42, min_z=-42.01, wall_tex='blueColor')
        self.add_rect_room(min_x=54, max_x=66, max_z=-42, min_z=-42.01, wall_tex='blueColor')
        self.add_rect_room(min_x=0, max_x=42, max_z=-45, min_z=-45.01, wall_tex='blueColor')
        self.add_rect_room(min_x=56, max_x=92, max_z=-45, min_z=-45.01, wall_tex='blueColor')
        self.add_rect_room(min_x=42.5, max_x=53.5, max_z=-47, min_z=-47.01, wall_tex='blueColor')
        self.add_rect_room(min_x=40, max_x=46.5, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=49.5, max_x=56, max_z=-49, min_z=-49.01, wall_tex='blueColor' )
        self.add_rect_room(min_x=40, max_x=40.01, max_z=-49, min_z=-60, wall_tex='blueColor')
        self.add_rect_room(min_x=56, max_x=56.01, max_z=-49, min_z=-60, wall_tex='blueColor')
        self.add_rect_room(min_x=18, max_x=35, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=0, max_x=2, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=4, max_x=10, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=10, max_x=10.01, max_z=-49, min_z=-58, wall_tex='blueColor')
        self.add_rect_room(min_x=61, max_x=74, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=90, max_x=92, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=82, max_x=88, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=82, max_x=82.01, max_z=-49, min_z=-58, wall_tex='blueColor')
        self.redGate = self.place_entity(MeshEnt(mesh_name=f'gate', height=2.6), pos=[48, 0, 49], dir=-3.1)
        self.blueGate = self.place_entity(MeshEnt(mesh_name=f'gate', height=2.6), pos=[48, 0, -49], dir=6.3)
        self.redFlag = self.place_entity(MeshEnt(mesh_name=f'flagRed', height=2.5, static=False), pos=start_info['RedFlagPos'])
        self.blueFlag = self.place_entity(MeshEnt(mesh_name=f'flagBlue', height=2.5, static=False), pos=start_info['BlueFlagPos'])
        # Iterate through the start_info dictionary
        for person in start_info['Everything']:
            # Check if the person is not the current user
            if person != myId:
                # Place the entity with the mesh name, height, and static status from the start_info dictionary
                animal = self.place_entity(MeshEnt(mesh_name=f''+start_info['Everything'][person]['team'], height=1.4, static=False), pos=start_info['Everything'][person]['pos'], dir=start_info['Everything'][person]['dir'])
                # Add the person to the people dictionary
                people[person] = animal
                # If the team of the person is not the same as the current user's team, add them to the list of players on their team
                if not start_info['Everything'][person]['team'] == myTeam:
                    list_of_players_on_their_team.append(person)

        # Place the red and blue buttons at the specified positions
        self.leftRedButton = self.place_entity(MeshEnt(mesh_name=f'RedButton', height=1), pos=[82.5, 1, -44.749], dir=-1.5)
        self.rightRedButton = self.place_entity(MeshEnt(mesh_name=f'RedButton', height=1), pos=[9.5, 1, -44.749], dir=-1.5)
        self.rightBlueButton = self.place_entity(MeshEnt(mesh_name=f'BlueButton', height=1), pos=[9.5, 1, 44.749], dir=1.6)
        self.leftBlueButton = self.place_entity(MeshEnt(mesh_name=f'BlueButton', height=1), pos=[82.5, 1, 44.749], dir=1.6)

        # Place the agent
        self.place_agent()

# Register the environment with the gym library
gym.envs.registration.register(id='Enviroment', entry_point=Scene)

# Get the starting information for the agent
myinfo = start_info['MyInfo']
myTeam = myinfo['team']
myId = myinfo['id']

# Initialize lists and dictionaries
list_of_players_on_their_team = []
people = {}

# Set creating to False
creating = False

# Create the environment, set the fuel, reset the environment, set the agent's position and direction, render the environment, and set the window properties
board = key.KeyStateHandler()
scene = gym.make("Enviroment", view='agent', render_mode='human')
scene.unwrapped.fuel = 5
scene.reset()
scene.agent.pos = [myinfo['x'], 0, myinfo['z']]
scene.agent.dir = myinfo['dir']
scene.render()
scene.unwrapped.window.push_handlers(board)
scene.unwrapped.window.set_icon(pyglet.image.load(get_file_path("images", "icon", "png")))
caption = f'Capture the Flag: [{myTeam} Team]'
scene.unwrapped.window.set_caption(caption)
scene.unwrapped.window.maximize()
scene.unwrapped.window.set_mouse_visible(False)

# Move the agent forward at a speed of 0.4
def forward(obj, speed):
    global touching
    direction = -obj.dir
    x = obj.pos[0] + math.cos(direction)*speed
    z = obj.pos[2] + math.sin(direction)*speed
    intersection = scene.intersect(obj, [x, 0, z], obj.radius)
    # Check if the agent is touching a button
    if not touching:
        if myTeam == 'wolf':
            if intersection == scene.leftBlueButton or intersection == scene.rightBlueButton:
                cl.send(str(['Updating touching', {'touching': True}]).encode('utf-8'))
                touching = True
        if myTeam == 'lynx':
            if intersection == scene.leftRedButton or intersection == scene.rightRedButton:
                cl.send(str(['Updating touching', {'touching': True}]).encode('utf-8'))
                touching = True
    # Check if the agent is intersecting with a gate
    if intersection == scene.blueGate and IAmPrisoner:return
    if intersection == scene.redGate and IAmPrisoner:return
    # Update the agent's position
    if intersection == True:
        x_pos = [x, 0, obj.pos[2]]
        if scene.intersect(obj, x_pos, obj.radius) == True:
            z_pos = [obj.pos[0], 0, z]
            if scene.intersect(obj, z_pos, obj.radius) == True:
                return
            else:
                cl.send(str(['Updating pos', {'pos': z_pos}]).encode('utf-8'))
        else:
            cl.send(str(['Updating pos', {'pos': x_pos}]).encode('utf-8'))
    else:
        cl.send(str(['Updating pos', {'pos': [x, 0, z]}]).encode('utf-8'))

# Set the speed of the agent
speed = 0.4

def update(dt):
    global speed, carrying
    # Increase fuel by 1
    scene.unwrapped.fuel += 1

    # Check if red flag is in the correct position
    if carrying == 'red' and scene.agent.pos[2] < 0:
        blue_wins()
    # Check if blue flag is in the correct position
    if carrying == 'blue' and scene.agent.pos[2] > 0:
        red_wins()
    # Move the agent forward if UP key is pressed
    if board[key.UP]:
        forward(scene.agent, speed)
    # Rotate the agent left if LEFT key is pressed
    if board[key.LEFT]:
        cl.send(str(['Updating dir', {'dir': scene.agent.dir + speed/2}]).encode('utf-8'))
    # Rotate the agent right if RIGHT key is pressed
    if board[key.RIGHT]:
        cl.send(str(['Updating dir', {'dir': scene.agent.dir - speed/2}]).encode('utf-8'))
    # Move the agent backward if DOWN key is pressed
    if board[key.DOWN]:
        forward(scene.agent, -speed)
    # Pick up the flag if P key is pressed
    if board[key.P]:
        if scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius) == scene.redFlag:
            carrying = 'red'
            scene.unwrapped.window.set_caption(f'{caption} [CARRYING A FLAG]')
            cl.send(str(['Updating carrying', {'carrying': 'red'}]).encode('utf-8'))
            scene.redFlag.pos = [30, -90, 0]
        if scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius) == scene.blueFlag:
            carrying = 'blue'
            scene.unwrapped.window.set_caption(f'{caption} [CARRYING A FLAG]')
            cl.send(str(['Updating carrying', {'carrying': 'blue'}]).encode('utf-8'))
            scene.blueFlag.pos = [30, -90, 0]

    # Drop the flag if D key is pressed
    if board[key.D]:
        drop_flag()

    # Increase the speed if SPACE key is pressed
    if board[key.SPACE]:
        if scene.unwrapped.fuel < 3:
            speed = 0.4
        else:
            scene.unwrapped.fuel -= 3
            speed = 0.8
    else:
        speed = 0.4
    # Render the scene
    scene.render()
    

# This function will close the scene after 4 seconds and display an alert image
def blue_wins():
    def close(dt):
        scene.close()
    pyglet.clock.schedule_once(close, 4)
    alert(get_file_path("images", "wolfwin", "png"), 4)

# This function will close the scene after 4 seconds and display an alert image
def red_wins():
    def close(dt):
        scene.close()
    pyglet.clock.schedule_once(close, 4)
    alert(get_file_path("images", "lynxwin", "png"), 4)

# This function drops the flag if the agent is carrying one
def drop_flag():
    global carrying
    if carrying:
        if carrying == 'red':
            scene.redFlag.pos = scene.agent.pos
            # Checks if the red flag is below 0, blue wins
            if scene.redFlag.pos[2] < 0:blue_wins()   
        elif carrying == 'blue':
            scene.blueFlag.pos = scene.agent.pos
            # Checks if the blue flag is above 0, red wins
            if scene.blueFlag.pos[2] > 0:red_wins()
        cl.send(str(['drop', {'flag': carrying}]).encode('utf-8'))
        carrying = None
        scene.unwrapped.window.set_caption(caption)

# Initializes the carrying variable to None
carrying = None

IAmPrisoner = False

# This function displays an alert image for a certain amount of time
def alert(picture, time):
    scene.unwrapped.alert = pyglet.image.load(picture)
    scene.unwrapped.showAlert = True
    # After the specified time, the alert image will be removed
    def put_back(dt):
        scene.unwrapped.showAlert = False
    pyglet.clock.schedule_once(put_back, time)
# This function is called when the window needs to be drawn. It clears the window and renders the scene.
@scene.unwrapped.window.event
def on_draw():
    scene.unwrapped.window.clear()
    scene.render() 

# This function receives messages from the server.
def recv():
    global raw_message
    while True:
        raw_message = cl.recv(58000).decode('utf-8').split('A@^!')[0]
        if raw_message.strip() == '':continue
        pyglet.clock.schedule_once(process_message, 1.0/60)

# This variable stores the raw message received from the server.
raw_message = None

# This dictionary stores the message after it has been evaluated.
message = {}

# This function processes the message received from the server.
def process_message(dt):
    global IAmPrisoner, message, creating
    try:
        message = eval(raw_message)
    except SyntaxError:
        return
    
    # Iterate through each person in the message.
    for person in message:
        # If the person is not in the people list and is not the current user and you are not currently creating something...
        if person not in people and person != myId and not creating:#Some one joined
            creating = True
            # Place an entity with the mesh name, height, and static status specified in the message.
            animal = scene.place_entity(MeshEnt(mesh_name=message[person]['team'], height=1.4, static=False), pos=message[person]['pos'], dir=message[person]['dir'])
            print(message[person]['pos'])
            people[person] = animal
            # If the team of the person is not the same as the current user's team, add them to the list of players on their team.
            if not message[person]['team'] == myTeam:
                list_of_players_on_their_team.append(person)
            creating = False

        elif person != myId: #Update the players
            # Update the position and direction of the player.
            people[person].pos = message[person]['pos']
            people[person].dir = message[person]['dir']
            # If the player is carrying the red flag, update its position and direction.
            if message[person]['carrying'] == 'red':
                scene.redFlag.pos = [message[person]['pos'][0], 0, message[person]['pos'][2]]
                if scene.redFlag.pos[2] < 0:blue_wins()
                scene.redFlag.dir = math.radians(math.degrees(message[person]['dir'])+180)
            # If the player is carrying the blue flag, update its position and direction.
            if message[person]['carrying'] == 'blue':
                scene.blueFlag.pos = [message[person]['pos'][0], 0, message[person]['pos'][2]]
                if scene.blueFlag.pos[2] > 0:red_wins()
                scene.blueFlag.dir = math.radians(math.degrees(message[person]['dir'])+180)

            # If the player is on the same team as the current user and the user is a prisoner and the player is touching them...
            if message[person]['team'] == myTeam and IAmPrisoner and message[person]['touching']:#Check to see if someone is freeing you
                    IAmPrisoner=False
                    alert(get_file_path("images", "release", "png"), 2.5)

        elif person == myId:
            # Update the position and direction of the current user.
            scene.agent.pos = message[person]['pos']
            scene.agent.dir = message[person]['dir']
            # If the user is touching something, alert them and move them back 10 units.
            if message[person]['touching'] == True:
                alert(get_file_path("images", "release", "png"), 2.5)
                forward(scene.agent, -10)
        
    # Iterate through each person in the people list.
    for person in people:
        # If the person is not in the message, they have left.
        if person not in message:#Some one left
            # Remove the entity from the scene and delete them from the people list.
            scene.unwrapped.entities.remove(people[person])
            del people[person]
            break
    # Check for capture and touching button.
    check_for_capture_and_touching_button()

# on_close() function closes the connection
def on_close():
    cl.close()

# touching is a boolean variable to check if the button is being touched
touching = False

# check_for_capture_and_touching_button() checks for capture and touching of buttons
def check_for_capture_and_touching_button():
    global IAmPrisoner, touching
    intersection = scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius)

    # Check if the button is being touched
    if touching:
        if myTeam == 'wolf':
            if intersection != scene.leftBlueButton or intersection == scene.rightBlueButton:
                cl.send(str(['Updating touching', {'touching': False}]).encode('utf-8'))
                touching = False
        if myTeam == 'lynx':
            if intersection != scene.leftRedButton or intersection == scene.rightRedButton:
                cl.send(str(['Updating touching', {'touching': False}]).encode('utf-8'))
                touching = False

    # Check for touching enemy and in enemy territory
    for person in list_of_players_on_their_team:
        try:
            if intersection == people[person] and scene.agent.pos[2] < 0:
                if myTeam == 'wolf':
                    if carrying:
                        drop_flag()
                        scene.agent.pos = [48, 0, -55]
                        scene.agent.dir = 4.754
                        IAmPrisoner = True
                        cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                        cl.send(str(['Updating pos', {'pos': [48, 0, -55]}]).encode('utf-8'))
                if myTeam == 'lynx':
                    if message[person]['carrying']: return
                    if message[person]['prisoner']: return
                    drop_flag()
                    scene.agent.pos = [48, 0, 55]
                    scene.agent.dir = 1.654
                    IAmPrisoner = True
                    cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                    cl.send(str(['Updating pos', {'pos': [48, 0, 55]}]).encode('utf-8'))
            if intersection == people[person] and scene.agent.pos[2] > 0:
                if myTeam == 'lynx':
                    if carrying:
                        drop_flag()
                        scene.agent.pos = [48, 0, 55]
                        scene.agent.dir = 1.654
                        IAmPrisoner = True
                        cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                        cl.send(str(['Updating pos', {'pos': [48, 0, 55]}]).encode('utf-8'))
                if myTeam == 'wolf':
                    if message[person]['carrying']:return
                    if message[person]['prisoner']: return
                    drop_flag()
                    scene.agent.pos = [48, 0, -55]
                    scene.agent.dir = 4.754
                    IAmPrisoner = True
                    cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                    cl.send(str(['Updating pos', {'pos': [48, 0, -55]}]).encode('utf-8'))
        except KeyError:
            list_of_players_on_their_team.remove(person)

# Start thread to receive messages from server
T(target=recv).start()

# Schedule update at 30 frames per second
pyglet.clock.schedule_interval(update, 1.0/30)

# Run the application
pyglet.app.run()