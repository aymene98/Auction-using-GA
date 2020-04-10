from PyQt5.QtWidgets import *
import sys
import random
from random import randint
import timeit

random.seed(123)

NUMOFFERS = 1500
MAXOBJECTS = 1500
MAXPOPULATION = 4


def cmpOffers(offer1, offer2):
    for index in range(len(offer1)):
        if (offer1[index] == 1 and offer2[index] == 1):
            return True
    return False

class Offre():
    def __init__(self,offre,price):
        self.offre = offre
        self.price = price
    def __str__(self):
        return self.offre.__str__() + " price : " + str(self.price)
    
class Solution():
    def __init__(self, solution, gain=0):
        # Solution : vector of 0s and 1s
        self.solution = solution
        self.gain = gain

    def __eq__(self, other):
        return self.solution == other.solution
        
    def __str__(self):
        return "Solution gain : " + str(self.gain)
    
    def calculateGain(self, offres):
        g = 0
        for i,v in enumerate(self.solution):
            if v == 1:
                # we take the offre
                g += offres[i].price
        self.gain = g
    
    def isAcceptable(self,offres):
        for i in range(len(self.solution)):
            y = self.solution[i]
            if y == 1:
                for x in range(i+1,len(self.solution)-1):
                    if self.solution[x] == 1:
                        if(cmpOffers(offres[x].offre,offres[y].offre)):
                            return False
        return True
    
    def genNeighbors(self):
        neighbors=[]
        for index in range(len(self.solution)):
            n = self.solution.copy()
            if n[index] == 0:
                n[index]=1
            else:
                n[index]=0
            neighbors.append(Solution(n))
        return neighbors
    
    def genNeighbor(self, offres):
        i = 0
        sol = Solution(self.solution.copy())
        while i < MAXOBJECTS:
            index = randint(0,MAXOBJECTS-1)
            n = self.solution.copy()
            if n[index] == 0:
                n[index]=1
            else:
                n[index]=0
            
            sol.solution = n
            sol.calculateGain(offres)
            if sol.isAcceptable(offres) :
                return sol
            i += 1

        return sol

    def acceptableNeighbors(self,offres):
        n = self.genNeighbors()
        accaptable = []
        for s in n:
            if s.isAcceptable(offres):
                accaptable.append(s)
        return accaptable

    def crossover(self,sol1):
        son1 = []
        son2 = []
        i = randint(1,len(self.solution))

        for x in range(0,i):
            son1.append(self.solution[x])
            son2.append(sol1.solution[x])

        for x in range(i,len(self.solution)):
            son1.append(sol1.solution[x])
            son2.append(self.solution[x])
            
        lson1=Solution(son1)
        lson2=Solution(son2)
        
        return lson1,lson2

class Genetic():
    def __init__(self,offres):
        solution = [0] * NUMOFFERS
        self.offres = offres
        s = Solution(solution)
        self.population = s.acceptableNeighbors(offres)
        for x in self.population:
            x.calculateGain(offres)
        self.MAXPOPULATION = MAXPOPULATION
        self.population = sorted(self.population,key=lambda s: s.gain,reverse=True)
        self.population = self.population[:MAXPOPULATION]
        
    def solve(self,offres, maxIterations):
        iteration = 0
        while(iteration < maxIterations):
            children = []
            for p in self.population:
                # c: acceptable neighbors of each member of the population
                #c = p.acceptableNeighbors(offers)
                #for x in c:
                #    x.calculateGain(offres)
                #    if x not in self.population and x not in children:
                #        children.append(x)
                c = p.genNeighbor(offres)
                if c not in self.population and c not in children :
                    children.append(c)

            for x in children:
                self.population.append(x)

            self.population = sorted(self.population,key=lambda s: s.gain,reverse=True)
            son1,son2 = self.population[0].crossover(self.population[1])
            
            son1.calculateGain(offres)
            son2.calculateGain(offres)
            
            self.population.extend((son1,son2))

            self.population = sorted(self.population,key=lambda s: s.gain,reverse=True)
            self.population = self.population[:MAXPOPULATION]
            iteration += 1

            #if iteration % 10 == 0:
            #    print("iteration :", iteration)
            
        return self.population

def getOffres(file):
    name = "./projet/groupe5/instance/in" + file
    print(name)
    offers = open(name,"r")
    header = offers.readline() # removing header

    offersFile = offers.readlines()
    offersList = []

    for offer in offersFile:
        t = offer.split()
        temp = [0]*1500
        value = float(t[0])
        for y in t[1:]:
            temp[int(y)-1] = 1
        offersList.append(Offre(temp,value))
    
    offers.close()
    return offersList


class Window(QMainWindow):
    def __init__(self,dimensions,title):
        super(Window, self).__init__()
        assert len(dimensions) == 4
        self.setGeometry(dimensions[0],dimensions[1],dimensions[2],dimensions[3])
        self.setWindowTitle(title)
        self.addObjects()
    
    def on_button_clicked(self):
        alert = QMessageBox()
        try:
            it = int(self.line2.text())
            offres = getOffres(self.cb.currentText())
            g = Genetic(offres)
            print(len(g.population))

            start = timeit.default_timer()
            q = g.solve(offres,it)
            end = timeit.default_timer()

            gain = q[0].gain
            t = end - start
            time = "\nTime : "+ str(t) + "sec."
            res = self.names(q[0])
            text = "Gain : " + str(gain) + ". \n" + res + time

            #text = str(it)
            alert.setText(text)
        except Exception:
            alert.setText('Iteration field should be a number.')
            alert.exec_()
        
        
        alert.exec_()

    def names(self,res):
        liste = []
        for i,v in enumerate(res.solution):
            if v == 1:
                liste.append(i+1)

        s = "Les offres choisi sont : "
        for i in liste:
            s = s + str(i) + " "
        
        return s
        
    
    def addObjects(self):
        # Label 1
        self.label1 = QLabel(self)
        self.label1.setText('File name : ')
        self.label1.move(10,10)

        # Combo box 
        self.cb = QComboBox(self)
        for i in range(1,100):
            if i < 10 :
                s = "60" + str(i)
            else:
                s = "6" + str(i)
            self.cb.addItem(s)
        self.cb.addItem("700")
        self.cb.move(10,40)

        # Label 2
        self.label2 = QLabel(self)
        self.label2.setText('Number of it : ')
        self.label2.move(10,70)

        # QLineEdit 2
        self.line2 = QLineEdit(self)
        self.line2.move(10,100)
        self.line2.resize(250, 20);

        # Button 1
        self.button1 = QPushButton(self)
        self.button1.move(80,130)
        self.button1.setText('Run')
        self.button1.clicked.connect(self.on_button_clicked)

    

app = QApplication(sys.argv)
dims = (300,300,270,170)
w = Window(dims,'Projet E-commerce')

w.show()
sys.exit(app.exec_())

