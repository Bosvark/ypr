import atexit
import sys
import serial
import time
import binascii
import struct

version = '1.0'

serial_port = None

def init_serial(port, command, logfile):
    global serial_port
    
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
        return
        
    print '%s is open'%(port)
    
    if len(logfile):
        dataFile = open(logfile, 'w')
    
    if command == 'q':
        loop_count = 30
    
        while True:
            serial_port.write('q'+chr(loop_count))
            
            for i in range(loop_count):
                while serial_port.inWaiting() > 0:
                    rx = serial_port.readline()
                    vals = rx.split(",")
                    q0 = struct.unpack('f', binascii.unhexlify(vals[0]))
                    q1 = struct.unpack('f', binascii.unhexlify(vals[1]))
                    q2 = struct.unpack('f', binascii.unhexlify(vals[2]))
                    q3 = struct.unpack('f', binascii.unhexlify(vals[3]))
                    print "{0:4.8f} {1:4.8f} {2:4.8f} {3:4.8f}".format(q0[0], q1[0], q2[0], q3[0])
    elif command == 'a':
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
    elif command == 'r':
   
        while True:
            serial_port.write('r')
            
            out = ''
            while serial_port.inWaiting() > 0:
                rx = serial_port.readline()
                vals = rx.split(",")
                
                out = ''
                for v in vals:
                    out += '%s '%v
                    
                print out
            
            if len(logfile):
                dataFile.write(out)
    else:
        print ' No command specified\n'
        
    dataFile.close()
        
def info():
    print 'ypr version '+version+'\n'
    print 'Expected serial port as an argument\n'
     
def main():
    argc = len(sys.argv)
    
    if argc != 2:
        info()
        return
    
    print 'args %d [%s]\n'%(argc,sys.argv[1])
    
    logfile = 'raw.txt'
    init_serial(sys.argv[1], 'r', logfile)
#    init_serial(sys.argv[1], 'r', '')
    
def exit_handler():
    if serial_port.isOpen():
        serial_port.close()
        print '%s is closed'%(serial_port.port)
    print 'My application is ending!'
    
if __name__ == '__main__':
    atexit.register(exit_handler)
    main()
    