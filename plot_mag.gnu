set title "Sensor Data"
#set xrange[0:200]
plot "raw.txt" using 0:7 with lines,\
"raw.txt" using 0:8 with lines,\
"raw.txt" using 0:9 with lines;
pause -1
