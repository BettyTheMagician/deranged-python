#Imports
import socket, threading
import time 
from colorama import Fore, Back, Style

#Global Variable to maintain user conn
connections = []

def handleUserConnection(connection: socket.socket, address:str) -> None:
	#Get users connection to ensure messages are being sent.

	while True:
		try:
			#Receive message
			msg = connection.recv(1024)

			#If there's an error with the message, it's possible that the conn has ended.
			if msg:
				#Log message
				print(f'{address[0]}:{address[1]} - {msg.decode()}')

				#Message format and broadcast
				msgtoSend = f'From {address[0]}:{address[1]} - {msg.decode()}'
				broadcast(msgtoSend, connection)

			#Close conn if not sent
			else:
				removeConnection(connection)
				break

		except Exception as e:
			print(Fore.RED + f'Error handling user connection: {e}')
			removeConnection(connection)
			break

def broadcast(message: str, connection: socket.socket) -> None:
	#Broadcast message to all users connected to the server

	#Iterate on connections to send message to all clients connected
	for clientConn in connections:
		#Check if isn't the connection of who's send
		if clientConn != connection:
			try:
				#Sending message to client connection
				clientConn.send(message.encode())

			#If fails, there is a chance the socket has died.
			except Exception as e:
				print(Fore.RED + 'Error broadcasting message: {e}')
			finally:
				removeConnection(clientConn)

def removeConnection(conn: socket.socket) -> None:
	#Remove specified connection from conns
	#Confirm connection is live
	if conn in connections:
		#Not only removing connection but closing socket.
		conn.close()
		connections.remove(conn)

def server() -> None:
	'''Main process, will receive clients and also create their threads,
		to handle messages	
	'''
	print(Fore.RED + 'ENSURE PORT IS OPEN AND NOT IN USE! (Preferably over 10000)')
	hostName = str(input('Enter host IP: '))
	ListeningPORT = int(input('Enter port you wish you use:	'))
	clients_Userinput = int(input('Enter how many clients you would like please: '))

	
	try:
		socketInstance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketInstance.bind((hostName, ListeningPORT))
		socketInstance.listen(clients_Userinput)
		
		#Log Server status
		print('Server running')

		while True:

			#Accept clients
			socketConnection, address = socketInstance.accept()
			#Append client to list
			connections.append(socketConnection)
			#Begin threading for clients connection and message handling and to send to others connections
			threading.Thread(target=handleUserConnection, args=[socketConnection, address]).start()

	except Exception as e:
		print(f'Failure instancing socket: {e}')
	finally:
		#If a problem arises, we'll close the server connection
		if len(connections) > 0:
			for conn in connections:
				removeConnection(conn)

		socketInstance.close()

if __name__ == '__main__':
	server()