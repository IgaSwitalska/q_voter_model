from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import tkinter as tk
from voter_model import Simulation

class Gui:
    def __init__(self):
        
        """ The function initializing GUI """

        self.bg_color = "#fafafa"
        self.text_font = "Courier"

        self.root = tk.Tk()
        self.root.title("Q-voter model")
        self.root.geometry('1500x800')
        self.root.configure(background=self.bg_color)


    def construction(self):

        """ The function responsible for the arrangement of GUI elements """

        tk.Label(self.root, text="Q-voter model",font=(self.text_font, 30),background=self.bg_color).place(x=50,y=0)

        self.var_nonconf = tk.IntVar()
        nonconf1 = tk.Radiobutton(self.root, text="anticonformism",font=(self.text_font, 10),background=self.bg_color,variable=self.var_nonconf,value=0,command=self.independ)
        nonconf1.place(x=50,y=80)

        nonconf2 = tk.Radiobutton(self.root, text="independence",font=(self.text_font, 10),background=self.bg_color,variable=self.var_nonconf,value=1,command=self.independ)
        nonconf2.place(x=250,y=80)
        nonconf1.select()

        self.var_rep = tk.IntVar()
        repeat1 = tk.Radiobutton(self.root, text="without repeating",font=(self.text_font, 10),background=self.bg_color,variable=self.var_rep,value=0)
        repeat1.place(x=50,y=120)
        repeat2 = tk.Radiobutton(self.root, text="with repeating",font=(self.text_font, 10),background=self.bg_color,variable=self.var_rep,value=1)
        repeat2.place(x=250,y=120)
        repeat1.select()

        tk.Label(self.root, text="System size:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=160)
        self.size = tk.Entry(self.root)
        self.size.place(x=210,y=165)

        tk.Label(self.root, text="Size of the influence group:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=200)
        self.select_q = tk.Entry(self.root)
        self.select_q.place(x=400,y=205)

        tk.Label(self.root, text="Density of people with a positive opinion:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=240)

        self.var_density = tk.DoubleVar()
        density = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_density,length=300, background=self.bg_color)
        density.place(x=50,y=280)

        tk.Label(self.root, text="The probability of non-conformism:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=330)

        self.var_probability = tk.DoubleVar()
        probability = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_probability,length=300, background=self.bg_color)
        probability.place(x=50,y=370)

        tk.Label(self.root, text="The probability of changing the state:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=420)
        tk.Label(self.root, text="(for independence):",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=450)

        self.var_independ_probability = tk.DoubleVar()
        self.independ_probability = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_independ_probability,length=300, background=self.bg_color,state=tk.DISABLED)
        self.independ_probability.place(x=50,y=490)


        tk.Button(self.root,text="Start",font=(self.text_font, 15),background=self.bg_color,command=self.start_simulation).place(x=50,y=560)
        tk.Button(self.root,text="Pause",font=(self.text_font, 15),background=self.bg_color,command=self.pause_animation).place(x=140,y=560)
        tk.Button(self.root,text="Resume",font=(self.text_font, 15),background=self.bg_color,command=self.start_animation).place(x=230,y=560)
        tk.Button(self.root,text="Stop",font=(self.text_font, 15),background=self.bg_color,command=self.end_animation).place(x=330,y=570)

        tk.Button(self.root,text="Close program",font=(self.text_font, 15),background="#e61919",command=self.root.quit).place(x=130,y=620)

        self.frame = tk.Frame(self.root)
        self.frame.place(x=670, y=-20)

    def simulation(self,fig):

        """ 
        The function that creates simulation

        params
        ------
        fig - figure on which a simulation will be displayed

        returns
        -------
        object of class Simulation
        """

        q = int(self.select_q.get())
        p = self.var_probability.get()
        f = self.var_independ_probability.get()
        x = self.var_density.get()
        L = int(self.size.get())
        nonconf = self.var_nonconf.get()
        rep = self.var_rep.get()
        

        anim = Simulation(fig,q,p,f,x,L,nonconf,rep)

        return anim

    def independ(self):

        """
        The function that disables a posibility to change 
        the probability of changing the state, 
        when independence is not chosen
        """

        if self.var_nonconf.get() == 0:
            self.independ_probability.config(state=tk.DISABLED)
        elif self.var_nonconf.get() == 1:
            self.independ_probability.config(state="normal")


    def start_simulation(self):

        """ 
        The function that creates the simulation, 
        is assigned to the Start button 
        """

        for widget in self.frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6,7),facecolor=self.bg_color)
        self.anim = self.simulation(fig)

        canvas = FigureCanvasTkAgg(fig, self.frame)

        function = canvas.get_tk_widget()
        function.pack()
    
        self.anim.simulation_show()

    def pause_animation(self):

        """ 
        The function that pauses the simulation, 
        is assigned to the Pause button 
        """

        self.anim.anim.event_source.stop()

    def start_animation(self):

        """ 
        The function that resumes the simulation, 
        is assigned to the Resume button 
        """

        self.anim.anim.event_source.start()

    def end_animation(self):

        """ 
        The function that ends the simulation, 
        is assigned to the Stop button 
        """
        
        self.anim.anim.event_source.stop()
    
        for widget in self.frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6,3),facecolor=self.bg_color)

        canvas = FigureCanvasTkAgg(fig, self.frame)

        function = canvas.get_tk_widget()
        function.pack()

    def gui_show(self):

        """ Function responsible for displaying GUI """
    
        self.root.mainloop()


if __name__ == "__main__":
    sim = Gui()
    sim.construction()
    sim.gui_show()