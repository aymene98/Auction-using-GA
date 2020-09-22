from PyQt5.QtWidgets import *
import sys
import timeit
from GA import *

class Window(QMainWindow):
    def __init__(self,dimensions,title):
        # creation de l'interface
        super(Window, self).__init__()
        assert len(dimensions) == 4
        self.setGeometry(dimensions[0],dimensions[1],dimensions[2],dimensions[3])
        self.setWindowTitle(title)
        self.addObjects()

    def on_button_clicked(self):
        # fonction qui s'execute apres qu'on click sur le bouton de l'inference
        alert = QMessageBox()
        try:
            it = int(self.line2.text()) # on recupère le nombre d'itération
            stagnation = int(self.line3.text()) # on recupere le max it de stagnation

            offres = getOffres(self.cb.currentText()) # on recupère les offres du fichier donné en paramètre
            g = Genetic(offres) # on cree la classe du GA

            start = timeit.default_timer()
            q = g.solve(offres, it, stagnation) # on execute le GA
            end = timeit.default_timer()

            gain = q[0].gain # le max gain trouver par le GA
            t = end - start
            time = "\nTime : "+ str(t) + "sec."
            res = self.names(q[0]) # les offres prises.
            text = "Gain : " + str(gain) + ". \n" + res + time

            #text = str(it)
            alert.setText(text)
        except Exception as e:
            print(e)
            alert.setText('Iteration field should be a number.') # execption si la champs des it n'est pas un entier
            alert.exec_()

        alert.exec_()

    def names(self,res):
        # pour recupéré les offres et pour construire le string d'affichage.
        liste = []
        for i,v in enumerate(res.solution):
            if v == 1:
                liste.append(i+1)

        s = "Les offres choisi sont : "
        for i in liste:
            s = s + str(i) + " "
        return s


    def addObjects(self):
        # Objet de l'interface
        # Label 1
        self.label1 = QLabel(self)
        self.label1.setText('File name : ')
        self.label1.move(10,10)

        # Combo box nom fichier
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

        # QLineEdit 2 nbr it
        self.line2 = QLineEdit(self)
        self.line2.move(10,100)
        self.line2.resize(250, 20)


        # Label 3 nbr it stagnation permises
        self.label3 = QLabel(self)
        self.label3.setText('Stagnation it : ')
        self.label3.move(10,130)

        # QLineEdit 3
        self.line3 = QLineEdit(self)
        self.line3.move(10,160)
        self.line3.resize(250, 20)

        # Button 1 pour executer le code
        self.button1 = QPushButton(self)
        self.button1.move(80,190)
        self.button1.setText('Run')
        self.button1.clicked.connect(self.on_button_clicked)



app = QApplication(sys.argv)
dims = (300,300,270,230)
w = Window(dims,'Projet E-commerce')

w.show()
sys.exit(app.exec_())
