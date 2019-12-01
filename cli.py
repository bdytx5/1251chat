import socket
import time

UDP_IP = "128.206.19.255" # set it to destination IP.. RPi in this case
UDP_PORT = 8820

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
  print("Turn ON")
  sock.sendto(b'roy-by-ffdljkdfdf', (UDP_IP, UDP_PORT))
  time.sleep(2)
  print("Turn OFF")
  sock.sendto(b'by-roy-sdsdsddssdsdsdsd', (UDP_IP, UDP_PORT))
  time.sleep(2)
