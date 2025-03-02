import socket, threading
import time 
from colorama import Fore, Back, Style

def handleMessage(connection: socket.socket):
	#Receive messages sent by the server, display to client.

	while True:
		try:
			'''1024-byte buffer is the optimal  size when working with various string sizes, 
			it'll only consume 1 chunk. '''
			msg = connection.recv(1024)

			#If no message, connection closed
			if msg:
				print(msg.decode())
			else:
				connection.closed()
				break

		except Exception as e:
			print(f'Error from server: {e}')
			connection.close()
			break

def client():
	#Main client process for server conn and message handling.
	serverADDRESS = str(input('Enter host address:	'))
	serverPORT = int(input('Enter port:	'))
	userName = input('Enter name: ')

	try:
		#Instance the socket and start conn
		socketInstance = socket.socket()
		socketInstance.connect((serverADDRESS, serverPORT))
		#Start thread for message handling
		threading.Thread(target=handleMessage, args=[socketInstance]).start()

		print(f'[*] {userName} [*] connected to chat.')

		#Take user input until quit then close conn.
		msg = input('> ')

		while True:
			if msg == 'quit':
				break
				
			#Parse messages to utf-8
			socketInstance.send(msg.encode())

	except Exception as e:
		print(f'Error connecting {e}')
		socketInstance.close()

if __name__ == '__main__':
	client()
		