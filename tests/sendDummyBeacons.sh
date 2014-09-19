# send some beacons from (4,1) of RSSI about -80, TX -50
echo '0101000400015032' | xxd -r -p | nc localhost 31000
echo '0101000400015132' | xxd -r -p | nc localhost 31000
echo '0101000400015232' | xxd -r -p | nc localhost 31000
echo '0101000400014F32' | xxd -r -p | nc localhost 31000
echo '0101000400015332' | xxd -r -p | nc localhost 31000

# send some beacons from (4,2) of RSSI about -70, TX -50
echo '0101000400024632' | xxd -r -p | nc localhost 31000
echo '0101000400024732' | xxd -r -p | nc localhost 31000
echo '0101000400024632' | xxd -r -p | nc localhost 31000
echo '0101000400024832' | xxd -r -p | nc localhost 31000
echo '0101000400024532' | xxd -r -p | nc localhost 31000


# send some beacons from (4,3) of RSSI about -90, TX -50
echo '0101000400035A32' | xxd -r -p | nc localhost 31000
echo '0101000400035B32' | xxd -r -p | nc localhost 31000
echo '0101000400035A32' | xxd -r -p | nc localhost 31000
echo '0101000400035C32' | xxd -r -p | nc localhost 31000
echo '0101000400035B32' | xxd -r -p | nc localhost 31000


