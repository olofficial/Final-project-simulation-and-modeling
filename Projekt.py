import pylab as plt
import random as rnd
import numpy as np
import matplotlib
import math

# Collection of squares with methods to place oases and populate with animals
class Grid():
    def __init__(self, n):
        self.n = n
        self.oasissquares = []
        self.desertsquares = []
        self.herbs = []
        self.mesos = []
        self.apices = []
        self.list = self._fill()

    # Fills grid with desert squares
    def _fill(self):
        list = []
        row = []
        for y in range(self.n):
            for x in range(self.n):
                square = Desert(x, y)
                #square = Oasis(x, y)
                row.append(square)
                self.desertsquares.append(square)
            list.append(row)
            row = []
        return list

    # Fills grid with aasis biomes
    def biomize(self, nr, d):
        for _ in range(nr):
            x0 = rnd.randint(0, self.n - 1)
            y0 = rnd.randint(0, self.n - 1)
            for x in range(int(x0-d/2), int(x0+d/2+1)):
                for y in range(int(y0-d/2), int(y0+d/2+1)):
                    if 0 <= x <= self.n-1  and 0 <= y <= self.n-1:
                        oldsquare = self.list[x][y]
                        if type(oldsquare) == Desert:
                            self.desertsquares.remove(oldsquare)
                            newsquare = Oasis(x, y)
                            self.list[x][y] = newsquare
                            self.oasissquares.append(newsquare)
                            
    #biomizes with fixed oases
    def biomize2(self, w):
        x0s = [int(self.n*1/4), int(self.n*3/4)]
        y0s = [int(self.n*1/4), int(self.n*3/4)]
        for x0 in x0s:
            for y0 in y0s:
                for x in range(int(x0-w/2), int(x0+w/2+1)):
                    for y in range(int(y0-w/2), int(y0+w/2+1)):
                        if 0 <= x <= self.n-1  and 0 <= y <= self.n-1:
                            oldsquare = self.list[x][y]
                            if type(oldsquare) == Desert:
                                self.desertsquares.remove(oldsquare)
                                newsquare = Oasis(x, y)
                                self.list[x][y] = newsquare
                                self.oasissquares.append(newsquare)


    # Randomly places h herbs, m mesos and a apices on grid
    def animalize(self, h, m, a):
        for _ in range(h):
            x = rnd.randint(0, self.n - 1)
            y = rnd.randint(0, self.n - 1)
            while self.list[x][y].animal != None:
                x = rnd.randint(0, self.n - 1)
                y = rnd.randint(0, self.n - 1)
            herb = Herb(x, y)
            self.list[x][y].animal = herb
            self.list[x][y].occupied = True
            self.herbs.append(herb)
        for _ in range(m):
            x = rnd.randint(0, self.n - 1)
            y = rnd.randint(0, self.n - 1)
            while self.list[x][y].animal != None:
                x = rnd.randint(0, self.n - 1)
                y = rnd.randint(0, self.n - 1)
            meso = Meso(x, y)
            self.list[x][y].animal = meso
            self.list[x][y].occupied = True
            self.mesos.append(meso)
        for _ in range(a):
            x = rnd.randint(0, self.n - 1)
            y = rnd.randint(0, self.n - 1)
            while self.list[x][y].animal != None:
                x = rnd.randint(0, self.n - 1)
                y = rnd.randint(0, self.n - 1)
            apex = Apex(x, y)
            self.list[x][y].animal = apex
            self.list[x][y].occupied = True
            self.apices.append(apex)

    #kills an animal
    def kill(self, animal):
        self.list[animal.x][animal.y].animal = None
        self.list[animal.x][animal.y].occupied = False
        if type(animal) == Herb:
            self.herbs.remove(animal)
        elif type(animal) == Meso:
            self.mesos.remove(animal)
        else:
            self.apices.remove(animal)


    #prints the grid at a given time step
    def print_grid(self):
        data = np.ones((self.n, self.n)) * np.nan
        for square in self.oasissquares:
            if square.greens:
                data[square.x, square.y] = 1

        for herb in self.herbs:
            data[herb.x,herb.y]=2
        for meso in self.mesos:
            data[meso.x, meso.y]=3
        for apex in self.apices:
            data[apex.x, apex.y]= 4

        fig, ax = plt.subplots(1, 1, tight_layout=True)
        my_cmap = matplotlib.colors.ListedColormap(['g','w', 'b', 'r' ])
        my_cmap.set_bad(color='y')

        # draw the grid
        for x in range(self.n + 1):
            ax.axhline(x, lw=2, color='k', zorder=5)
            ax.axvline(x, lw=2, color='k', zorder=5)
        # draw the boxes
        ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, self.n, 0, self.n], zorder=0)
        # turn off the axis labels
        ax.axis('off')
        plt.show()


