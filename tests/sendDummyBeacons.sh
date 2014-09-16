# send some beacons from (4,10) of RSSI about -80, TX -50
echo '01010004000A5032' | xxd -r -p | nc localhost 31000
echo '01010004000A5132' | xxd -r -p | nc localhost 31000
echo '01010004000A5232' | xxd -r -p | nc localhost 31000
echo '01010004000A4F32' | xxd -r -p | nc localhost 31000
echo '01010004000A5332' | xxd -r -p | nc localhost 31000

# send some beacons from (4,20) of RSSI about -70, TX -50
echo '0101000400144632' | xxd -r -p | nc localhost 31000
echo '0101000400144732' | xxd -r -p | nc localhost 31000
echo '0101000400144632' | xxd -r -p | nc localhost 31000
echo '0101000400144832' | xxd -r -p | nc localhost 31000
echo '0101000400144532' | xxd -r -p | nc localhost 31000


# send some beacons from (4,30) of RSSI about -90, TX -50
echo '01010004001E5A32' | xxd -r -p | nc localhost 31000
echo '01010004001E5B32' | xxd -r -p | nc localhost 31000
echo '01010004001E5A32' | xxd -r -p | nc localhost 31000
echo '01010004001E5C32' | xxd -r -p | nc localhost 31000
echo '01010004001E5B32' | xxd -r -p | nc localhost 31000


