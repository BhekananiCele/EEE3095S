## IoT application

This project simply serves up a web page on port `:80` of the balena device(Pi2).

#In your browser you should be able to open the device URL and perfom the following fuctions:

1. Sensor On: Turn on the sensors
2. Sensor Off: Turn off the sensors
3. Status: To check status of the Pi using sensors to collect the data
4. Log Check: This function print out the last 10 samples from the current run to the screen.
5. Log download: Allows the user to download the current sensorlog file.
6. Exit: This fuction exits the server program.

#There are two devices on this project(which communicate with each other):

1. Pi1: Client collecting Data From the sonsors(Temparature sensor and Light sensor)
2. Pi2: Server serving  web page to the user(mentioned above)