# Squares of the grid
class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.animal = None
        self.greens = False

# Childclass of Square with bare land
class Desert(Square):
    pass

# Childclass of Square with fertile land
class Oasis(Square):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.greens = True

    def refill(self, p):
        if rnd.random() < p:
            self.greens = True

class Animal():
    def __init__(self, x, y, foodres = 5):
        self.x = x
        self.y = y
        self.res = foodres

    #spawns an animal in the moore neighborhood of the parent
    def spawn(self, grid, d):
        animaltype = type(self)
        baby = animaltype(self.x, self.y, 4)
        x = self.x + rnd.randint(int(-d/2), int(d/2))
        y = self.y + rnd.randint(int(-d/2), int(d/2))
        for _ in range(2*d):
            if (x < 0 or x > grid.n-1 or y < 0 or y > grid.n-1) or grid.list[x][y].animal != None: #(not (0 <= x <= grid.n-1) or not (0 <= y <= grid.n-1)):
                x = self.x + rnd.randint(int(-d/2)-2, int(d/2)+2)
                y = self.y + rnd.randint(int(-d/2)-2, int(d/2)+2)
            else:
                baby.x = x
                baby.y = y
                grid.list[x][y].occupied = True
                grid.list[x][y].animal = baby
                if type(baby) == Herb:
                    grid.herbs.append(baby)
                elif type(baby) == Meso:
                    grid.mesos.append(baby)
                else:
                    grid.apices.append(baby)
                break

class Apex(Animal):
    pass

class Meso(Animal):
    pass

class Herb(Animal):
    pass

#checks if something is in range of something else
def check_in_range(grid, x0, y0, d, yumyum = Herb, apex = False):
    for x in range(int(x0-d/2), int(x0+d/2)):
        for y in range(int(y0-d/2), int(y0+d/2)):
            if 0 <= x <= grid.n-1  and 0 <= y <= grid.n-1:
                if not(x == x0 and y == y0):
                    if type(grid.list[x][y].animal) == yumyum:
                        return True, x, y
                    if apex:
                        if type(grid.list[x][y].animal) == Meso:
                            return True, x, y
    return False, None, None



