from os import stat
from flask import Flask, send_file, render_template, redirect, url_for
from Server import *
import csv
app = Flask(__name__, template_folder="template", static_folder='static')

#Status of the sonsors variables
statusOnline = """<div name="status" style="display: inline-block" class="status-online">Sensors On</div>"""
statusOffline = """<div name="status" style="display: inline-block" class="status-offline">Sensors Off</div>"""  

#Function that return the offline text
def offline():
    offline = """<pre>

8888888b.                    d8b                         d8b                          .d888  .d888 888 d8b                   
888  "Y88b                   Y8P                         Y8P                         d88P"  d88P"  888 Y8P                   
888    888                                                                           888    888    888                       
888    888  .d88b.  888  888 888  .d8888b  .d88b.        888 .d8888b         .d88b.  888888 888888 888 888 88888b.   .d88b.  
888    888 d8P  Y8b 888  888 888 d88P"    d8P  Y8b       888 88K            d88""88b 888    888    888 888 888 "88b d8P  Y8b 
888    888 88888888 Y88  88P 888 888      88888888       888 "Y8888b.       888  888 888    888    888 888 888  888 88888888 
888  .d88P Y8b.      Y8bd8P  888 Y88b.    Y8b.           888      X88       Y88..88P 888    888    888 888 888  888 Y8b.     
8888888P"   "Y8888    Y88P   888  "Y8888P  "Y8888        888  88888P'        "Y88P"  888    888    888 888 888  888  "Y8888  
                                                                                               
</pre>"""
    return offline
    
#Sensors On Route    
@app.route("/SensorOn", methods=['POST'])
def SensonOn():
    results = sendDataToClient(SENDON)
    if(results!="Done"):
        return render_template('Index.html', body=offline(), status=getStatus())
    
    body = """<pre>
   _____                                                                                                                  
  / ____|                                                                                                                 
 | (___     ___   _ __    ___    ___    _ __   ___      __ _   _ __    ___     _ __     ___   __      __     ___    _ __  
  \___ \   / _ \ | '_ \  / __|  / _ \  | '__| / __|    / _` | | '__|  / _ \   | '_ \   / _ \  \ \ /\ / /    / _ \  | '_ \ 
  ____) | |  __/ | | | | \__ \ | (_) | | |    \__ \   | (_| | | |    |  __/   | | | | | (_) |  \ V  V /    | (_) | | | | |
 |_____/   \___| |_| |_| |___/  \___/  |_|    |___/    \__,_| |_|     \___|   |_| |_|  \___/    \_/\_/      \___/  |_| |_|

</pre>"""
    return render_template('Index.html', body=body, status=getStatus())

#Sensors Off Route      
@app.route("/SensorOff", methods=['POST'])
def SensonOFF():
    results = sendDataToClient(SENDOFF)
    if(results!="Done"):
        return render_template('Index.html', body=offline(), status=getStatus())
    body = """<pre>
   _____                                                                                                             __    __ 
  / ____|                                                                                                           / _|  / _|
 | (___     ___   _ __    ___    ___    _ __   ___      __ _   _ __    ___     _ __     ___   __      __     ___   | |_  | |_ 
  \___ \   / _ \ | '_ \  / __|  / _ \  | '__| / __|    / _` | | '__|  / _ \   | '_ \   / _ \  \ \ /\ / /    / _ \  |  _| |  _|
  ____) | |  __/ | | | | \__ \ | (_) | | |    \__ \   | (_| | | |    |  __/   | | | | | (_) |  \ V  V /    | (_) | | |   | |  
 |_____/   \___| |_| |_| |___/  \___/  |_|    |___/    \__,_| |_|     \___|   |_| |_|  \___/    \_/\_/      \___/  |_|   |_|  
                                                                                                               
 </pre>"""
    return render_template('Index.html', body=body, status=getStatus())

#Status Route      
@app.route("/Status", methods=['POST'])
def Status():
    results=sendDataToClient(CHECK)
    if(results=="Offline"):
        return render_template('Index.html', body=offline(), status=getStatus())
    return render_template('Index.html', body=results, status=getStatus())

