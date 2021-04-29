import socket, threading
from Crypto.Cipher import AES

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
        
        self.con.sendto(("Server forbindelse etableret!\nSkriv '!hjælp' for hjælp\n" + str(len(KLIENTER)) + " person(er) herinde lige nu\n").encode(), (HOST, PORT))
        self.broadcast("En klient oprettede forbindelse.")
        
        self.thread = threading.Thread(target=self.klient_aflytter)
        self.thread.start()

    def __del__(self):
        self.thread.should_abort_immediately = True

    def do_decrypt(self, ciphertext):
        obj2 = AES.new('key123', AES.MODE_CBC, 'IV456')
        ciphertext = obj2.decrypt(ciphertext)
        return ciphertext
    
    def klient_aflytter(self):
        while True:
            try:
                data = self.con.recv(1024)
                
            except:
                print("Klienten ", self.brugernavn ," afsluttede forbindelsen")
                self.broadcast("\nKlienten " + self.brugernavn + " afsluttede forbindelsen")
                break

            if not self.klient_kommandoer(data):
                data_decrypt = do_decrypt(data.decode())
                print(self.brugernavn, self.addr, " >> ", data_decrypt)
                self.broadcast("\n" + self.brugernavn + " >> " + data_decrypt)

        KLIENTER.remove(self)
        del self
    
    def klient_kommandoer(self, besked):
        if besked.decode() == "!hjælp":
            self.con.sendto("!hjælp:        Udskriver hjælpemeddelser.\n!brugerliste:  Udskriver en liste over alle brugere.\n!afslut:       Lukker chatprogrammet ned.\n!brugernavn X: Ændre dit brugernavn i chatten.\n".encode(), (HOST, PORT))
            return True
            
        if besked.decode() == "!brugerliste":
            liste_brugere = "Brugere (" + str(len(KLIENTER)) + "):\n"
            
            for index, klnt in enumerate(KLIENTER):
                liste_brugere += str(index) + ": " + klnt.brugernavn + "\n"
    
            self.con.sendto(liste_brugere.encode(), (HOST, PORT))
            return True

        if besked.decode().split(' ', 1)[0] == "!brugernavn":
            self.brugernavn = besked.decode().split(' ', 1)[1]

            return True
    
        return False
    
    def broadcast(self, besked):
        for klnt in KLIENTER:
            if klnt is not self:
                klnt.con.sendto(besked.encode(), (HOST, PORT))

while True:
    CON, ADDR = SOCK.accept()
    KLIENTER.append(klient(CON, ADDR))

SOCK.close()
