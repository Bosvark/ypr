from visual import *
import serial
import binascii
import struct

port = "/dev/ttyACM0"

arrow_length = 100.0

x_arrow = arrow(pos=(0,0,0), axis=(arrow_length,0,0), shaftwidth=1,color=color.red)
y_arrow = arrow(pos=(0,0,0), axis=(0,arrow_length,0), shaftwidth=1,color=color.green)
z_arrow = arrow(pos=(0,0,0), axis=(0,0,arrow_length), shaftwidth=1,color=color.yellow)

redbox=box(pos=vector(0,0,0),size=(65,1,97),color=color.red)

serial_port = serial.Serial()
serial_port.port = port
serial_port.baudrate=115200
serial_port.parity=serial.PARITY_NONE
serial_port.stopbits=serial.STOPBITS_ONE
serial_port.bytesize=serial.EIGHTBITS

try:
	serial_port.open()
except serial.SerialException as e:
	print str(e)
	exit(-1)

loop_count = 30
    
while True:
	serial_port.write('a'+chr(loop_count))

	for i in range(loop_count):
		while serial_port.inWaiting() > 0:
			rx = serial_port.readline()
			vals = rx.split(",")
			yaw = struct.unpack('f', binascii.unhexlify(vals[0]))
			pitch = struct.unpack('f', binascii.unhexlify(vals[1]))
			roll = struct.unpack('f', binascii.unhexlify(vals[2]))
			print "Yaw={0:4.8f} Pitch={1:4.8f} Roll={2:4.8f}".format(yaw[0], pitch[0], roll[0])

			fyaw = yaw[0] * pi/180.0
			fpitch = pitch[0] * pi/180.0
			froll = -roll[0] * pi/180.0

			x_arrow.axis=(arrow_length*cos(fpitch),  arrow_length*sin(fpitch), arrow_length*sin(froll))
			y_arrow.axis=(arrow_length*sin(-fpitch), arrow_length*cos(fpitch), arrow_length*sin(-froll))
			z_arrow.axis=(arrow_length*sin(-froll),  arrow_length*sin(froll),  arrow_length*cos(froll))