class CellularAutomaton():
    def __init__(self, grid):
        self.grid = grid

    #concatenates the animal lists to iterate through for the method step
    def _animal_list(self):
        return self.grid.herbs + self.grid.mesos + self.grid.apices

    #returns hma
    def hma(self, flag):
        if flag:
            return len(self.grid.herbs) * len(self.grid.mesos) * len(self.grid.apices)
        else:
            return len(self.grid.herbs) * len(self.grid.mesos) + len(self.grid.herbs) * len(self.grid.apices) + len(self.grid.mesos) * len(self.grid.apices)
    #time step method
    def timestep(self, maxres=10, d=2, sexylimit=5, p=0.5, show =False, step=0):
        if show:
            self.grid.print_grid()
        for animal in self._animal_list():
            self._step(animal)
            animal.res -= 1

        #Herbs eating
        for herb in self.grid.herbs:
            if self.grid.list[herb.x][herb.y].greens:
                herb.res = maxres
                self.grid.list[herb.x][herb.y].greens = False

        #Mesos eating
        for meso in self.grid.mesos:
            near, x, y = check_in_range(self.grid, meso.x, meso.y, d, Herb)
            if near:
                if meso.res < maxres:
                    meso.res = maxres
                    self.grid.kill(self.grid.list[x][y].animal)
            elif self.grid.list[meso.x][meso.y].greens and meso.res <= 3:
                meso.res = maxres//2
                self.grid.list[meso.x][meso.y].greens = False

        # Apices eating
        for apex in self.grid.apices:
            near, x, y = check_in_range(self.grid, apex.x, apex.y, d, Herb)
            if near:
                if apex.res < maxres:
                    apex.res = maxres
                    self.grid.kill(self.grid.list[x][y].animal)
                    continue
            near, x, y = check_in_range(self.grid, apex.x, apex.y, d, Meso)
            if near: 
                if apex.res < maxres:
                    apex.res = maxres
                    self.grid.kill(self.grid.list[x][y].animal)

        # Starving and reproducing
        for herb in self.grid.herbs:
            if herb.res <= 0:
                self.grid.kill(herb)
            elif herb.res >= sexylimit:
                near, x, y = check_in_range(self.grid, herb.x, herb.y, d, Herb)
                if near:
                    herb.res -= 3
                    herb.spawn(self.grid, d)

        for meso in self.grid.mesos:
            if meso.res <= 0:
                self.grid.kill(meso)
            elif meso.res >= sexylimit:
                near, x, y = check_in_range(self.grid, meso.x, meso.y, d, Meso)
                if near:
                    meso.res -= 3
                    meso.spawn(self.grid, d)

        for apex in self.grid.apices:
            if apex.res <= 0:
                self.grid.kill(apex)
            elif apex.res >= sexylimit:
                near, x, y = check_in_range(self.grid, apex.x, apex.y, d, Apex)
                if near:
                    apex.res -= 3
                    apex.spawn(self.grid, d)

        # Food refill oasis
        for square in self.grid.oasissquares:
            square.refill(p)
        self.animal_list = self._animal_list()

    #random number generator
    def _random_number(self):
        return int(rnd.random() * 4)

    #step method, moves an animal randomly
    def _step(self, animal):
        num = self._random_number()
        match num:
            case 0:
                self._move(animal, "left")
            case 1:
                self._move(animal, "right")
            case 2:
                self._move(animal, "down")
            case 3:
                self._move(animal, "up")

    #checks if animal can move, then moves it
    def _move(self, animal, direction):
        self.grid.list[animal.x][animal.y].occupied = False
        self.grid.list[animal.x][animal.y].animal = None
        if direction == "left":
            if animal.x >= 1:
                if self.grid.list[animal.x - 1][animal.y].occupied == False:
                    animal.x -= 1
            else:
                if self.grid.list[self.grid.n - 1][animal.y].occupied == False:
                    animal.x = self.grid.n - 1
        elif direction == "right":
            if animal.x < self.grid.n - 1:
                if self.grid.list[animal.x + 1][animal.y].occupied == False:
                    animal.x += 1
            else:
                if self.grid.list[0][animal.y].occupied == False:
                    animal.x = 0
        elif direction == "down":
            if animal.y >= 1:
                if self.grid.list[animal.x][animal.y - 1].occupied == False:
                    animal.y -= 1
            else:
                if self.grid.list[animal.x][self.grid.n - 1].occupied == False:
                    animal.y = self.grid.n - 1
        elif direction == "up":
            if animal.y <= self.grid.n - 2:
                if self.grid.list[animal.x][animal.y + 1].occupied == False:
                    animal.y += 1
            else:
                if self.grid.list[animal.x][0].occupied == False:
                    animal.y = 0
        self.grid.list[animal.x][animal.y].animal = animal
        self.grid.list[animal.x][animal.y].occupied = True

