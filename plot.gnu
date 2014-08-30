set title "Sensor Data"
#set xrange[0:200]
plot "raw.txt" using 0:1 with lines,\
"raw.txt" using 0:2 with lines,\
"raw.txt" using 0:3 with lines;
pause -1
