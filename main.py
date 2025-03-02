from server import server
from client import client
from colorama import Fore, Back, Style
import os

#https://pypi.org/project/bitcoinrpc/ Future referencing for handling BTC payments.

#Creating Graphics for terminal window.
def banner() -> None:
	topBanner = '''
         ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
         ┃                        ┃                                                                                                                                                                                                                               
         ┃       TermaChat        ┃
         ┃       Version 1.0      ┃
         ┃                        ┃
         ┗━━━━━━━━━━━━━━━━━━━━━━━━┛

'''    
	print(topBanner)                                                             

def Userinterface() -> bool:
	banner()
	choice = input(Fore.GREEN + 'Do you wish to host or connect? c/s:  ')
	if choice == 'c':
		client()
	elif choice == 's':
		server()
	else:
		print(Fore.RED + 'Invalid Choice, please try again.')

def main() -> None:
	while True:
		try:
			Userinterface()
		except Exception as e:
			print(Fore.RED + 'An error occurred {e}')


if __name__ == '__main__':
	main()





