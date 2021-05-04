import socket, threading

class server:
    def __init__(self, host, port, parent):
        self.parent = parent
        self.forbind(host, port)
        
        if self.SERVER_ALIVE:
            self.thread = threading.Thread(target=self.server_aflytter)
            self.thread.start()
        
            self.parent.print("\nVælg brugernavn: ")

    def forbind(self, host, port):
        self.HOST = host
        self.PORT = int(port)
        self.SERVER_ALIVE = False
        
        self.SOCK = socket.socket()

        try:
            self.SOCK.connect((self.HOST, self.PORT))
            self.parent.print("Forbindelse til server etableret!\nSkriv '!hjælp' for hjælp.\n")
            self.toggle_status()
            
        except:
            self.parent.print("Kunne ikke oprette forbindelse til serveren!\n")

    def luk(self):
        self.SOCK.close()

        if hasattr(self, "thread"):
            self.thread.do_run = False

    def server_aflytter(self):
        while getattr(self.thread, "do_run", True):
            try:
                data = self.SOCK.recv(1024)
                
            except:
                self.parent.print("Forbindelsen med server afbrudt!\n")
                self.toggle_status()
                self.parent.set_ipport("normal")
                self.parent.set_input("disabled")
                self.parent.set_destroy("disable")
                del self.valgt_brugernavn
                break

            if not hasattr(self, "valgt_brugernavn"):
                if data.decode() == "brugernavn_nægtet":
                    self.parent.print("Brugernavnet er optaget!\nVælg brugernavn: ")

                elif data.decode() == "brugernavn_valgt":
                    self.valgt_brugernavn = True
                    self.parent.set_destroy("normal")
                    self.parent.print("Brugernavnet er valgt! Velkommen!\n")
                    self.send("!brugerliste", True)

                continue
            
            self.parent.print(data.decode())

        del self

    def send(self, besked, stille=False):
        if self.SERVER_ALIVE:
            if not hasattr(self, "valgt_brugernavn"):
                besked = "!brugernavn " + besked
                self.parent.print(besked[12:] + "\n\n")

            elif besked == "!afslut":
                self.parent.luk_vindue()

            elif besked == "!ryd":
                self.parent.ryd_chat()
                
            elif not stille:
                self.parent.print("Dig >> " + besked + "\n")
                
            self.SOCK.sendto(besked.encode(), (self.HOST, self.PORT))   
    
    def toggle_status(self):
        self.SERVER_ALIVE = not self.SERVER_ALIVE
