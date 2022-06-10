from os import name
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from numba import jit

class Simulation:

    def __init__(self,fig,q,p,f,x,L,nonconf=0,rep=1):

        """ 
        The function initializing simulation 
        
        params
        ------
        fig  - figure on which a simulation will be displayed
        q - number of neighbors we draw
        p - probability of non-conformism
        f - the probability of changing the state (for independence)
        x - density of people with a positive opinion
        L - mesh dimension
        nonconf - 1: independence, 0: anticonformism 
        rep - 1: with repetition, 0: without repetition
        """

        self.fig = fig
        self.ax1 = fig.add_subplot(211)
        self.ax1.set_title("Q-voter model for q = {}".format(q))
        self.ax1.axis("off")

        self.ax2 = fig.add_subplot(212)
        self.ax2.set_ylim(-1.5,1.5)
        self.ax2.set_xlabel("time")
        self.ax2.set_ylabel("average opinion")

        self.q = q # how many neighbors we draw
        self.p = p # the probability of non-conformism
        self.f = f # the probability of changing the state (for independence)
        self.L = L # mesh dimension
        self.N = self.L**2
        self.nonconf = nonconf
        self.rep = rep

        self.x = x # density of people with a positive opinion
        self.S = np.random.permutation([1]*round(x*self.N) + [-1]*(self.N - round(x*self.N)))
        self.S = self.S.reshape((self.L, self.L))

        self.fps = 30
        self.heat_map = self.ax1.imshow(np.copy(self.S), vmin=-1, vmax=1, cmap="cubehelix")
        self.time, self.average_opinion = [0], [0]
        self.line, = self.ax2.plot(self.time,self.average_opinion,color="k")

        self.global_time = 0

    def animate_func(self,i):

        """ 
        The function that creates animation,
        is used as parameter in animation.FuncAnimation object
        """
    
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

            if self.nonconf == 0: # anticonformism
                if np.abs(np.sum(inf)) == self.q:
                    U = np.random.random()
                    if U <= self.p:
                        self.S[i][j] = -np.sum(inf)/self.q
                    else:
                        self.S[i][j] = np.sum(inf)/self.q
            elif self.nonconf == 1: # independence
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

        """ Function responsible for displaying simulation """

        self.anim = animation.FuncAnimation(
                                    self.fig, 
                                    self.animate_func,
                                    interval = 100 / self.fps, # in ms
                                    repeat = False
                                    )

        plt.show()

if __name__ == "__main__":
    fig = plt.figure(figsize = (6,6))
    simulation = Simulation(fig,2,0.5,0.5,0.5,5,0,0)
    simulation.simulation_show()