class Simulation():
    def __init__(self, n = 40, N = 1000, nr = 10, w = 20, h = 128, m = 64, a = 48):
        self.grid = Grid(n)
        #self.grid.biomize(nr, d)
        self.grid.biomize2(w)
        self.grid.animalize(h, m, a)
        self.N = N

    #checks if hma = 0
    def _hma_check(self, automaton, three_flag = True):
        if automaton.hma(three_flag) == 0:
            return True
        else:
            return False
    
    #runs the simulation for N time steps, either plots the results, returns T_e or returns the population numbers
    def run(self, returning = False, hma_flag = True, three_flag = True):
        cell_auto = CellularAutomaton(self.grid)
        observable_lists = [[], [], [], []]
        number_lists = [[], [], [], []]
        label_list = ["Herbs", "Mesos", "Apices", "hma"]
        #cell_auto.timestep(show=True)
        for i in range(self.N):
            observable_lists[0].append(len(cell_auto.grid.herbs))
            observable_lists[1].append(len(cell_auto.grid.mesos))
            observable_lists[2].append(len(cell_auto.grid.apices))
            observable_lists[3].append(cell_auto.hma(three_flag))
            cell_auto.timestep(step=i)
            if hma_flag == True:
                if self._hma_check(cell_auto, three_flag) == True:
                    return i
        #cell_auto.timestep(show=True)
        if hma_flag == False:
            # for i in range(3):#range(len(number_lists)):
            #     for j in range(self.N):
            #         number_lists[i].append(observable_lists[i][j])
                #self.plotobservables(number_lists[i], label_list[i])

            self.phase_plot(observable_lists[0], observable_lists[2])
        if returning:
            return len(cell_auto.grid.herbs), len(cell_auto.grid.mesos), len(cell_auto.grid.apices)
        if hma_flag:
            return self.N

    #resets the grid
    def reset(self):
        self.grid = None
        self.N = None

    #plots random walk
    def plot_2D(self, xy_list):
        x_path = []
        y_path = []
        for step in range(len(xy_list)):
            x_path.append(xy_list[step].x)
            y_path.append(xy_list[step].y)
        plt.plot(x_path, y_path)

    #plots individual numbers over time
    def plotobservables(self, y_list, plot_label):
        if plot_label:
            x_list = range(self.N)
            plt.plot(x_list, y_list, label = plot_label)
            plt.xlabel("Time")
            plt.ylabel("Number of individuals")
            plt.legend()

    #phase plot method
    def phase_plot(self, list1, list2):
        plt.plot(list1[200:], list2[200:])
        plt.xlabel("Herbs")
        plt.ylabel("Apices")

#plots a "fundamental diagram" with mean actor number over density
def fundamental_diagram():
    n  = 100
    total = n**2
    sum = 8+4+3
    end = total//sum
    density = []
    her = []
    mes = []
    api = []
    for i in range(end):
        density.append(sum*i/total)
        herbsnr = []
        mesosnr = []
        apicesnr = []
        for nrsims in range(10):
            sim = Simulation(n, 300, nr=5, w=40, h=8*i, m=4*i, a=3*i)
            herbs, mesos, apices = sim.run(returning = True)
            herbsnr.append(herbs)
            mesosnr.append(mesos)
            apicesnr.append(apices)
        her.append(np.mean(herbsnr))
        mes.append(np.mean(mesosnr))
        api.append(np.mean(apicesnr))
    plt.plot(density, her, label="Herbs")
    plt.plot(density, mes, label="Mesos")
    plt.plot(density, api, label="Apices")
    plt.legend()
    plt.show()

#calculate standard error
def sterr(n, r):
    return math.sqrt((1 / ( n - 1) ) *np.var(r))

# calculates standard error and mean for timestep > 200
def accuracy(herb, meso, apex, filename):
    nrsims = [i for i in range(149,151)]
    hersterr = []
    messterr = []
    apisterr = []
    for nrsim in nrsims:
        her = []
        mes = []
        api = []
        for _ in range(nrsim):
            sim = Simulation(40, 1000, nr=5, w=20, h=herb, m=meso, a=apex)
            herbs, mesos, apices = sim.run(returning = True, hma_flag=False)
            her.append(herbs)
            mes.append(mesos)
            api.append(apices)
        print("herbs",sterr(nrsim, her), np.mean(her))
        print("mesos",sterr(nrsim, mes), np.mean(mes))
        print("apices",sterr(nrsim, api), np.mean(api))
        hersterr.append(sterr(nrsim, her))
        #messterr.append(sterr(nrsim, sterr(mes)))
        apisterr.append(sterr(nrsim, api))
    plt.plot(nrsims, hersterr, label="Herbs")
    plt.plot(nrsims, apisterr, label="Apices")
    plt.xlabel("Nr simulations")
    plt.ylabel("Standard error")
    plt.legend()
    plt.savefig(filename)
    #plt.show()

