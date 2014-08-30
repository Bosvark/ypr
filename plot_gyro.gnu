set title "Sensor Data"
#set xrange[0:200]
plot "gyro.txt" using 0:1 with lines,\
"gyro.txt" using 0:2 with lines,\
"gyro.txt" using 0:3 with lines;
pause -1
