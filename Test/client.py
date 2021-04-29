import socket, threading, time

HOST = '127.0.0.1' #'176.23.70.52'
PORT = 12345
SERVER_ALIVE = False

SOCK = socket.socket()
SOCK.connect((HOST, PORT))
SOCK.sendto(("!brugernavn " + input("Vælg brugernavn: ")).encode(), (HOST, PORT))

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
        SOCK.sendto(data.encode(), (HOST, PORT))

SOCK.close()
