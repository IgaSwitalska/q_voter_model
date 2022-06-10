from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import tkinter as tk


class Simulation:

    def __init__(self,fig,q,p,f,x,L,nonconf=0,rep=1):
        self.fig = fig
        self.ax1 = fig.add_subplot(211)
        self.ax1.set_title("Model q-wyborcy dla q = {}".format(q))
        self.ax1.axis("off")

        self.ax2 = fig.add_subplot(212)
        self.ax2.set_ylim(-1.5,1.5)
        self.ax2.set_xlabel("czas")
        self.ax2.set_ylabel("średnia opnia")

        self.q = q # ilu sąsiadów losujemy
        self.p = p # prawdopodobieństwo nonkonformizmu
        self.f = f #prawdopodobieństwo zmiany stanu przy niezależności
        self.L = L # wymiar siatki
        self.N = self.L**2
        self.nonconf = nonconf
        self.rep = rep

        self.x = x # zagęszczenie ludzi o pozytywnej opinii
        self.S = np.random.permutation([1]*round(x*self.N) + [-1]*(self.N - round(x*self.N)))
        self.S = self.S.reshape((self.L, self.L))
        #self.S = np.random.choice([-1,1], size=(L, L))
        #self.snapshots = []

        self.fps = 30
        self.heat_map = self.ax1.imshow(np.copy(self.S), vmin=-1, vmax=1, cmap="cubehelix")
        self.time, self.average_opinion = [0], [0]
        self.line, = self.ax2.plot(self.time,self.average_opinion,color="k")
        #plt.title("Model q-wyborcy)

        self.global_time = 0

    def animate_func(self,i):
        # if self.global_time == 0:
        #     self.global_time += 1
        #     return [self.heat_map],self.line,
        # else:
        for _ in range(self.N):
            i = np.random.randint(0,self.L)
            j = np.random.randint(0,self.L)

            if i == 0 and j == 0:
                neighbours = [self.S[1][0],self.S[0][1]]
            elif i == 0 and j == self.L-1:
                neighbours = [self.S[0][self.L-2],self.S[1][self.L-1]]
            elif i == self.L-1 and j == 0:
                neighbours = [self.S[self.L-2][0],self.S[self.L-1][1]]
            elif i == self.L-1 and j == self.L-1:
                neighbours = [self.S[self.L-1][self.L-2],self.S[self.L-2][self.L-1]]
            else:
                if i == 0:
                    neighbours = [self.S[i][j-1],self.S[i][j+1],self.S[i+1][j]]
                elif i == self.L-1:
                    neighbours = [self.S[i][j-1],self.S[i][j+1],self.S[i-1][j]]
                elif j == 0:
                    neighbours = [self.S[i-1][j],self.S[i+1][j],self.S[i][j+1]]
                elif j == self.L-1:
                    neighbours = [self.S[i-1][j],self.S[i+1][j],self.S[i][j-1]]
                else:
                    neighbours = [self.S[i][j-1],self.S[i][j+1],self.S[i+1][j],self.S[i-1][j]]
            
            if self.rep == 1:
                inf = np.random.choice(neighbours,size=self.q,replace=True)
            elif self.rep == 0:
                inf = np.random.choice(neighbours,size=min(self.q,len(neighbours)),replace=False)

            if self.nonconf == 0: #antykonformizm
                if np.abs(np.sum(inf)) == self.q:
                    U = np.random.random()
                    if U <= self.p:
                        self.S[i][j] = -np.sum(inf)/self.q
                    else:
                        self.S[i][j] = np.sum(inf)/self.q
            elif self.nonconf == 1: #niezależność
                U = np.random.random()
                if U <= self.p:
                    U2 = np.random.random()
                    if U2 <= self.f:
                        self.S[i][j] = -1
                    else:
                        self.S[i][j] = 1
                else:
                    if np.abs(np.sum(inf)) == self.q:
                        self.S[i][j] = np.sum(inf)/self.q

        self.time.append(self.global_time)
        self.ax2.set_xlim(0,self.global_time)
        self.average_opinion.append(np.sum(np.copy(self.S))/self.N)
        self.line.set_data(self.time,self.average_opinion)

        self.heat_map.set_array(np.copy(self.S))

        self.global_time += 1

        return [self.heat_map],self.line,

    def simulation_show(self):
        self.anim = animation.FuncAnimation(
                                    self.fig, 
                                    self.animate_func,
                                    interval = 100 / self.fps, # in ms
                                    repeat = False
                                    )

        plt.show()
        # self.ax1.show()
        # self.ax2.show()

