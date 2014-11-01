#!/usr/bin/ruby

require 'socket'

s = TCPSocket.new 'localhost', 31000
var = 0

while true # Read lines from socket
  s.puts var         # and print them
  var = var + 1
  sleep(0.1)
end

s.close             # close socket when done