import socket
ClientMultiSocket = socket.socket()
host = os.getenv("HOST_IP")
port = 2004

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

print("\n")
word=input("After hiding the painting in his __ for two years, he grew __ and tried to sell it to a/an __ in Florence, but was caught.\n \nEnter the words:")
ClientMultiSocket.send(word.encode())
sentence = ClientMultiSocket.recv(1024)
print(sentence.decode())
print("--------------------------------------------------------------------------------------------------------------------")
coins_string=input("Enter the crypto names: ")
ClientMultiSocket.send(coins_string.encode())
cryto_price=ClientMultiSocket.recv(1024)
print(cryto_price.decode())
print("--------------------------------------------------------------------------------------------------------------------")
city=input("Enter the city name to find weather: ")
ClientMultiSocket.send(city.encode())
weather=ClientMultiSocket.recv(1024)
print(weather.decode())
print("--------------------------------------------------------------------------------------------------------------------")

    
ClientMultiSocket.close()