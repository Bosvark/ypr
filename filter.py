import math

sampleRepetition = 500
PI = 3.142857143

# Gyro values
gyroSensitivity = 57.142857143
gyroOdr = 760.0
gyro_x_min = 0
gyro_x_max = 0
gyro_y_min = 0
gyro_y_max = 0
gyro_z_min = 0
gyro_z_max = 0
gyro_x_dc_offset = 0
gyro_y_dc_offset = 0
gyro_z_dc_offset = 0
noise_x = 0
noise_y = 0
noise_z = 0
angle_x = 0
angle_y = 0
angle_z = 0


# Accelerometer values
accSensitivty = 1000.0#0.001
accOdr = 400.0
acc_x = 0.0
acc_y = 0.0
acc_z = 0.0
acc_x_min = 0.0
acc_x_max = 0.0
acc_y_min = 0.0
acc_y_max = 0.0
acc_z_min = 0.0
acc_z_max = 0.0
acc_x_dc_offset = 0.0
acc_y_dc_offset = 0.0
acc_z_dc_offset = 0.0
acc_noise_x = 0.0
acc_noise_y = 0.0
acc_noise_z = 0.0

def calc_noise(current_level, value):
    noise=0
    
    if value > current_level:
        noise = value
        return noise
    
    if value < -current_level:
        noise = -value
        return noise
    
    return current_level
    
def calibrate():
    global sampleRepetition
    global gyro_x_min
    global gyro_x_max
    global gyro_y_min
    global gyro_y_max
    global gyro_z_min
    global gyro_z_max
    global gyro_x_dc_offset
    global gyro_y_dc_offset
    global gyro_z_dc_offset
    global noise_x
    global noise_y
    global noise_z
    global acc_x_min
    global acc_x_max
    global acc_y_min
    global acc_y_max
    global acc_z_min
    global acc_z_max
    global acc_x_dc_offset
    global acc_y_dc_offset
    global acc_z_dc_offset
    global acc_noise_x
    global acc_noise_y
    global acc_noise_z
    
    logfile = open('raw.txt', 'r')

    # Calculate DC offset    
    for i in range(sampleRepetition):
        logline = logfile.readline()
        vals = logline.split()
        
        acc_raw_x = int(vals[0]) >> 4
        acc_raw_y = int(vals[1]) >> 4
        acc_raw_z = int(vals[2]) >> 4
        
        acc_x_dc_offset += acc_raw_x
        acc_y_dc_offset += acc_raw_y
        acc_z_dc_offset += acc_raw_z
        
        gyro_x_dc_offset += int(vals[3])
        gyro_y_dc_offset += int(vals[4])
        gyro_z_dc_offset += int(vals[5])
        
    acc_x_dc_offset = acc_x_dc_offset / sampleRepetition
    acc_y_dc_offset = acc_y_dc_offset / sampleRepetition
    acc_z_dc_offset = acc_z_dc_offset / sampleRepetition
    
    gyro_x_dc_offset = gyro_x_dc_offset / sampleRepetition
    gyro_y_dc_offset = gyro_y_dc_offset / sampleRepetition
    gyro_z_dc_offset = gyro_z_dc_offset / sampleRepetition
    
    logfile.seek(0) # Go back to the beginning of the file
    
    # Calculate noise level, using the DC offset
    for i in range(sampleRepetition):
        logline = logfile.readline()
        vals = logline.split()
        
        acc_raw_x = int(vals[0]) >> 4
        acc_raw_y = int(vals[1]) >> 4
        acc_raw_z = int(vals[2]) >> 4
        
        acc_x = acc_raw_x - acc_x_dc_offset
        acc_y = acc_raw_y - acc_y_dc_offset
        acc_z = acc_raw_z - acc_z_dc_offset
        
        if acc_x < acc_x_min: acc_x_min = acc_x 
        if acc_y < acc_y_min: acc_y_min = acc_y
        if acc_z < acc_z_min: acc_z_min = acc_z
        
        if acc_x > acc_x_max: acc_x_max = acc_x
        if acc_y > acc_y_max: acc_y_max = acc_y
        if acc_z > acc_z_max: acc_z_max = acc_z
        
        gyro_x = int(vals[3]) - gyro_x_dc_offset
        gyro_y = int(vals[4]) - gyro_y_dc_offset
        gyro_z = int(vals[5]) - gyro_z_dc_offset
        
        if gyro_x < gyro_x_min: gyro_x_min = gyro_x
        if gyro_y < gyro_y_min: gyro_y_min = gyro_y
        if gyro_z < gyro_z_min: gyro_z_min = gyro_z
        
        if gyro_x > gyro_x_max: gyro_x_max = gyro_x
        if gyro_y > gyro_y_max: gyro_y_max = gyro_y
        if gyro_z > gyro_z_max: gyro_z_max = gyro_z
        
        acc_noise_x = calc_noise(acc_noise_x, acc_x)
        acc_noise_y = calc_noise(acc_noise_y, acc_y)
        acc_noise_z = calc_noise(acc_noise_z, acc_z)

        noise_x = calc_noise(noise_x, gyro_x)
        noise_y = calc_noise(noise_y, gyro_y)
        noise_z = calc_noise(noise_z, gyro_z)
    
    logfile.close()
    
    print 'Gyro:'
    print '-----'
    print 'Min X:%d Max X:%d DC Offs X:%d Noise:%d'%(gyro_x_min,gyro_x_max,gyro_x_dc_offset,noise_x)
    print 'Min Y:%d Max Y:%d DC Offs Y:%d Noise:%d'%(gyro_y_min,gyro_y_max,gyro_y_dc_offset,noise_y)
    print 'Min Z:%d Max Z:%d DC Offs Z:%d Noise:%d'%(gyro_z_min,gyro_z_max,gyro_z_dc_offset,noise_z)

