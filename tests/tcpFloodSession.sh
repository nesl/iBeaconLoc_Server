var=1
while true; do
	var=$((var+1))
	echo $var | nc 192.168.2.2 31000
	sleep 0.01
done
