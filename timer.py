import time
import tkinter as tk
from tkinter import ttk
     
class StopWatch:
    def __init__(self, app):
        self.app = app
        self.startTime = 0
        self.elapsedTime = 0
        self.isRunning = False
        self.i = 0
        self.topmost_var = tk.IntVar() #For checkbox. Stores 0 and 1
        self.formatted_time = None
        self.resetButton = None
        self.intervals = []
        self.appSetup()

    def header(self):
        header_frame = ttk.Frame(master=root, height=60, borderwidth=1, style="Header.TFrame")
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False) #Frame wont adjust size to fit content inside
        
        header_label = ttk.Label(header_frame, text="Study Timer", style='HeaderLabel.TLabel')
        header_label.place(relx=0.5, rely=0.5, anchor='center')
    
    def body(self):
        self.body_upper_frame = ttk.Frame(master=root, style="Body.TFrame")
        self.body_upper_frame.grid(row=1, column=0, sticky='nsew')

        self.body_down_frame = ttk.Frame(master=root, relief='flat', style="Body.TFrame")
        self.body_down_frame.grid(row=2, column=0, sticky='nsew')

    #Timer Borders
        timer_frame = ttk.Frame(master=self.body_upper_frame, borderwidt=10, relief='solid', style='TimerBorder.TFrame')
        timer_frame.pack(expand=False, anchor='n', pady=20)
    #TIME RUNNING
        self.LabTime = ttk.Label(master=timer_frame, style='Timer.TLabel')
        self.LabTime.pack()
        formatted_time = "{:02d}:{:02d}:{:02d}".format(0, 0, 0)
        self.LabTime.config(text=formatted_time)
    
    #START/PAUSE BUTTON
        self.startButton = ttk.Button(master=self.body_upper_frame, text="Start", command=self.start)
        self.startButton.pack(side='top')
    #NEW INTERVALL Button
        self.intervallButton = ttk.Button(master=self.body_upper_frame, text="Intervall", command=self.newIntervall)
        self.intervallButton.pack(side='top', pady=5, expand=False)
    
    def footer(self):
        footer_frame = ttk.Frame(root, height=20, borderwidth=1, relief='solid', style="Footer.TFrame")
        footer_frame.place(relx=0, rely=1, x=0, y=0, anchor='sw')
        footer_frame.grid_propagate(True)

        alwaysOnTopCheck = ttk.Checkbutton(master=footer_frame, text="Top", style="checkButton.TCheckbutton", variable=self.topmost_var,command=self.topmostToggle)
        alwaysOnTopCheck.grid(row=0, column=0) 

    def styles(self):
        style = ttk.Style()

    ######HEADER STYLES#####
        style.configure('HeaderLabel.TLabel', foreground='white', background='#090909',  font=('Orbitron', 24, 'bold'))  
        style.configure('Header.TFrame', background='#090909')
  
    #####BODY STYLES#####
        style.configure('Body.TFrame', background='#131313')
        style.configure('TimerBorder.TFrame', relief='ridge', borderwidth=2, background='#7A7A7A')
        style.configure('Timer.TLabel', background='#CACACA', font=('Helvetica', 24, 'bold'), foreground='black')
        style.configure('Intervall.TLabel', background='#CACACA', font=('Helvetica', 10), foreground='black')

    #####FOOTER STYLES#####
        style.configure("checkButton.TCheckbutton", background="white")

    def appSetup(self):
        root.geometry("360x400")
        self.app.title("Study Timer") #App banner title
        # Configure the grid layout to allocate space for header, body, and footer
        root.grid_rowconfigure(2, weight=10)  #Resizing window makes row 2 10x
        root.grid_rowconfigure(1, weight=5)  #Resizing window makes row 1 1x
        root.grid_columnconfigure(0, weight=1) 

        self.styles()
        self.header()
        self.body()
        self.footer()
   
    def updateTime(self):
        if self.isRunning:
            now = time.time()
            elapsed = now-self.startTime + self.elapsedTime
            hours, remainder = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)

            self.formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, int(seconds))
            self.LabTime.config(text=self.formatted_time)
            self.app.after(1000, self.updateTime)

    def start(self):
        if self.i>11:
            return

        if not self.isRunning:
            self.isRunning = True
            self.startButton.config(text='Pause')
            if self.startTime == 0:
                self.startTime = time.time()
            self.updateTime()

        else:
            self.isRunning = False
            self.startButton.config(text='Start')

            self.elapsedTime += time.time() - self.startTime
            self.startTime = 0

    def reset(self):
        self.formatted_time = 0
        self.startTime = 0
        self.elapsedTime = 0
        self.isRunning = False
        self.LabTime.config(text="00:00:00")

        for i in self.intervals:
            i.destroy()
        self.intervals.clear()
        self.i = 0
        

    def newIntervall(self):
    #Reset Button
        if not self.resetButton:
            self.resetButton = ttk.Button(master=self.body_upper_frame, text="Reset All", command=self.reset)
            self.resetButton.pack(side='top')

        if (self.elapsedTime>0 or self.isRunning) and self.i<13:
            self.LabTime.config(text="00:00:00")
            self.startButton.config(text='Start')
            self.i+=1
            if self.i<5:
                saveIntervall = "{}: {}".format(self.i, self.formatted_time)
                new_label = ttk.Label(master=self.body_down_frame, text=saveIntervall, style='Intervall.TLabel')
                new_label.grid(column=self.i, row=1, padx=10, pady=10, sticky="n")
                self.intervals.append(new_label)  
            elif self.i>4 and self.i<9:
                saveIntervall = "{}: {}".format(self.i, self.formatted_time)
                new_label = ttk.Label(master=self.body_down_frame, text=saveIntervall, style='Intervall.TLabel')
                new_label.grid(column=self.i-4, row=2, padx=5, pady=10, sticky="n")
                self.intervals.append(new_label)  
            elif self.i>8 and self.i<13:
                saveIntervall = "{}: {}".format(self.i, self.formatted_time)
                new_label = ttk.Label(master=self.body_down_frame, text=saveIntervall, style='Intervall.TLabel')
                new_label.grid(column=self.i-8, row=3, padx=5, pady=10, sticky="n")
                self.intervals.append(new_label)

            self.formatted_time = 0
            self.startTime = 0
            self.elapsedTime = 0
            self.isRunning = False

    def topmostToggle(self):
            # If checked, set the window to stay on top
        if self.topmost_var.get():
           root.attributes('-topmost', True)
        else:
          root.attributes('-topmost', False)

root = tk.Tk()
st = StopWatch(root)
root.mainloop()