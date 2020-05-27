import socket
import select

UDP_NETWORK_IN = ('127.0.0.1', 5000)
UDP_NETWORK_OUT = ('127.0.0.1', 5001)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Client started')

client.bind(UDP_NETWORK_IN)

isRunning = True

while isRunning:
    print('listening %s:%s' % UDP_NETWORK_IN)
    ready = select.select([client], [], [], 10)
    if ready[0]:
        data, addr = client.recvfrom(1024)
        content = data.decode()

        print('>', content)

        client.sendto('Success'.encode(), UDP_NETWORK_OUT)

        if content == 'stop':
            isRunning = False
            continue

print('Client has been closed')
client.close()
