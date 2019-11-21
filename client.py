import socket
my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))
message = raw_input('Enter some data: ')
my_socket.send(message)
response_data = my_socket.recv(1024)
print("Received: %s" % response_data)
my_socket.close
