## IoT application

This project simply serves up a web page on port `:80` of the balena device(Pi2).

In your browser you should be able to open the device URL and perfom the following fuctions:

• Sensor On: Turn on the sensors
• Sensor Off: Turn off the sensors
• Status: To check status of the Pi using sensors to collect the data
• Log Check: This function print out the last 10 samples from the current run to the screen.
• Log download: Allows the user to download the current sensorlog file.
• Exit: This fuction exits the server program.

There are two devices on this project(which communicate with each other):

Pi1: Client collecting Data From the sonsors(Temparature sensor and Light sensor)
Pi2: Server serving  web page to the user(mentioned above)


