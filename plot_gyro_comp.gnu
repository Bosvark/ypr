set title "Sensor Data"
set xrange[500:]
plot "comp.txt" using 0:1 with lines,\
"comp.txt" using 0:2 with lines,\
"comp.txt" using 0:3 with lines,\
"gyro.txt" using 0:1 with lines,\
"gyro.txt" using 0:2 with lines,\
"gyro.txt" using 0:3 with lines,\
"acc.txt" using 0:1 with lines,\
"acc.txt" using 0:2 with lines,\
"acc.txt" using 0:3 with lines;

pause -1
