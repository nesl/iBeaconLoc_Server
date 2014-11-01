var=1
while true; do
	var=$((var+1))
	echo $var | nc -u 172.17.5.253 31000
	sleep 0.01
done
