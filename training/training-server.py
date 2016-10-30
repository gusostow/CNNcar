import numpy as np
import cv2
import socket
import struct
import io
import pygame


class CollectTrainingData(object):

	def __init__(self):
		self.server_socket = socket.socket()

		#sets host as this computer's local ip
		host = socket.gethostbyname(socket.gethostname())
		port = 8033
		self.server_socket.bind((host, port))
		self.server_socket.listen(0)
		print "WAITING FOR CONNECTION FROM PI..."

		# accept a single connection
		self.connection = self.server_socket.accept()[0].makefile('rb')
		print "PI CONNECTED"

		#create labels matrix. each row corresponds to a "one hot encoded" command
		self.labels = np.eye(5,5)
		#call the collect images method after CollectTrainingData is first initialized
		self.CollectImages()


	def CollectImages(self):
		pygame.init()
		pygame.key.set_repeat(200, 200)

		frame_count = 0
		print "COLLECTING IMAGES..."
		print "-----"

		image_array = np.zeros((1, 230400))
		label_array = np.zeros((1, 5), 'float')

		# stream video frames one by one
		try:
			image_stream = io.BytesIO()

			total_frame_count = 0
			saved_frame_count = 0

			running = True

			while running:

				image_len = struct.unpack('<L' , self.connection.read(struct.calcsize('<L')))[0]


				image_stream.write(self.connection.read(image_len))
				image_stream.seek(0)
				captured_bytes = image_stream.read(image_len)

				temp_image_array = np.frombuffer(captured_bytes, dtype=np.uint8)

				#handles keyboard input
				events = pygame.event.get()
				for event in events:
					key_input = pygame.key.get_pressed()
					if event.type == pygame.KEYDOWN:

						if key_input[pygame.K_ESCAPE]:
							running = False

						#complex events
						if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
							print("Forward Right")
							image_array = np.vstack((image_array, temp_image_array))
							label_array = np.vstack((label_array, self.labels[0, :]))
							saved_frame_count += 1

						elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
							print("Forward Left")
							image_array = np.vstack((image_array, temp_image_array))
							label_array = np.vstack((label_array, self.labels[1, :]))
							saved_frame_count += 1

						elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
							print("Reverse Right")


						elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
							print("Reverse Left")


						elif key_input[pygame.K_UP]:
							print("Forward")
							image_array = np.vstack((image_array, temp_image_array))
							label_array = np.vstack((label_array, self.labels[2, :]))
							saved_frame_count += 1

						elif key_input[pygame.K_DOWN]:
							print("Reverse")

						elif key_input[pygame.K_RIGHT]:
							print("Right")
							image_array = np.vstack((image_array, temp_image_array))
							label_array = np.vstack((label_array, self.labels[3, :]))
							saved_frame_count += 1

						elif key_input[pygame.K_LEFT]:
							print("Left")
							image_array = np.vstack((image_array, temp_image_array))
							label_array = np.vstack((label_array, self.labels[4, :]))
							saved_frame_count += 1

				total_frame_count += 1
				print "frames saved: ", saved_frame_count
				if not total_frame_count % 50:
					print "total frame count: ", total_frame_count

		finally:

			train = image_array[1:, :]
			train_labels = label_array[1:, :]
			print train.shape
			np.savez('training-data/test.npz', train=train, train_labels=train_labels)

			self.connection.close()
			self.server_socket.close()

CollectTrainingData()


