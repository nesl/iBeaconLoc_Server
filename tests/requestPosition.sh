# request position for user 1
resp=`echo '0201' | xxd -r -p | nc localhost 31000`
unpacked=`echo $resp | perl -lpe 'unpack("ff", $1)'`
echo "received packet: " $unpacked