#parameter study of density
def param_rho(three):
    rho = np.linspace(0,0.6, 20)
    n = 40
    N = 1000
    y_list = []
    ints = [8, 4, 3]
    norm = np.sum(ints)
    ratio = ints/norm
    for i in rho[1:]:
        t_list = []
        for _ in range(10):
            sim = Simulation(n, N, nr = 1, w = int(0.5*n), h = int(ratio[0]*i*n**2), m = int(ratio[1]*i*n**2), a = int(ratio[2]*i*n**2))
            t_list.append(sim.run(three_flag = three))
        y_list.append(np.mean(t_list))
    if three == True:
        plt.plot(rho[1:], y_list, label = "3 actors")
    else:
        plt.plot(rho[1:], y_list, label = "2 actors")
    plt.xlabel("Density")
    plt.ylabel("T_e")
    #plt.show()

def param_size():
    ns = [4*i for i in range(25)]
    ratioh = 128/1600
    ratiom = 64/1600
    ratioa = 48/1600
    t_es = []
    for n in ns:
        t_es_temp = []
        for _ in range(5):
            sim = Simulation(n, 1000, nr=10, w=0.5*n, h=int(ratioh*n**2), m=int(ratiom*n**2), a=int(ratioa*n**2))
            t_e = sim.run(three_flag = False)
            t_es_temp.append(t_e)
        t_es.append(np.mean(t_es_temp))
    plt.plot(ns, t_es)
    plt.xlabel("n")
    plt.ylabel("T_e")
    plt.show()

#parameter study of oasis width
def param_oasiswidth(three_flag):
    widths = [i for i in range(0,16)]
    ratioh = 400/10000
    ratiom = 200/10000
    ratioa = 150/10000
    t_es = []
    for width in widths:
        t_es_temp = []
        for _ in range(50):
            sim = Simulation(n=40, N=1000, nr=0, w=width, h=128, m=64, a=48)
            t_e = sim.run(three_flag = three)
            t_es_temp.append(t_e)
        t_es.append(np.mean(t_es_temp))
    plt.plot(widths, t_es, label=string)
    plt.xlabel("w")
    plt.ylabel("T_e")
    #plt.show()

#parameter study of actor ratio
def param_ratio(index, three, label_string):
    rat = np.linspace(0.7,1.3,10)
    n = 40
    N = 1000
    y_list = []
    
    x_list = [100*i for i in rat]
    for i in rat:
        int_list = [128, 64, 48]
        int_list[index] = int(int_list[index] * i)
        t_list = []
        for _ in range(5):
            sim = Simulation(n, N, nr = 1, w = int(0.4*n), h = int_list[0], m = int_list[1], a = int_list[2])
            t_list.append(sim.run(three_flag = three))
        y_list.append(np.mean(t_list))
    plt.plot(x_list, y_list, label = label_string)
    plt.xlabel("Relative ratio")
    plt.ylabel("T_e")

def main():
    #t_e()
    #sim = Simulation(m = 0)
    #sim.run(hma_flag = False)
    #plt.show()
    #fundamental_diagram()
    #param_size()
    #param_rho(three=True)
    #param_rho(three=False)
    #param_ratio(0, True, "3 actors")
    #param_ratio(0, False, "2 actors")
    #plt.legend()
    #plt.show()
    #accuracy(128, 0, 48, "./bilder/2-actors-herbapex1.png")
    #accuracy(0, 64, 48, "./bilder/2-actors-mesoapex1.png")
    #accuracy(128, 64, 48, "./bilder/3-actors1.png")
    print("Hello world!")


if __name__ == "__main__":
    main()