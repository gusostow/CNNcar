import pygame
import serial

pygame.init()
pygame.key.set_repeat(200, 200)

running = True

ser = serial.Serial('/dev/tty.usbmodem1411', 115200, timeout=1)

while running:
#handles keyboard input
    events = pygame.event.get()

    for event in events:
        key_input = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:

            if key_input[pygame.K_ESCAPE]:
                running = False

            elif key_input[pygame.K_UP]:
                print("Forward")
                ser.write(chr(1))

            elif key_input[pygame.K_DOWN]:
                print("Reverse")
                ser.write(chr(2))

            elif key_input[pygame.K_RIGHT]:
                print("Right")

            elif key_input[pygame.K_LEFT]:
                print("Left")

ser.close()
