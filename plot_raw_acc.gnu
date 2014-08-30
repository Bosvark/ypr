set title "Sensor Data"
set yrange[-32765:32767]
plot "raw.txt" using 0:1 with lines,\
"raw.txt" using 0:2 with lines,\
"raw.txt" using 0:3 with lines;
pause -1
