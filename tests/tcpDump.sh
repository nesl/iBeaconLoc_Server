while true; do
	nc -l 0.0.0.0 31000 | xxd
	sleep 0.1
done