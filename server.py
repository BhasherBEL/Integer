import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Server started')

UDP_NETWORK_OUT = ('127.0.0.1', 5000)
UDP_NETWORK_IN = ('127.0.0.1', 5001)

server.bind(UDP_NETWORK_IN)
server.setblocking(False)

print("Target: %s:%s" % UDP_NETWORK_OUT)

isRunning = True

while isRunning:
    userInput = input('%s:%s < ' % UDP_NETWORK_OUT)
    if userInput.lower() in ['close', 'leave', 'exit']:
        isRunning = False
        continue
    server.sendto(userInput.encode(), UDP_NETWORK_OUT)
    print('waiting for response ...', end='\r')
    answer = select.select([server], [], [], 5)
    if answer[0]:
        try:
            data, addr = server.recvfrom(1024)
        except ConnectionResetError as e:
            print('%s:%s' % UDP_NETWORK_IN, 'not connected')
        else:
            print('%s:%s >' % addr, data.decode())
    else:
        print('No response received    ')

print('Server has been stopped')
server.close()
