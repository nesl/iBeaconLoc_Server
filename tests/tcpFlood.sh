var=1
while true; do
	var=$((var+1))
	echo $var | nc 172.17.5.61 31000
	sleep 0.01
done
