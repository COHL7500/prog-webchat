import tkinter as tk

class App:
    def init(self, root):
        #setting title
        root.title("chat")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        connectBut=tk.Button(root)
        connectBut["justify"] = "center"
        connectBut["text"] = "Connect"
        connectBut.place(x=10,y=110,width=140,height=30)
        connectBut["command"] = self.connectBut_command

        self.ipAdress=tk.Entry(root)
        self.ipAdress["borderwidth"] = "1px"
        self.ipAdress["justify"] = "left"
        self.ipAdress["text"] = ""
        self.ipAdress.place(x=10,y=20,width=140,height=30)

        self.port=tk.Entry(root)
        self.port["borderwidth"] = "1px"
        self.port["justify"] = "left"
        self.port["text"] = ""
        self.port.place(x=10,y=70,width=140,height=30)

        self.chatWindow=tk.Listbox(root)
        self.chatWindow["borderwidth"] = "1px"
        self.chatWindow.place(x=160,y=20,width=430,height=426)

        self.chatInput=tk.Entry(root)
        self.chatInput["borderwidth"] = "1px"
        self.chatInput["justify"] = "left"
        self.chatInput["text"] = ""
        self.chatInput.place(x=160,y=450,width=390,height=35)

        self.chatInputBut=tk.Button(root)
        self.chatInputBut["text"] = "Send"
        self.chatInputBut.place(x=550,y=450,width=40,height=35)
        self.chatInputBut["command"] = self.chatInputBut_command

        ipLabel=tk.Label(root)
        ipLabel["text"] = "Ip Adress"
        ipLabel.place(x=0,y=0,width=70,height=25)

        portLabel=tk.Label(root)
        portLabel["text"] = "Port"
        portLabel.place(x=-15,y=50,width=70,height=25)



        def connectBut_command(self):
            print("server aflyt connect")
            self.ip = self.ipAdress.get()
            self.port = self.port.get()

        def scrollDown(self):
            if self.chatWindow.size() == 27:
                self.chatWindow.delete(0)

        def chatInputBut_command(self):
            if self.chatInput.get():
                print(self.chatInput.get())
                self.chatWindow.insert("end",("Me: ", self.chatInput.get()))
                # Skriv komando til at sende til server her
                self.chatInput.delete(0, 'end')
                self.scrollDown()

        def remoteInput(self, remoteIP, input):
            self.chatWindow.insert("end", (remoteIP, ": ", input))
            self.scrollDown()

if name == "main":
    root = tk.Tk()
    app = App(root)
    root.mainloop()