import socket
import pickle

# creating the network class
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server's IP address
        self.server = "192.168.43.253"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    # creating connection to the server
    def connect(self):
        try:
            # connecting the client
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    # sending information to the server
    def send(self, data):
        try:
            # sending string data from server to client (player number)
            self.client.send(str.encode(data))
            # receiving object data from client
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)