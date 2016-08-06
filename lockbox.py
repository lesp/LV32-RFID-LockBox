#! /usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522
from time import sleep
GPIO.setmode(GPIO.BOARD)
LED = 8
BUZZER = 10
GPIO.setup(11,GPIO.OUT)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)

pwm=GPIO.PWM(11,50)

continue_reading = True
locked = True
MIFAREReader = MFRC522.MFRC522()

try:
	pwm.start(5)
	for i in range(2):
		GPIO.output(BUZZER, True)
		sleep(0.1)
		GPIO.output(BUZZER, False)
		sleep(0.1)
	print("Please present your RFID card to the reader - this can only be seen in debug")
	while continue_reading == True:
		GPIO.output(LED, True)
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
		sleep(0.5)
		if status == MIFAREReader.MI_OK:
			print("Card detected")
			(status,uid) = MIFAREReader.MFRC522_Anticoll()
			print(uid)
			if uid == [195, 87, 55, 213, 118]:
				print("KEY DETECTED")
				if locked == True:
					locked = False
					pwm.start(5)
				elif locked == False:
					locked = True
					pwm.ChangeDutyCycle(10)
			else:
				print("ALERT ALERT ALERT")
				for i in range(3):
					GPIO.output(LED, True)
					GPIO.output(BUZZER, True)
					sleep(0.2)
					GPIO.output(LED, False)
					GPIO.output(BUZZER, False)
					sleep(0.2)
except KeyboardInterrupt:
	continue_reading = False
	GPIO.cleanup()
	print("\nExiting the application")
