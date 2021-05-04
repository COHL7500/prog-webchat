import tkinter as tk
from klient import server

class chatrum_app:
    def __init__(self, width, height):
        #setting title
        self.root = tk.Tk()
        self.root.title("chat")
        self.root.protocol("WM_DELETE_WINDOW", self.luk_vindue)
        
        #setting window size
        screenwidth = (self.root.winfo_screenwidth() - width) / 2
        screenheight = (self.root.winfo_screenheight() - height) / 2
        self.root.geometry('%dx%d+%d+%d' % (width, height, screenwidth, screenheight))
        self.root.resizable(width=False, height=False)
        
        # Mal vinduet
        self.skab_vindue()
        self.root.mainloop()

    def luk_vindue(self):
        if hasattr(self, "server"):
            self.server.luk()
        self.root.destroy()

    def skab_vindue(self):
        ipLabel=tk.Label(self.root)
        ipLabel["text"] = "IP Address:"
        ipLabel.place(x=5,y=0,width=70,height=20)
        
        self.ipAdress=tk.Entry(self.root)
        self.ipAdress["borderwidth"] = "1px"
        self.ipAdress["justify"] = "left"
        self.ipAdress["text"] = ""
        self.ipAdress.place(x=10,y=20,width=140,height=20)
        self.ipAdress.insert("end", "127.0.0.1")

        portLabel=tk.Label(self.root)
        portLabel["text"] = "Port:"
        portLabel.place(x=-12,y=50,width=70,height=20)

        self.port=tk.Entry(self.root)
        self.port["borderwidth"] = "1px"
        self.port["justify"] = "left"
        self.port["text"] = ""
        self.port.place(x=10,y=70,width=140,height=20)
        self.port.insert("end", "12345")

        self.connectBut=tk.Button(self.root)
        self.connectBut["justify"] = "center"
        self.connectBut["text"] = "Forbind"
        self.connectBut.place(x=10,y=110,width=140,height=30)
        self.connectBut["command"] = self.connectBut_command

        self.destroyBut=tk.Button(self.root)
        self.destroyBut["justify"] = "center"
        self.destroyBut["text"] = "Afbryd"
        self.destroyBut.place(x=10,y=150,width=140,height=30)
        self.destroyBut["command"] = self.destroyBut_command
        self.destroyBut.config(state="disabled")
        
        self.chatWindow=tk.Text(self.root)
        self.chatWindow["borderwidth"] = "1px"
        self.chatWindow.place(x=160,y=5,width=435,height=455)

        self.chatScrollbar = tk.Scrollbar(self.chatWindow, orient="vertical")
        self.chatScrollbar.config(command=self.chatWindow.yview)
        self.chatScrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.chatWindow.config(state="disabled", yscrollcommand=self.chatScrollbar.set)

        portLabel=tk.Label(self.root)
        portLabel["text"] = "Input:"
        portLabel.place(x=145,y=470,width=70,height=20)

        self.chatInput=tk.Entry(self.root)
        self.chatInput["borderwidth"] = "1px"
        self.chatInput["justify"] = "left"
        self.chatInput["text"] = ""
        self.chatInput.place(x=212,y=470,width=295,height=20)
        self.chatInput.config(state="disabled")

        self.chatInputBut=tk.Button(self.root)
        self.chatInputBut["text"] = "Send"
        self.chatInputBut.place(x=515,y=470,width=80,height=20)
        self.chatInputBut["command"] = self.chatInputBut_command
        self.chatInputBut.config(state="disabled")
        self.root.bind("<Return>", lambda event=None: self.chatInputBut.invoke())

        # Printer velkommen besked
        self.print("Velkommen til brugerchatten!\nForbind til en server ude til venstre for at kunne skrive med andre!\n\n")
    
    def connectBut_command(self):
        self.str_ip = self.ipAdress.get()
        self.str_port = self.port.get()
        self.server = server(self.str_ip, self.str_port, self)

        if self.server.SERVER_ALIVE:
            self.set_ipport("disabled")
            self.set_input("normal")

    def destroyBut_command(self):
        self.server.luk()
        self.destroyBut.config(state="disabled")
    
    def chatInputBut_command(self):
        if self.chatInput.get() and hasattr(self, "server"):
            self.server.send(self.chatInput.get())
            self.chatWindow.see("end")

    def set_input(self,fstate):
        self.chatInput.config(state=fstate)
        self.chatInputBut.config(state=fstate)

    def set_ipport(self, fstate):
        self.ipAdress.config(state=fstate)
        self.port.config(state=fstate)
        self.connectBut.config(state=fstate)

    def set_destroy(self,fstate):
        self.destroyBut.config(state=fstate)
    
    def print(self, tekstinput):
        self.chatWindow.config(state="normal")
        self.chatWindow.insert("end", tekstinput)
        self.chatWindow.config(state="disabled")
        self.chatWindow.see("end")
        self.chatInput.delete(0, "end")

    def ryd_chat(self):
        self.chatWindow.config(state="normal")
        self.chatWindow.delete("1.0", "end")
        self.chatWindow.config(state="disabled")
        self.print("Chat ryddet!\n\n")

chatrum_app(600, 500)