class Gui:
    def __init__(self):
        #self.bg_color = "#b77396"
        self.bg_color = "#fafafa"
        self.text_font = "Courier"

        self.root = tk.Tk()
        self.root.title("Model q-wyborcy")
        self.root.geometry('1500x800')
        self.root.configure(background=self.bg_color)


    def construction(self):
        tk.Label(self.root, text="Model q-wyborcy",font=(self.text_font, 30),background=self.bg_color).place(x=50,y=0)

        self.var_nonconf = tk.IntVar()
        nonconf1 = tk.Radiobutton(self.root, text="antykonformizm",font=(self.text_font, 10),background=self.bg_color,variable=self.var_nonconf,value=0,command=self.independ)
        nonconf1.place(x=50,y=80)

        nonconf2 = tk.Radiobutton(self.root, text="niezależność",font=(self.text_font, 10),background=self.bg_color,variable=self.var_nonconf,value=1,command=self.independ)
        nonconf2.place(x=250,y=80)
        nonconf1.select()

        self.var_rep = tk.IntVar()
        repeat1 = tk.Radiobutton(self.root, text="bez powtarzania",font=(self.text_font, 10),background=self.bg_color,variable=self.var_rep,value=0)
        repeat1.place(x=50,y=120)
        repeat2 = tk.Radiobutton(self.root, text="z powtarzaniem",font=(self.text_font, 10),background=self.bg_color,variable=self.var_rep,value=1)
        repeat2.place(x=250,y=120)
        repeat1.select()

        tk.Label(self.root, text="Rozmiar układu:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=160)
        self.size = tk.Entry(self.root)
        self.size.place(x=250,y=165)

        tk.Label(self.root, text="Rozmiar grupy wpływu:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=200)
        self.select_q = tk.Entry(self.root)
        self.select_q.place(x=320,y=205)

        tk.Label(self.root, text="Zagęszczenie ludzi o pozytywnej opinii:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=240)

        self.var_density = tk.DoubleVar()
        density = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_density,length=300, background=self.bg_color)
        density.place(x=50,y=280)

        tk.Label(self.root, text="Prawdopodobieństwo nonkonformizmu:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=330)

        self.var_probability = tk.DoubleVar()
        density = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_probability,length=300, background=self.bg_color)
        density.place(x=50,y=370)

        tk.Label(self.root, text="Prawdopodobieństwo zmiany stanu przy niezależności:",font=(self.text_font, 15),background=self.bg_color).place(x=50,y=420)

        self.var_independ_probability = tk.DoubleVar()
        self.density = tk.Scale(self.root,from_=0, to=1, orient="horizontal", resolution=0.01,variable=self.var_independ_probability,length=300, background=self.bg_color,state=tk.DISABLED)
        self.density.place(x=50,y=460)


        tk.Button(self.root,text="Start",font=(self.text_font, 15),background=self.bg_color,command=self.start_simulation).place(x=50,y=530)
        tk.Button(self.root,text="Pauza",font=(self.text_font, 15),background=self.bg_color,command=self.pause_animation).place(x=140,y=530)
        tk.Button(self.root,text="Wznów",font=(self.text_font, 15),background=self.bg_color,command=self.start_animation).place(x=230,y=530)
        tk.Button(self.root,text="Przerwij",font=(self.text_font, 15),background=self.bg_color,command=self.end_animation).place(x=320,y=530)

        tk.Button(self.root,text="Zamknij program",font=(self.text_font, 15),background="#e61919",command=self.root.quit).place(x=130,y=590)

        self.frame = tk.Frame(self.root)
        self.frame.place(x=650, y=-20)

    def simulation(self,fig):
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
        if self.var_nonconf.get() == 0:
            self.density.config(state=tk.DISABLED)
        elif self.var_nonconf.get() == 1:
            self.density.config(state="normal")


    def start_simulation(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6,7),facecolor=self.bg_color)
        self.anim = self.simulation(fig)

        canvas = FigureCanvasTkAgg(fig, self.frame)

        function = canvas.get_tk_widget()
        function.pack()
    
        self.anim.simulation_show()

    def pause_animation(self):
        self.anim.anim.event_source.stop()

    def start_animation(self):
        self.anim.anim.event_source.start()

    def end_animation(self):
        self.anim.anim.event_source.stop()
    
        for widget in self.frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6,3),facecolor=self.bg_color)

        canvas = FigureCanvasTkAgg(fig, self.frame)

        function = canvas.get_tk_widget()
        function.pack()

    def gui_show(self):
        self.root.mainloop()


if __name__ == "__main__":
    sim = Gui()
    sim.construction()
    sim.gui_show()