# _iBeacon-Based Indoor Localization Server_

_Description: For use with Android-based indoor localization demo_

## Project Setup

_How do you start?_ 

1. _Make sure you have python 3.2+ installed_
2. _Make sure you have the modules listed at the top of StartServer.py_
3. _Run the upper level script using \<Python3Interpreter\> StartServer.py \<port\_number\>_

## Testing

_How do test the server?_

1. _Make sure you have netcat installed_
2. _Run $ echo '01020304050607' | xxd -r -p | nc localhost \<port\_number\>_ to send a dummy beacon report

## License