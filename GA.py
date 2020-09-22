import random
from random import randint
import timeit

#random.seed(123) #pour la reproducibilité des resultats

# param
NUMOFFERS = 1500
MAXOBJECTS = 1500
MAXITERATION = 30
MAXPOPULATION = 10

def cmpOffers(offer1, offer2): # comparer deux offres si elle sont similaires
    for index in range(len(offer1)):
        if (offer1[index] == 1 and offer2[index] == 1):
            return True
    return False

class Offre():
    # classe offre
    def __init__(self,offre,price):
        self.offre = offre
        self.price = price
    def __str__(self):
        return self.offre.__str__() + " price : " + str(self.price)

class Solution():
    # class solution
    def __init__(self, solution, gain=0):
        self.solution = solution # list de 0s et 1s de longeur 1500 (nb objets);
        # a la position i si 1 on prend l'objet i 0 sinon.
        self.gain = gain # gain totale = somme des prix des offres

    def __eq__(self, other):
        return self.solution == other.solution # comparer des solutions.

    def __str__(self):
        return "Solution gain : " + str(self.gain)

    def calculateGain(self, offres):
        # calculer le gain totale = somme des prix des offres
        g = 0
        for i,v in enumerate(self.solution):
            if v == 1:
                g += offres[i].price
        self.gain = g

    def isAcceptable(self,offres):
        # voir si une solution est acceptable
        # pas de conflit entre les offres
        # on compare chaque offre avec les suivants
        for i in range(len(self.solution)):
            y = self.solution[i]
            if self.solution[i] == 1:
                for j in range(i+1,len(self.solution)):
                    x = self.solution[j]
                    if x == 1:
                        if(cmpOffers(offres[i].offre,offres[j].offre) == True):
                            return False
        return True

    def genNeighbors(self):
        # generer toutes les offres voisine
        # mutation de chaque gène flip 1 à 0 et 0 a 1
        # a seul flip donne un voisin.
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
        # flip one bit. i.e. mutation
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
        # chercher parmi tout les voisins ceux qui sont acceptables. pas de conflit d'offres
        n = self.genNeighbors()
        accaptable = []
        for s in n:
            if s.isAcceptable(offres):
                accaptable.append(s)
        return accaptable

    def crossover(self,sol1):
        # croissement
        son1 = []
        son2 = []
        i1 = randint(1,len(self.solution))
        i2 = randint(i1,len(self.solution))

        for x in range(0,i1):
            son1.append(self.solution[x])
            son2.append(sol1.solution[x])

        for x in range(i1,len(self.solution)):
            son1.append(sol1.solution[x])
            son2.append(self.solution[x])

        lson1=Solution(son1)
        lson2=Solution(son2)

        return lson1,lson2

class Genetic():
    def __init__(self,offres):
        # generer une solution qui ne prend aucune offre
        solution = [0] * NUMOFFERS
        self.offers = offres
        s = Solution(solution)
        self.population = s.acceptableNeighbors(offres) # generer ces voisin;
        # rajouter une offre seulement.

        for x in self.population:
            x.calculateGain(offres)

        self.MAXPOPULATION = MAXPOPULATION

        # trier et prendre les meilleurs objets.
        self.population = sorted(self.population,key=lambda s: s.gain,reverse=True)
        self.population = self.population[:MAXPOPULATION]

    def solve(self,offres, maxIterations, stagnation):
        iteration = 0
        max_stagnation_it = stagnation
        stagnation_it = 0
        current_best_fitness = 0
        best_fitness = 0

        while(iteration < maxIterations):
            son1,son2 = self.population[0].crossover(self.population[1]) # croissement des deux meilleurs idiv

            if son1.isAcceptable(offres) == True:
                # si acceptable on calcule le gain et on l'ajoute a la population
                son1.calculateGain(offres)
                self.population.append(son1)

            if son2.isAcceptable(offres) == True:
                # si acceptable on calcule le gain et on l'ajoute a la population
                son2.calculateGain(offres)
                self.population.append(son2)

            c1 = son1.genNeighbor(offres) # mutation et calcule de gain des fils
            c2 = son2.genNeighbor(offres)


            if c1.isAcceptable(offres) == True:
                # si acceptable on calcule le gain et on l'ajoute a la population
                self.population.append(c1)

            if c2.isAcceptable(offres) == True:
                # si acceptable on calcule le gain et on l'ajoute a la population
                self.population.append(c2)

            # trier et tranquer
            self.population = sorted(self.population,key=lambda s: s.gain,reverse=True)
            self.population = self.population[:MAXPOPULATION]
            iteration += 1

            # verifier que l'algorithme de stagne pas sinon on arrete apres une certain nombre d'iterations
            if best_fitness < self.population[0].gain:
                best_fitness = self.population[0].gain
            else:
                if stagnation_it >= max_stagnation_it:
                    print("stagnating at it:", iteration)
                    break
                else:
                    stagnation_it += 1

        return self.population

def getOffres(file):
    # to get the offers file
    name = "./projet/groupe5/instance/in" + file
    offers = open(name,"r")
    header = offers.readline() # removing header

    offersFile = offers.readlines()
    offersList = []

    # and format it into a list
    for offer in offersFile:
        t = offer.split()
        temp = [0]*1500
        value = float(t[0])
        for y in t[1:]:
            temp[int(y)-1] = 1
        offersList.append(Offre(temp,value))

    offers.close()
    return offersList
