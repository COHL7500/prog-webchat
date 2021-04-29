import socket, threading, time

HOST = '0.0.0.0' #'176.23.70.52'
PORT = 27015
SERVER_ALIVE = False
SOCK = socket.socket()
SOCK.connect((HOST, PORT))

def do_encrypt(message):
    obj = AES.new('key123'), AES.MODE_CBC, 'IV456')
    message = obj.encrypt(message)
    return message

SOCK.sendto(("!brugernavn " + do_encrypt(input("Vælg brugernavn: ")).encode()), (HOST, PORT))

class server:
    def __init__(self):
        self.toggle_state()
        self.thread = threading.Thread(target=self.server_aflytter)
        self.thread.start()

    def __del__(self):
        self.thread.should_abort_immediately = True

    def server_aflytter(self):
        while True:
            try:
                data = SOCK.recv(1024)
                
            except:
                print("Serveren afsluttede forbindelsen!")
                self.toggle_state()
                break;

            print(data.decode())

        del self

    def toggle_state(self):
        global SERVER_ALIVE
        SERVER_ALIVE = not SERVER_ALIVE
        
server()
time.sleep(1)

while True:
    data = input(">> ")
    
    if data == "!afslut" or not SERVER_ALIVE:
        break
    
    elif(SERVER_ALIVE):
        SOCK.sendto(do_encrypt(data.encode()), (HOST, PORT))

SOCK.close()
