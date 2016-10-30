## Training overview

During training mode, the human driver controls the RC car via the laptop keyboard to collect data. These data are video frames captured  by the car’s onboard picamera and the driver’s steering commands. The raspberry pi continuously captures and transmits frames wirelessly to the laptop. Every time the driver makes a steering command, both the current frame and that particular command are saved to numpy matrices. Only video frames that are associated with a steering command are saved.

**Directions:** Run training-server.py on laptop first, then training-client.py on the pi. Control the car with the laptop's arrow keys. After a session, training data is saved as pickled numpy arrays in the training-data folder.

### Laptop training-server.py sript

The laptop has two main functions during training: send steering commands to the car and save training data as numpy matrices.

As soon as the CollectTrainingData class is initialized, it sets up the laptop to be a TCP server so it can receive video frames from the pi onboard the car. The laptop listens for a connection from the pi on a specific host and port. The script automatically sets the host to the laptop’s local ip address. The port can pretty much be set as any 4-digit number. Both are important to note because they have to match in the pi’s training script to be able to connect.

After the pi connects to the laptop, the CollectImages method starts and the driver can begin operating the car with the keyboard arrow keys. The laptop is now receiving video frames one by one from the pi. Every frame needs to be temporarily saved and decoded into an unraveled numpy matrix (so instead of 320x240x3, it’s saved as a flattened 230,400 vector). If the driver is currently making a steering command (pressing an arrow key) the script saves the temporary frame, otherwise it is discarded when as the process moves to the next streamed frame.

The CollectImages method uses a module called pygame to handle keyboard input. Although it was designed for computer games, it works just fine for controlling an RC car IRL. Every time pygame detects a keypress three things happen:

1. The current, temporary video frame is saved to a more permanent image data matrix.

2. A vector corresponding to that specific steering action is saved to a steering data matrix.

3. The laptop sends the steering command over usb to the arduino chip to simulate that button press from the remote control. This step actually controls the car, which is important.


### Pi training-client.py script

The role of the pi is simple: passively stream video frames to the laptop as a TCP client.

Before the pi can connect to the laptop server, the host and the port need to match the training-server script. Change these here: `client_socket.connect(("192.168.1.164", 8033))`. The host address is your laptop's local ip address (you can find it by typing `ifconfig` into terminal on the laptop). The port is whatever 4-digit number you chose in the training-server script.

Picamera has a module that allows you to capture video frames continuously as numpy arrays to a stream. Here is more information on the [picamera.array module](http://picamera.readthedocs.io/en/release-1.10/api_array.html) and [capturing to a network stream](http://picamera.readthedocs.io/en/release-1.10/recipes1.html#capturing-to-a-network-stream).


## Credit

I lifted the pipeline design and training code heavily from https://github.com/hamuchiwa/AutoRCCar.