#Log check Route      
@app.route("/LogCheck", methods=['POST'])
def LogCheck():
    try:
        data = readDataFromFile(reversed=True)
        return render_template('Index.html', body=printData(data), status=getStatus())
    except:
        return render_template('Index.html', body="Failed to read log file, try again later.", status=getStatus())

#Log Download Route 
@app.route("/LogDownload", methods=['POST'])
def LogDownload():
    try:
        path = os.getcwd()+"/sensorlog.csv"
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)
        return render_template('Index.html', body="No Logs Have Been Made Yet!", status=getStatus())
        
#Exit Program Route 
@app.route("/Exit", methods=['POST'])
def Exit():
    
    body = """<pre> 
  _____                                                        _                       ______          _   _                _ 
 |  __ \                                                      | |                     |  ____|        (_) | |              | |
 | |__) |  _ __    ___     __ _   _ __    __ _   _ __ ___     | |__     __ _   ___    | |__    __  __  _  | |_    ___    __| |
 |  ___/  | '__|  / _ \   / _` | | '__|  / _` | | '_ ` _ \    | '_ \   / _` | / __|   |  __|   \ \/ / | | | __|  / _ \  / _` |
 | |      | |    | (_) | | (_| | | |    | (_| | | | | | | |   | | | | | (_| | \__ \   | |____   >  <  | | | |_  |  __/ | (_| |
 |_|      |_|     \___/   \__, | |_|     \__,_| |_| |_| |_|   |_| |_|  \__,_| |___/   |______| /_/\_\ |_|  \__|  \___|  \__,_|
                           __/ |                                                                                              
                          |___/                                                                                               
    
    </pre>"""
    return render_template('Exit.html', body=body)

#Home Route           
@app.route("/Home", methods=['POST'])  
@app.route('/')
def Index():
    body = """<pre>

 /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$
| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/
| $$ /$$$| $$| $$      | $$      | $$  \__/| $$  \ $$| $$$$  /$$$$| $$      
| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$   
| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/   
| $$$/ \  $$$| $$      | $$      | $$    $$| $$  | $$| $$\  $ | $$| $$      
| $$/   \  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$$$$$$$
|__/     \__/|________/|________/ \______/  \______/ |__/     |__/|________/
                                                                                                     
</pre>"""
    return render_template('Index.html', body=body, status=getStatus())

#Function that reads data from the log file 
def readDataFromFile(reversed=False):
    dataFromFile = []
    dataFromFileReversed = []
    header = True;
    try:
        file = "sensorlog.csv" 
        with open(file, 'r') as textfile:
            reader = csv.reader(textfile)
            for row in reader:
                if(header):
                    header = False
                    continue
                dataFromFile.append(row)
            if(reversed):
                count = 0 
                for row in dataFromFile[::-1]:
                    dataFromFileReversed.append(row)
                    count+=1
                    if(count>=10):
                        break
                return dataFromFileReversed
            return dataFromFile;  
    except Exception as e:
        if(reversed):
            return dataFromFileReversed
        return dataFromFile;  
 
#Function that checks the status of the client 
def getStatus():
    body=sendDataToClient(CHECK)
    status = statusOffline
    if(body.find("True")>=0):
        status = statusOnline
    return status

#Function that print the data to the screen
def printData(array):
    dataString= ""
    for data in array:
       dataString += """<tr>
                            <td style="text-align:left">"""+data[0]+"""</td>
                            <td style="text-align:left">"""+data[1]+"""</td>
                            <td style="text-align:left">"""+data[2]+"""</td>
                        </tr>"""
     
    return  """<table>
                <thead>
                    <tr>
                        <th style="padding-right: 20px">Temp Reading</th>
                        <th style="padding-right: 18px">Light Reading</th>
                        <th style="padding-right: 24px">Time Stamp</th>
                    </tr>
                </thead>
                <tbody>"""+ dataString +"""</tbody> 
            </table>"""
        
if __name__ == '__main__':
    print("Server Running")
    os.system("touch sensorlog.csv") 
    thread = threading.Thread(target=ListenToClients)
    thread.daemon = True
    thread.start()
    
    app.run(host='0.0.0.0', port=80)
     
    while True:
        pass
