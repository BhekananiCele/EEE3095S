import socket
from datetime import datetime
import threading

#difine constants
SENDON = "SENDON"
SENDOFF = "SENDOFF"
SENDACK = "SENDACK"
CHECK= "CHECK"
STATUS = "STATUS"
SENSORS = "SENSORS"

TCP_IP_SERVER = "192.168.137.122" #Server IP Address
TCP_PORT_SERVER = 5005

TCP_IP_CLIENT = "192.168.137.53" #Client IP Address
TCP_PORT_CLIENT = 5007

BUFFER_SIZE = 1024
SAMPLING = 0
LAST_SAMPLING_TIME_STAMP = None
 
# Function that send a message to the server
def sendDataToServer(MESSAGE):
    global LAST_SAMPLING_TIME_STAMP
    if(SAMPLING):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP_SERVER, TCP_PORT_SERVER))
            LAST_SAMPLING_TIME_STAMP = datetime.now().strftime("%d/%m/%y %H:%M")
            msg = SENSORS+"@"+MESSAGE+"@"+ str(LAST_SAMPLING_TIME_STAMP)
            s.send(msg.encode())
            s.close()
        except Exception as e:
            print(e)

# Function that listens for messages coming from the server
def ListenToServer():
    global SAMPLING
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP_CLIENT, TCP_PORT_CLIENT))
    s.listen(1)
    print("Client Listening To The Server")
    while 1:
        conn, addr = s.accept()
        try:
            data = conn.recv(BUFFER_SIZE).decode().split()
            if(data[0]==SENDON):
                SAMPLING = 1
                conn.send(SENDACK.encode()) 
            elif(data[0]==SENDOFF):
                SAMPLING = 0
                conn.send(SENDACK.encode()) 
            elif(data[0]==CHECK):
                msg = STATUS+" <h3>Sampling: "+str(bool(SAMPLING))+"<br/>Last Sampling Time Stamp: "+str(LAST_SAMPLING_TIME_STAMP)+"</h3>"
                conn.send(msg.encode())      
            conn.close()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        
if __name__ == '__main__':
    thread = threading.Thread(target=ListenToServer)
    thread.daemon = True
    thread.start()
    
    while True:
        pass
     
     