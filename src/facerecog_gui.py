from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import os
from facerecognition import *
from tkinter import messagebox

class App():
    def about(self,master):
        self.window = Toplevel(master)
        self.window.resizable(0,0)
        self.window.title('About')
        self.window.iconbitmap('assets/icon.ico')
        self.label1 = Label(self.window,text = "Created By:").grid(row=0,column=0,padx=10,pady=10)
        self.label1 = Label(self.window,text = "Muhammad Daru Darmakusuma").grid(row=1,column=0,padx=10)
        self.label2 = Label(self.window,text = "Gregorius Jovan Kresnadi").grid(row=2,column=0,padx=10)
        self.labe3 = Label(self.window,text = "Arthur Edgar Yunanto").grid(row=3,column=0,padx=10)

    def ChooseFolder(self):
        self.dicname = filedialog.askdirectory()
        if (self.dicname != ''):
            self.entrydb.delete(0, "end")
            self.entrydb.insert(0, self.dicname)
    def DefaultFolder(self):
        self.entrydb.delete(0, "end")
        self.entrydb.insert(0,"database/")

    def ChooseFile(self):
        self.matchfile = filedialog.askopenfilename(title = "Select Picture to Match",initialdir='sample/',filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        if (self.matchfile != ''):
            self.entrys.delete(0, "end")
            self.entrys.insert(0, self.matchfile)
        img = Image.open(self.entrys.get())
        height = 250
        hpercent = (height/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        self.simg = ImageTk.PhotoImage(img.resize((wsize, height), Image.ANTIALIAS))
        self.sample.config(image=self.simg)

    def verify(self):
        if (self.entrys.get() == "assets/placeholder1.png"):
            temp = messagebox.askokcancel("No File to Match!", "Choose a file and continue?")
            if (temp):
                self.ChooseFile()
                self.matchRun()
        else:
            self.matchRun()
    
    def sel(self):
        self.entrym.delete(0, "end")
        if (self.var.get()==0):
            self.entrym.insert(0,0)
        elif (self.var.get()==1):
            self.entrym.insert(0,1)
        else:
            self.entrym.insert(0,2)

    def on_closing(self):
        self.setbut.config(state='normal')
        self.entryn.delete(0,END)
        self.entryn.insert(0,self.npic.get())
        self.window.grab_release()
        self.window.destroy()

    def settings(self,master):
        self.setbut.config(state='disabled')
        self.folder = self.entrydb.get()
        if (self.folder!='database/'):
            namepck = self.folder.split('/')[-1].lower()
        else:
            namepck = 'default'
        if not(os.path.exists("../bin/"+namepck+".pck")):
            files = [os.path.join(root, file) for root, dirs, files in os.walk(self.folder) for file in files if file.endswith(".jpg")]
            x = len(files)
        else:
            ma = Matcher(pickled_path="../bin/"+namepck+".pck")
            x = len(ma.names)
        self.window = Toplevel(master)
        self.window.resizable(0,0)
        self.window.title('Settings')
        self.window.iconbitmap('assets/icon.ico')
        self.window.config(bg='#2d3436')
        self.window.grab_set()
        self.var = IntVar()
        self.var.set(int(self.entrym.get())) 
        self.lab = Label(self.window,font='Helvetica 12 bold',bg='#2d3436',fg='white',text="Choose a method:").pack(pady=5)
        self.R1 = Radiobutton(self.window,text="Euclidian Distance", variable=self.var, value=0,command=self.sel)
        self.R1.pack( anchor = W, padx=15, fill = X )
        self.R2 = Radiobutton(self.window,text="Cosine Similarity", variable=self.var, value=1,command=self.sel)
        self.R2.pack( anchor = W, padx=15, fill = X )
        self.R3 = Radiobutton(self.window,text="Mixed (Euc Dist and Cos Sim)", variable=self.var, value=2,command=self.sel)
        self.R3.pack( anchor = W, padx=15, pady=(0,5), fill = X )
        self.lab1 = Label(self.window,font='Helvetica 12 bold',bg='#2d3436',fg='white',text="Similar picture(s) showed:").pack()
        self.npic = Spinbox(self.window, from_ = 1, to = x, textvariable=self.entryn)
        self.npic.pack(pady=(8,10),padx=15,fill = X)
        self.window.protocol('WM_DELETE_WINDOW',self.on_closing)

    def matchRun(self):
        print("Matching...")
        self.folder = self.entrydb.get()
        self.file = self.entrys.get()
        self.meth = int(self.entrym.get())
        if (self.folder!='database/'):
            namepck = self.folder.split('/')[-1].lower()
        else:
            namepck = 'default'
        temp = True
        if not(os.path.exists("../bin/"+namepck+".pck")):
            temp = False
            temp = messagebox.askokcancel("No Database Extraction!", "Extract it and continue?")
            if (temp):
                extract_batch(self.folder,pickled_path=namepck+".pck")
        if (temp):
            ma = Matcher(pickled_path="../bin/"+namepck+".pck")
            self.names, self.matches = ma.match(self.file,method=self.meth,topn=int(self.entryn.get()))
            self.i = 0
            self.rank.config(text="Rank " + str(self.i+1))
            self.perc.config(text=str(round(self.matches[self.i],2))+'%')
            img2 = Image.open(self.names[self.i])
            nama = self.names[self.i].split('\\')[-1]
            self.pathc.delete(0,END)
            self.pathc.insert(0,"Image: " + str(nama))
            heightc = 300
            hpercentc = (heightc/float(img2.size[1]))
            wsizec = int((float(img2.size[0])*float(hpercentc)))
            print("Done!")
            self.initimg2 = ImageTk.PhotoImage(img2.resize((wsizec, heightc), Image.ANTIALIAS))
            self.comp.config(image=self.initimg2)
        else:
            print('Match Process Stopped')
    def next(self):
        self.i += 1
        if (self.i >= len(self.matches)):
            self.i %= len(self.matches)
        self.rank.config(text="Rank " + str(self.i+1))
        self.perc.config(text=str(round(self.matches[self.i],2))+'%')
        img2 = Image.open(self.names[self.i])
        nama = self.names[self.i].split('\\')[-1]
        self.pathc.delete(0,END)
        self.pathc.insert(0,"Image: " + str(nama))
        heightc = 300
        hpercentc = (heightc/float(img2.size[1]))
        wsizec = int((float(img2.size[0])*float(hpercentc)))
        self.initimg2 = ImageTk.PhotoImage(img2.resize((wsizec, heightc), Image.ANTIALIAS))
        self.comp.config(image=self.initimg2)
    def prev(self):
        self.i -= 1
        if (self.i >= ((-1)*len(self.matches))):
            self.i %= len(self.matches)
        self.rank.config(text="Rank " + str(self.i+1))
        self.perc.config(text=str(round(self.matches[self.i],2))+'%')
        img2 = Image.open(self.names[self.i])
        nama = self.names[self.i].split('\\')[-1]
        self.pathc.delete(0,END)
        self.pathc.insert(0,"Image: " + str(nama))
        heightc = 300
        hpercentc = (heightc/float(img2.size[1]))
        wsizec = int((float(img2.size[0])*float(hpercentc)))
        self.initimg2 = ImageTk.PhotoImage(img2.resize((wsizec, heightc), Image.ANTIALIAS))
        self.comp.config(image=self.initimg2)

        
    def __init__(self,master):
        # Title
        master.resizable(0, 0)
        master.configure(background='#2d3956')
        master.title('Face-Recognition Fesbuk')
        master.iconbitmap('assets/icon.ico')
        self.menuframe = Frame(master, relief='ridge', borderwidth = 5,bg='#ffffff')
        self.menuframe.grid(column=0,row=0,rowspan=2,padx=10, pady=10, ipadx=2, ipady =2,sticky=N) 
        self.mid = Frame(master,bg='#2d3436')
        self.mid.grid(column=1,row=0, pady=10, sticky=N)
        self.pic1frame = Frame(self.mid,relief='ridge',borderwidth = 5,bg='#ffffff')
        self.pic1frame.grid(row=0, pady=(0,5))
        self.pic2frame = Frame(master,relief='ridge',borderwidth = 5,bg='#ffffff')
        self.pic2frame.grid(column=2,row=0,rowspan=2,padx=10, pady=10,ipady =4,sticky=N)

        # Menu bar
        self.menu = Menu(root) 
        master.config(menu=self.menu) 
        self.filemenu = Menu(self.menu,tearoff=0) 
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Open Image Database',command=self.ChooseFolder)
        self.filemenu.add_command(label='Set Image Database to Default',command=self.DefaultFolder)
        self.filemenu.add_separator() 
        self.filemenu.add_command(label='Exit', command=master.quit) 
        self.helpmenu = Menu(self.menu,tearoff=0) 
        self.menu.add_cascade(label='Help', menu=self.helpmenu) 
        self.helpmenu.add_command(label='About', command=lambda: self.about(master)) 

        # Logo
        self.intro = ImageTk.PhotoImage(Image.open('assets/intro.png').resize((245, 400), Image.ANTIALIAS))
        self.label = Label(self.menuframe,image=self.intro,bg='#ffffff')
        self.label.pack(fill=BOTH,pady=15,padx=25)
        
        # Folder and file holder
        defaultdb = StringVar(master, value="database/")
        defaults = StringVar(master, value="assets/placeholder1.png")
        defaultm = StringVar(master, value=0)
        defaultn = StringVar(master, value=1)
        self.entrys = Entry(master,textvariable=defaults)
        self.entrym = Entry(master,textvariable=defaultm)
        self.entryn = Entry(master,textvariable=defaultn)
        
        # Image viewer: Match
        self.title1 = Label(self.pic1frame,text = "Picture to match: ",font=('Roboto',14),bg='white')
        self.title1.grid(sticky=W,row=0,column=0, columnspan=2, padx=3, pady=3)
        img = Image.open(self.entrys.get())
        height = 250
        hpercent = (height/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        self.initimg = ImageTk.PhotoImage(img.resize((wsize, height), Image.ANTIALIAS))
        self.sample = Label(self.pic1frame,image=self.initimg,bg='#ffffff')
        self.sample.grid(row=1,column=0,columnspan=2,padx=40,pady=(0,5),sticky='nsew')


        # Button Match
        self.clusterbut = Frame(self.pic1frame)
        self.clusterbut.grid(column=0, row=2, pady=2, padx = 80)
        self.clusterbut.config(bg='white')
        self.choose = ImageTk.PhotoImage(Image.open('assets/choose.png'))
        self.matchimg = ImageTk.PhotoImage(Image.open('assets/match.png'))
        self.setimg = ImageTk.PhotoImage(Image.open('assets/settings.png'))
        self.openFile = Button(self.clusterbut,text="Choose File",relief=FLAT)
        self.openFile.config(image=self.choose, bg='#ffffff',command=self.ChooseFile)
        self.openFile.pack(side=LEFT)
        self.setbut = Button(self.clusterbut,text="Settings", bg='#ffffff', relief=FLAT)
        self.setbut.config(image=self.setimg,command=lambda: self.settings(master))
        self.setbut.pack(side=LEFT)
        self.matchbut = Button(self.pic1frame,text="Match",width=172,height=43,bg='#ffffff', relief=FLAT)
        self.matchbut.config(image=self.matchimg,command=self.verify)
        self.matchbut.grid(column=0,row=3, pady=(2,5))
        
        
        # # Compare
        self.labelcomp = Label(self.pic2frame,text = "Compared picture: ",font=('Roboto',14),bg='white')
        self.labelcomp.grid(sticky=W,row=0,column=0,columnspan=2,padx=3, pady=(3,0))
        self.rank = Label(self.pic2frame,text = "",font='Helvetica 12 bold',bg='white',fg='#0984e3')
        self.rank.grid(sticky=EW,row=1,column=0,columnspan=3)
        self.perc = Label(self.pic2frame,text = "",font='Helvetica 12 bold',bg='white',fg='#0984e3')
        self.perc.grid(sticky=EW,row=2,column=0,columnspan=3)
        img2 = Image.open(self.entrys.get())
        heightc = 300
        hpercentc = (heightc/float(img2.size[1]))
        wsizec = int((float(img2.size[0])*float(hpercentc)))
        self.initimg2 = ImageTk.PhotoImage(img2.resize((wsizec, heightc), Image.ANTIALIAS))
        self.comp = Label(self.pic2frame,image=self.initimg2,bg='#ffffff')
        self.comp.grid(row=3,column=0,columnspan=3,padx=10,sticky='new')
        self.bwd = ImageTk.PhotoImage(Image.open('assets/backward.png'))
        self.butprev = Button(self.pic2frame, text="Prev image", padx=10, pady=4,command=self.prev, relief=FLAT, bg='white')
        self.butprev.config(image=self.bwd)
        self.butprev.grid(row=4,column=0, pady=2, padx=5, sticky=W)
        self.pathc = Entry(self.pic2frame,font='Helvetica 10 bold',width=20)
        self.pathc.grid(row=4,column=1,sticky=EW)
        self.fwd = ImageTk.PhotoImage(Image.open('assets/forward.png'))
        self.butnext = Button(self.pic2frame, text="Next image", padx=10, pady=4,command=self.next, relief=FLAT, bg='white')
        self.butnext.config(image=self.fwd)
        self.butnext.grid(row=4,column=2, pady=2, padx=5,sticky=E)
        
        # Status Database
        self.statframe = Frame(self.mid, relief='ridge', borderwidth = 5,bg='#ffffff')
        self.statframe.grid(row=1, pady=2, sticky="nsew")
        self.entrydb = Entry(self.statframe,textvariable=defaultdb,width=40)
        self.entrydb.pack(side=RIGHT,fill=X)
        self.statusbar = Label(self.statframe, text="Image Database: ", bd=1, anchor=W)
        self.statusbar.pack(side=LEFT)
# GUI
root = Tk()
app = App(root)
root.mainloop()