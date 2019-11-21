import socket
from _thread import *
import pickle
from game import Game

# creating the server and the port
# server's IP address
server = "192.168.43.253"
port = 5555

# creating the socket(socket type, stream)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding our server znd port to the socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Listening for the connection(opening the port) 2 player connect at atime to a game
s.listen(2)
print("Waiting for a connection, Server Started")


# storing ip addresses of the connected clients
connected = set()
# storing games in game dictionary
games = {}
# idcount is the id of the current game
idCount = 0


# Creating a threaded client for creating multiple 2 player games at the same time
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            # the amount of information we are trying to receive is 4096 bits
            data = conn.recv(4096).decode()

            # if the game exits
            if gameId in games:
                game = games[gameId]

                # if we are not getting information from client or client left then we break
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    # closing connection
    conn.close()


# always looking for a client connection while threaded client is in process all the time
while True:
    # accepting the connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    # how many people are connected
    idCount += 1
    p = 0
    # every 2 people connected to the server we create a game id
    gameId = (idCount - 1)//2
    # if idcount is odd then we need another player to create a game
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")

    # when we have the even no of player to join the game with earlier player who is waiting to start palying (then we start the game because both the player are connected)
    else:
        games[gameId].ready = True
        p = 1

    # creating new thread for every game for every two players
    start_new_thread(threaded_client, (conn, p, gameId))
