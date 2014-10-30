# send some beacons from (4,1) of RSSI about -80, TX -74
echo '010100040001B0B6' | xxd -r -p | nc localhost 31000
echo '010100040001B1B6' | xxd -r -p | nc localhost 31000
echo '010100040001B0B6' | xxd -r -p | nc localhost 31000
echo '010100040001B0B6' | xxd -r -p | nc localhost 31000
echo '010100040001B2B6' | xxd -r -p | nc localhost 31000

# send some beacons from (4,2) of RSSI about -85, TX -50
echo '010100040002ABB6' | xxd -r -p | nc localhost 31000
echo '010100040002ABB6' | xxd -r -p | nc localhost 31000
echo '010100040002ACB6' | xxd -r -p | nc localhost 31000
echo '010100040002ABB6' | xxd -r -p | nc localhost 31000
echo '010100040002ABB6' | xxd -r -p | nc localhost 31000


# send some beacons from (4,3) of RSSI about -90, TX -50
echo '010100040003A6B6' | xxd -r -p | nc localhost 31000
echo '010100040003A6B6' | xxd -r -p | nc localhost 31000
echo '010100040003A7B6' | xxd -r -p | nc localhost 31000
echo '010100040003A3B6' | xxd -r -p | nc localhost 31000
echo '010100040003A3B6' | xxd -r -p | nc localhost 31000


