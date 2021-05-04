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
        self.brugernavn = None
        self.ignorer_liste = []
        
        print("Forbindelse oprettet fra ", self.addr)
        self.broadcast("En klient oprettede forbindelse.\n")
        
        self.thread = threading.Thread(target=self.aflyt)
        self.thread.start()

    def __del__(self):
        self.thread.should_abort_immediately = True
    
    def aflyt(self):
        while True:
            try:
                data = self.con.recv(1024)
                
            except:
                print("Klienten ", self.brugernavn , self.addr, " afsluttede forbindelsen.")
                self.broadcast("\nKlienten '" + self.brugernavn + "' afsluttede forbindelsen.\n")

                if self.snakker_privat():
                    self.chat_bruger.send_besked("Brugeren '" + self.brugernavn + "' forlod serveren!\nNu i gruppechat!\n")
                    del self.chat_bruger.chat_bruger
                    
                break

            print(self.brugernavn, " >> ", data.decode())
            
            if not self.afkod_kommando(data):
                if not self.snakker_privat():
                    self.broadcast(self.brugernavn + " >> " + data.decode() + "\n")
                else:
                    self.chat_bruger.send_besked(self.brugernavn + " >> " + data.decode() + "\n")

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
            self.send_besked(("-"*30) + "\n")
            self.send_besked("!hjælp:        Udskriver hjælpemeddelser.\n!brugerliste:  Udskriver en liste af alle brugere.\n!afslut:       Lukker chatprogrammet.\n!brugernavn X: Ændre dit brugernavn til 'X'.\n!snak Y:       Anmoder om privat chat med 'Y'.\n!stopsnak:     Stopper en privat chat.\n!ignorer Y:    Igonerer alt fra brugeren 'Y'.\n!igliste:      Printer ignorerede brugere.\n!ryd           Ryder chatvinduet fuldstændigt!\n")
            self.send_besked(("-"*30) + "\n")
            
            return True
        
        elif besked.decode() == "!brugerliste":
            if len(KLIENTER):
                liste_brugere = str(len(KLIENTER)) + " person(er) herinde lige nu.\n" + ("-"*30) + "\n"
                
                for index, klnt in enumerate(KLIENTER):
                    if klnt.brugernavn is not None:
                        liste_brugere += str(index) + ": " + klnt.brugernavn + ("(privat chat)" if klnt.snakker_privat() else "") + ("(ignoreret)" if klnt in self.ignorer_liste else "") + (" <- dig" if klnt is self else "") + "\n"
                    else:
                        liste_brugere += str(index) + ": Opretter forbindelse...\n"
                    
                liste_brugere += ("-"*30) + "\n"
                
            else:
                liste_brugere = "Kun dig inde i chatrummet (1)!\n"
    
            self.send_besked(liste_brugere)
            
            return True

        elif besked.decode() == "!igliste":
            if len(self.ignorer_liste):
                liste_brugere = str(len(self.ignorer_liste)) + " person(er) ignoreret lige nu.\n" + ("-"*30) + "\n"
                
                for index, klnt in enumerate(self.ignorer_liste):
                    liste_brugere += str(index) + ": " + klnt.brugernavn + "\n"

                liste_brugere += ("-"*30) + "\n"

            else:
                liste_brugere = "Ingen ignorerede brugere!\n"

            self.send_besked(liste_brugere)

            return True
        
        elif besked.decode().split(' ', 1)[0] == "!ignorer":
            anden_bruger = besked.decode().split(' ', 1)[1]

            # Hvis brugeren prøver at blokerer sig selv
            if anden_bruger == self.brugernavn:
                self.send_besked("Du kan ikke ignorerer dig selv!\n")

            for klnt in KLIENTER:
                if klnt.brugernavn == anden_bruger and klnt is not self: # Hvis denne bruger er den nævnte
                    if klnt in self.ignorer_liste:
                        self.ignorer_liste.remove(klnt)
                        self.send_besked("Ignorering af '" + klnt.brugernavn + "' fjernet!\n")
                        klnt.send_besked("Brugeren '" + self.brugernavn + "' har fjernet din ignorering!\n")
                    else:
                        self.ignorer_liste.append(klnt)
                        self.send_besked("Ignorerer nu alle beskeder og anmodninger fra '" + klnt.brugernavn + "'!\n")
                        klnt.send_besked("Brugeren '" + self.brugernavn + "' har valgt at ignorer dig!\n")

            return True
        
        elif besked.decode().split(' ', 1)[0] == "!snak":
            anden_bruger = besked.decode().split(' ', 1)[1]

            # Hvis brugeren prøver at snakke privat med sig selv
            if anden_bruger == self.brugernavn:
                self.send_besked("Du kan ikke indlede en privat samtale med dig selv!\n")

            # Hvis brugeren prøver at snakke privat mens de allerede er i en privat chat eller sendt en anmodning
            elif hasattr(self, "chat_bruger"):
                self.send_besked("Kan ikke indlede en ny privat samtale!\nAfslut den nuværende samtale med '!stopsnak' først!\n")
                return True

            # Gennemgår alle brugere for brugeren med brugernavnet angivet
            for klnt in KLIENTER:
                if klnt.brugernavn == anden_bruger: # Hvis denne bruger er den nævnte
                    self.chat_bruger = klnt

                    # Hvis brugeren prøver at snakke med en der har blokeret ham
                    if self in klnt.ignorer_liste:
                        self.send_besked("Brugeren '" + klnt.brugernavn + "' har blokeret dig!\n")

                    # Hvis brugeren prøver at snakke med en han selv har blokeret
                    elif klnt in self.ignorer_liste:
                        self.send_besked("Brugeren '" + klnt.brugernavn + "' har du blokeret!\n")

                    # Hvis brugeren nævnt allerede er i en privat chat med en anden bruger
                    elif klnt.snakker_privat() and klnt.chat_bruger is not self:
                        self.send_besked("Brugeren '" + klnt.brugernavn + "' er allerede i en privat chat!\n")
                        klnt.send_besked("Brugeren '" + self.brugernavn + "' har sendt en chatting anmodning!\n")

                    # Hvis brugeren ikke er i en privat chat, send en anmodning
                    elif not hasattr(klnt, "chat_bruger"):
                        print(self.brugernavn + " " + str(self.addr) + " vil snakke privat med " + klnt.brugernavn + " " + str(klnt.addr))
                        klnt.send_besked("\n" + ("-"*30) + "\n" + self.brugernavn + " vil snakke privat!\n")
                        klnt.send_besked("Send '!snak " + self.brugernavn + "' for at acceptere.\n" + ("-"*30) + "\n")

                    # Hvis begge brugere har sendt anmodninger til hinanden, snakker de nu privat
                    elif klnt.chat_bruger == self and self.chat_bruger == klnt:
                        print(self.brugernavn + " " + str(self.addr) + " har accepteret " + klnt.brugernavn + " " + str(klnt.addr) + " privat snak anmodning.")
                        klnt.send_besked("Snakker nu privat med " + self.brugernavn + ".\n")
                        self.send_besked("Snakker nu privat med " + klnt.brugernavn + ".\n")

                    break

            # Hvis brugeren ikke eksistere
            if not hasattr(self, "chat_bruger"):
                self.send_besked("Brugeren du vil snakke med privat findes ikke!\n")
                
            return True
        
        elif besked.decode() == "!stopsnak":
            if self.snakker_privat():
                print(self.brugernavn + " har afbrudt den private chat med " + self.chat_bruger.brugernavn + ".")

                self.send_besked("Stoppede den private chat med '" + self.chat_bruger.brugernavn + "'!\nNu i gruppechat!\n")
                self.chat_bruger.send_besked("Brugeren '" + self.brugernavn + "' stoppede den private chat!\nNu i gruppechat!\n")
                
                del self.chat_bruger.chat_bruger
                del self.chat_bruger

            return True
        
        elif besked.decode().split(' ', 1)[0] == "!brugernavn":
            nyt_brugernavn = besked.decode().split(' ', 1)[1]

            for klnt in KLIENTER:
                if klnt.brugernavn == nyt_brugernavn:
                    self.send_besked("brugernavn_nægtet")
                    return True

            self.send_besked("brugernavn_valgt")
            self.brugernavn = nyt_brugernavn;

            return True

        elif besked.decode()[0] == '!' and besked.decode() != "!ryd" and besked.decode() != "!afslut":
            self.send_besked("Ukendt kommando: " + besked.decode() + "\n")
            return True
    
        return False

    # Skriver en besked til alle brugere som ikke:
    # - er personen der har skrevet den
    # - er brugere der er i en privat chat
    # - er brugere som ikke har valgt et brugernavn
    def broadcast(self, besked):
        for klnt in KLIENTER:
            if klnt is not self and not klnt.snakker_privat() and self not in klnt.ignorer_liste:
                klnt.send_besked(besked)

while True:
    CON, ADDR = SOCK.accept()
    KLIENTER.append(klient(CON, ADDR))

SOCK.close()