def filter():
    global sampleRepetition
    global PI
    global sensitivity
    global gyroOdr
    global gyro_x_min
    global gyro_x_max
    global gyro_y_min
    global gyro_y_max
    global gyro_z_min
    global gyro_z_max
    global gyro_x_dc_offset
    global gyro_y_dc_offset
    global gyro_z_dc_offset
    global noise_x
    global noise_y
    global noise_z
    global angle_x
    global angle_y
    global angle_z
    
    global accSensitivty
    global accOdr
    global acc_x
    global acc_y
    global acc_z
    global acc_x_min
    global acc_x_max
    global acc_y_min
    global acc_y_max
    global acc_z_min
    global acc_z_max
    global acc_x_dc_offset
    global acc_y_dc_offset
    global acc_z_dc_offset
    global acc_noise_x
    global acc_noise_y
    global acc_noise_z
    
    logfile = open('raw.txt', 'r')
    gyrofile = open('gyro.txt', 'w')
    gyrofile.truncate()
    
    accfile = open('acc.txt', 'w')
    accfile.truncate()
    
    compfile = open('comp.txt', 'w')
    compfile.truncate()
    
    yprfile = open('ypr.txt', 'w')
    yprfile.truncate()
    
    # Read past the calibration sample range
    for i in range(sampleRepetition):
        logfile.readline()
    
    prev_time = 0.0
    current_time = 0.0
    
    gyro_pitch = 0.0
    gyro_roll = 0.0
    comp_pitch = 0.0
    comp_roll = 0.0
    
    comp_x = 0.0
    comp_y = 0.0
    comp_z = 0.0
    
    count = 0
    
    while True:
        count += 1
        
        logline = logfile.readline()
        
        if logline == '':
            break
        
        vals = logline.split()
        
        if len(vals) < 11:
            break
        
        current_time = float(vals[9])/1000
        dt = current_time - prev_time
        prev_time = current_time
        
        acc_raw_x = int(vals[0])
        acc_raw_y = int(vals[1])
        acc_raw_z = int(vals[2])
        
        accScale = 16348
        acc_x = (float(acc_raw_x) - acc_x_dc_offset) / accScale
        acc_y = (float(acc_raw_y) - acc_y_dc_offset) / accScale
        acc_z = (float(acc_raw_z) - acc_z_dc_offset) / accScale
        
        out = '{0:4.8f} {1:4.8f} {2:4.8f}\n'.format(acc_x,acc_y,acc_z)
        accfile.write(out)
        
        gyroScale = 0.001
        gyro_x = (float(vals[3]) - gyro_x_dc_offset) * gyroScale
        gyro_y = (float(vals[4]) - gyro_y_dc_offset) * gyroScale
        gyro_z = (float(vals[5]) - gyro_z_dc_offset) * gyroScale
        
        out = '{0:4.8f} {1:4.8f} {2:4.8f}\n'.format(gyro_x, gyro_y, gyro_z)
        gyrofile.write(out)
        
        acc_pitch = math.atan(acc_x / math.sqrt(math.pow(acc_y, 2) + math.pow(acc_z, 2)))*180/PI
        gyro_pitch += gyro_x * dt
        
        acc_roll = math.atan(acc_y / math.sqrt(math.pow(acc_x, 2) + math.pow(acc_z, 2)))*180/PI
        gyro_roll -= gyro_y * dt
        
        #angle = (0.98)*(angle + gyro*dt) + (0.02)*(x_acc);
        alpha = 0.98
        comp_pitch = alpha * (comp_pitch + gyro_pitch * dt) + (1.0 - alpha) * acc_pitch
        comp_roll = alpha * (comp_roll + gyro_roll * dt) + (1.0 - alpha) * acc_roll
        
        out = '{0:4.8f} {1:4.8f} {2:4.8f} {3:4.8f} {4:4.8f}\n'.format(acc_pitch,gyro_pitch,comp_pitch,comp_roll,dt)
        yprfile.write(out)
        
        alpha = 0.98
        comp_x = alpha * (comp_x + gyro_x * dt) + (1.0 - alpha) * acc_x
        comp_y = alpha * (comp_y + gyro_y * dt) + (1.0 - alpha) * acc_y
        comp_z = alpha * (comp_z + gyro_z * dt) + (1.0 - alpha) * acc_z

        out = '{0:4.8f} {1:4.8f} {2:4.8f}\n'.format(comp_x, comp_y, comp_z)
        compfile.write(out)
        
    print '%d iterations from file\n'%(count)
    
    gyrofile.close()
    logfile.close()
    accfile.close()
    compfile.close()
    yprfile.close()

def main():
    calibrate()
    filter()
    
if __name__ == '__main__':
    main()