import socket, threading

HOST = ''
PORT = 12345
KLIENTER = []
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.bind((HOST, PORT))
SOCK.listen(5)

print("Server startet!")
print("Venter på klienter...")

class klient:
    def __init__(self, con, addr):
        self.con = con
        self.addr = addr
        self.brugernavn = str(self.addr)
        
        print("Forbindelse oprettet fra ", self.addr)

        self.send_besked("Server forbindelse etableret!\nSkriv '!hjælp' for hjælp\n" + str(len(KLIENTER)) + " person(er) herinde lige nu\n")
        self.broadcast("En klient oprettede forbindelse.") if self.snakker_privat() else None
        
        self.thread = threading.Thread(target=self.aflyt)
        self.thread.start()

    def __del__(self):
        self.thread.should_abort_immediately = True
    
    def aflyt(self):
        while True:
            try:
                data = self.con.recv(1024)
                
            except:
                print("Klienten ", self.brugernavn ," afsluttede forbindelsen")
                self.broadcast("\nKlienten " + self.brugernavn + " afsluttede forbindelsen") if self.snakker_privat() else None
                break
            
            if not self.afkod_kommando(data):
                print(self.brugernavn, self.addr, " >> ", data.decode())
                
                if not self.snakker_privat():
                    self.broadcast("\n" + self.brugernavn + " >> " + data.decode())
                else:
                    self.chat_bruger.send_besked("\n" + self.brugernavn + " >> " + data.decode())

        KLIENTER.remove(self)
        del self

    def send_besked(self, besked):
        self.con.sendto(besked.encode(), (HOST, PORT))

    def snakker_privat(self):
        return False if (not hasattr(self, "chat_bruger") or hasattr(self, "chat_bruger") \
                and (not hasattr(self.chat_bruger, "chat_bruger") \
                     or hasattr(self.chat_bruger, "chat_bruger") and self.chat_bruger.chat_bruger is not self)) else True
    
    def afkod_kommando(self, besked):
        if besked.decode() == "!hjælp":
            self.send_besked("!hjælp:        Udskriver hjælpemeddelser.\n!brugerliste:  Udskriver en liste over alle brugere.\n!afslut:       Lukker chatprogrammet ned.\n!brugernavn X: Ændre dit brugernavn i chatten.\n")

            return True
            
        if besked.decode() == "!brugerliste":
            liste_brugere = "Brugere (" + str(len(KLIENTER)) + "):\n"
            
            for index, klnt in enumerate(KLIENTER):
                liste_brugere += str(index) + ": " + klnt.brugernavn + "\n"
    
            self.send_besked(liste_brugere)
            
            return True
        
        if besked.decode().split(' ', 1)[0] == "!snak":
            anden_bruger = besked.decode().split(' ', 1)[1]

            for klnt in KLIENTER:
                if klnt.brugernavn == anden_bruger:
                    self.chat_bruger = klnt

                    if not hasattr(klnt, "chat_bruger"):
                        print(self.brugernavn + " vil snakke privat med " + klnt.brugernavn + ".")
                        klnt.send_besked(self.brugernavn + " vil snakke privat! Send '!snak " + self.brugernavn + "' for at acceptere.")
                        
                    else:
                        print(self.brugernavn + " har accepteret " + klnt.brugernavn + " privat snak anmodning.")
                        klnt.send_besked("Snakker nu privat med " + klnt.brugernavn + ".")

            return True
        
        if besked.decode() == "!stopsnak":
            if self.snakker_privat():
                print(self.brugernavn + " har afbrudt den private chat med " + self.chat_bruger.brugernavn + ".")
                del self.chat_bruger.chat_bruger
                del self.chat_bruger

            return True
        
        if besked.decode().split(' ', 1)[0] == "!brugernavn":
<<<<<<< Updated upstream
            self.brugernavn = besked.decode().split(' ', 1)[1]
=======
            nyt_brugernavn = besked.decode().split(' ', 1)[1]

            for klnt in KLIENTER:
                if klnt.brugernavn == nyt_brugernavn:
                    break
                
            self.brugernavn = nyt_brugernavn;

>>>>>>> Stashed changes
            return True
    
        return False
    
    def broadcast(self, besked):
        for klnt in KLIENTER:
            if klnt is not self and not klnt.snakker_privat():
                klnt.send_besked(besked)

while True:
    CON, ADDR = SOCK.accept()
    KLIENTER.append(klient(CON, ADDR))

SOCK.close()
