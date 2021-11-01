import socket
import threading
import csv
import os
#difine constants
SENDON = "SENDON"
SENDOFF = "SENDOFF"
SENDACK = "SENDACK"
CHECK = "CHECK"
STATUS = "STATUS"
SENSORS = "SENSORS"

TCP_IP_SERVER = "192.168.137.122" #Server IP Address
TCP_PORT_SERVER = 5005

TCP_IP_CLIENT = "192.168.137.53" #Client IP Address
TCP_PORT_CLIENT = 5007

BUFFER_SIZE = 1024
Render_Page = False

# Function that send a message to the client
def sendDataToClient(MESSAGE):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP_CLIENT, TCP_PORT_CLIENT))
        s.send(MESSAGE.encode())
        data = s.recv(BUFFER_SIZE).decode()
        s.close()
        if(data.split(" ")[0]==STATUS):
            return data[len(STATUS)+1:]
        return "Done"
    except Exception as e:
        print(e)
        return "Offline"

# Function that listens for messages coming from the client
def ListenToClients():
    global Render_Page
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP_SERVER, TCP_PORT_SERVER))
    s.listen(1)
    print("Server Listening To The Client")
    while 1:
        conn, addr = s.accept()
        try:
            data = conn.recv(BUFFER_SIZE).decode().split("@")
            sensorVal = data[1].split()
            conn.close()
            if(data[0]==SENSORS):   
                file = "sensorlog.csv"        
                with open(file , 'a') as csvfile:
                    fieldnames = ['Temp_Reading','Light_Reading','Time_Stamp']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if(csvfile.tell() == 0):
                        writer.writeheader()
                    writer.writerow({'Temp_Reading': sensorVal[0], 'Light_Reading': sensorVal[1], 'Time_Stamp': data[2]})
                Render_Page = True
        except Exception as e:
            print(e)
        finally:
            conn.close()
             
if __name__ == '__main__':
    thread = threading.Thread(target=ListenToClients)
    thread.daemon = True
    thread.start()
    while True:
        pass
     
     
     
     
     