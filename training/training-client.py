import io
import socket
import struct
import time
import picamera
from picamera.array import PiRGBArray, PiArrayOutput, bytes_to_rgb

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(("192.168.1.164", 8033))
print "connected to laptop"

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 10
        # Start a preview and let the camera warm up for 2 seconds
        time.sleep(2)
        start = time.time()
        stream = PiArrayOutput(camera, (320, 240))
        "TRAINING MODE ACTIVATED"
        
        for foo in camera.capture_continuous(stream, 'rgb', use_video_port=True ):
            
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
    

            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            connection.flush()
            
            # Reset the stream for the next capture
            stream.truncate()
            stream.seek(0)

    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
