# send some beacons from (4,0) of RSSI about -80, TX -74
echo '010100040000B0B6' | xxd -r -p | nc localhost 31000
echo '010200040000B1B6' | xxd -r -p | nc localhost 31000
echo '010100040000B0B6' | xxd -r -p | nc localhost 31000
echo '010200040000B0B6' | xxd -r -p | nc localhost 31000
echo '010100040000B2B6' | xxd -r -p | nc localhost 31000

# send some beacons from (4,1) of RSSI about -85, TX -50
echo '010100040001ABB6' | xxd -r -p | nc localhost 31000
echo '010200040001ABB6' | xxd -r -p | nc localhost 31000
echo '010100040001ACB6' | xxd -r -p | nc localhost 31000
echo '010200040001ABB6' | xxd -r -p | nc localhost 31000
echo '010100040001ABB6' | xxd -r -p | nc localhost 31000


# send some beacons from (4,2) of RSSI about -90, TX -50
echo '010100040002A6B6' | xxd -r -p | nc localhost 31000
echo '010200040002A6B6' | xxd -r -p | nc localhost 31000
echo '010100040002A7B6' | xxd -r -p | nc localhost 31000
echo '010200040002A3B6' | xxd -r -p | nc localhost 31000
echo '010100040002A3B6' | xxd -r -p | nc localhost 31000


