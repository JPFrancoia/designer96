#!/usr/bin/python
# -*-coding:Utf-8 -*

import sys
import os
from PyQt4 import QtSql, QtCore
from PyQt4.QtGui import *


#Pour les modules persos
sys.path.append('/home/djipey/informatique/python/batbelt')
from easyxls import EasyXls
import batbelt
import log


class Fenetre(QMainWindow):
    

    def __init__(self):

        # On hérite de QMainWindow et de Fenetre, on appelle dc les 2
        #constructeurs
        super(Fenetre, self).__init__()

        #Logger
        self.l = log.MyLog(total=False)

        #Attribute to store the solutions
        self.dico_solutions = {}

        self.initUI()
        self.connectSlots()


    def connectSlots(self):

        """Method to connect the slots"""

        self.new_solution.returnPressed.connect(self.addSolution)


    def addSolution(self):

        """Method to create a new solution"""

        #Counting the nulber of rows in the up part,
        #to determine where to add the new solution
        last_row = self.up_grid.rowCount()

        #Getting the name of the new solution
        name_solution = self.new_solution.text()

        #Creating to lineEdit to contain the concentration
        #and the comments
        tuple_line = QLineEdit(), QLineEdit()

        if name_solution in self.dico_solutions.keys():
            return

        self.dico_solutions[name_solution] = tuple_line

        #Add a new line for a new solution:
            #- Label (name of the solution)
            #- First line edit (concentration)
            #- Second line edit (comments)
        self.up_grid.addWidget(QLabel(name_solution), last_row, 0)
        self.up_grid.addWidget(tuple_line[0], last_row, 1)
        self.up_grid.addWidget(tuple_line[1], last_row, 2)

        self.down_grid.addWidget(QLabel(name_solution), 0, len(self.dico_solutions) - 1)

        self.up_grid.setColumnStretch(1, 1)
        self.up_grid.setColumnStretch(2, 3)

        self.new_solution.clear()


    def initUI(self):               

        """Méthode pour créer la fenêtre et régler ses paramètres"""

        #Window parameters
        self.setGeometry(0, 25, 1900 , 1020)
        self.setWindowTitle('Designer96')    

        #Widget for the top part
        self.up_widget = QWidget()
        self.up_grid = QGridLayout()

        #Grid layout for the top part
        self.up_widget.setLayout(self.up_grid)
        self.up_grid.setColumnStretch(1, 1)

        #Line to add new solutions
        self.new_solution = QLineEdit()

        self.up_grid.addWidget(QLabel("New solution"), 0, 0)
        self.up_grid.addWidget(self.new_solution, 0, 1, QtCore.Qt.AlignLeft)
        self.up_grid.addWidget(QLabel("Work in :"), 0, 3)
        self.up_grid.addWidget(QComboBox(), 0, 4)


        #---------------------------- BOTTOM PART --------------------------------

        #Widget for the bottom part
        self.down_widget = QWidget()

        #Grid for the bottom part
        self.down_grid = QGridLayout()
        self.down_widget.setLayout(self.down_grid)

        #TabWidget for the wells lines
        self.down_tab = QTabWidget()
        self.down_tab.addTab(QTableWidget(1, 12), "Line")

        self.down_grid.addWidget(self.down_tab, 1, 0, 1, 100)


        #---------------------------- ASSEMBLING --------------------------------

        #Splitter containing the top and bottom parts
        self.v_splitter = QSplitter(QtCore.Qt.Vertical)
        self.v_splitter.addWidget(self.up_widget)
        self.v_splitter.addWidget(self.down_widget)

        self.setCentralWidget(self.v_splitter)

        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fenetre()
    sys.exit(app.exec_())
