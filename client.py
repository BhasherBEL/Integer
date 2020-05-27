import socket
import select
import subprocess

UDP_NETWORK_IN = ('192.168.1.58', 5000)
UDP_NETWORK_OUT = ('192.168.1.58', 5001)

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

        print('[DEBUG] > ', content)

        if '::' in content:
            splitContent = content.split('::')
            if len(splitContent) != 2:
                client.sendto('Invalid request'.encode(), UDP_NETWORK_OUT)
            elif splitContent[0].lower() == 'text':
                print(splitContent[1])
                client.sendto('Text successfully printed'.encode(), UDP_NETWORK_OUT)
            elif splitContent[0].lower() == 'run':
                process = subprocess.run(splitContent[1].split(' '), capture_output=True)
                text = process.stdout if len(process.stdout) > 0 else process.stderr
                client.sendto(text, UDP_NETWORK_OUT)
            elif splitContent[0].lower() == 'client':
                if splitContent[1].lower() == 'stop':
                    isRunning = False
                    client.sendto('Client stopped'.encode(), UDP_NETWORK_OUT)
                    continue
                elif splitContent[1].lower() == 'isonline':
                    client.sendto('True'.encode(), UDP_NETWORK_OUT)
        else:
            client.sendto('Invalid request'.encode(), UDP_NETWORK_OUT)

print('Client has been closed')
client.close()
