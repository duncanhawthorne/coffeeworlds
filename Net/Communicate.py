from Errors import *
try:    import cPickle as pickle
except: import pickle as pickle

class Packet:
    def __init__(self,data):
        self.data = data

def SendData(sock,data):
    #pickle data
    try:
        data = pickle.dumps(Packet(data))
        data = str(len(data))+"||"+data
    except:
        sock.close()
        raise PickleError("The data could not be pickled.")
    #send data
    try:
        sock.send(data)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be sent!")
def ReceiveData(sock):
    #receive data
    try:
        x = sock.recv(1024)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be received!")
    n = x.split("||")[0]
    rest = x[len(n)+2::]
    size = int(n)
    buf = rest
    while len(buf) < size:
        try:
            buf += sock.recv(1024)
        except:
            sock.close()
            raise SocketError("Connection is broken; data could not be received!")
    #unpickle data
    try:
        data = pickle.loads(buf).data
        return data
    except:
        sock.close()
        raise PickleError("The data could not be unpickled.")
