set title "Sensor Data"
set xrange[500:]
plot "ypr.txt" using 0:1 with lines,\
"ypr.txt" using 0:2 with lines,\
"ypr.txt" using 0:3 with lines,\
"ypr.txt" using 0:4 with lines;
pause -1
