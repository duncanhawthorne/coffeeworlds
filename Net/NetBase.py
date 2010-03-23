import socket,select,sys,time
from Errors import *
from Communicate import SendData, ReceiveData
    
class Server():
    def __init__(self):
        self.sending_socket = None

    def input_func(self,sock,host,port,address):pass
    def output_func(self,sock,host,port,address):pass
    def connect_func(self,sock,host,port):pass
    def client_connect_func(self,sock,host,port,address):pass
    def client_disconnect_func(self,sock,host,port,address):pass
    def quit_func(self,host,port):pass
        
    def connect(self,host,port):
        self.host = host
        self.port = port
        try:
            self.unconnected_socket = socket.socket()
            self.unconnected_socket.bind((self.host,self.port))
            self.unconnected_socket.listen(5)
            self.connect_func(self.unconnected_socket,self.host,self.port)
        except:
            self.unconnected_socket.close()
            raise ServerError("Only one instance of the server on port "+str(self.port)+" may run at one time!")
        self.connected_sockets = []
        self.socketaddresses = {}

    def remove_socket(self,sock):
        address = self.socketaddresses[sock]
        self.client_disconnect_func(sock,self.host,self.port,address)
        self.connected_sockets.remove(sock)
    def serve_forever(self):
        self.looping = True
        while self.looping:
            input_ready,output_ready,except_ready = select.select([self.unconnected_socket]+self.connected_sockets,[],[])
            for sock in input_ready:
                if sock == self.unconnected_socket:
                    #init socket
                    connected_socket, address = sock.accept()
                    self.connected_sockets.append(connected_socket)
                    self.socketaddresses[connected_socket] = address
                    self.client_connect_func(connected_socket,self.host,self.port,address)
                else:
                    try:
                        data = ReceiveData(sock)
                        address = self.socketaddresses[sock]
                        self.input_func(sock,self.host,self.port,address)
                    except:
                        data = "client quit"
                    if data != None:
                        if data == "client quit":
                            self.remove_socket(sock)
                            continue
                        self.sending_socket = sock
                        self.handle_data(data)
                    
    def handle_data(self,data):
        pass
    def send_data(self,data):
        try:
            SendData(self.sending_socket,data)
            address = self.socketaddresses[self.sending_socket]
            self.input_func(self.sending_socket,self.host,self.port,address)
        except:
            self.remove_socket(self.sending_socket)
            
    def quit(self):
        for s in self.connected_sockets: s.close()
        self.quit_func(self.host,self.port)
        
class Client:
    def __init__(self):
        pass
    def connect(self,host,port):
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket()
            self.sock.connect((self.host,self.port))
        except:
            self.sock.close()
            raise SocketError("The connection could not be opened.  It must be created first with a server object.")
        
    def send_data(self,data):
        SendData(self.sock,data)
    def receive_data(self):
        data = ReceiveData(self.sock)
        return data
    
    def quit(self):
        SendData(self.sock,"client quit")
        self.sock.close()
