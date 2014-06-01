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

        #Attribute to store the hbox lists
        #in the bottom part, to display/acces the QCheckBoxes
        self.list_hbox = []

        #Attribute to store the checkBoxes
        self.list_check_box = []

        #Attribute to store the headers.
        #Multiple list
        self.list_headers = [ [] for x in range(0, 8) ]

        #Attribute to store the volume of the
        #wells and the volume unit, for each line
        self.list_volumes = []

        #Attribute to store the tables
        self.list_table = []

        self.initUI()
        self.connectSlots()


    def connectSlots(self):

        """Method to connect the slots"""

        self.new_solution.returnPressed.connect(self.addSolution)

        #Connecting the double-click on a header cell
        for table in self.list_table:
            table.verticalHeader().sectionDoubleClicked.connect(self.headerFixed)


    def boxChecked(self, index):

        """Slot called when a QCheckBox is checked/unchecked."""

        #Getting the tab index, or the table index where the
        #checkbox has been checked/unchecked
        index = self.list_check_box.index(self.sender()) % 8

        #Getting the name of the checkbox
        name = self.sender().text()

        #If checked
        if self.sender().checkState() == QtCore.Qt.Checked:

            #Insert a row in the table
            self.list_table[index].insertRow(self.list_table[index].rowCount())

            #Define the vertical header labels
            self.list_headers[index].append(name)
            self.list_table[index].setVerticalHeaderLabels(self.list_headers[index])

        #If unchecked
        elif self.sender().checkState() == QtCore.Qt.Unchecked:

            #For all the rows in the table, find the good one based on the
            #header label
            for row in range(self.list_table[index].rowCount()):

                #if the name of the vertical header label matches
                if self.list_table[index].verticalHeaderItem(row).text() == name \
                    or self.list_table[index].verticalHeaderItem(row).text() == name + "\n(fixed)":

                    #Remove row of the table
                    self.list_table[index].removeRow(row)

                    #Try to remove the name of the headers list
                    try:
                        self.list_headers[index].remove(name + "\n(fixed)")
                    except ValueError:
                        self.list_headers[index].remove(name)
                    break


    def addSolution(self):

        """Method to create a new solution"""

        #Counting the number of rows in the up part,
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

        #Creating the checkbox in every tab
        for hbox_down in self.list_hbox:
            check_box = QCheckBox(name_solution)
            check_box.stateChanged.connect(self.boxChecked)

            hbox_down.addWidget(check_box)
            self.list_check_box.append(check_box)

        #Display matter
        self.up_grid.setColumnStretch(1, 1)
        self.up_grid.setColumnStretch(2, 3)

        self.new_solution.clear()


    def headerFixed(self, index):


        """Slot called when a header section is double clicked"""

        #Getting the right table
        table = self.sender().parent()

        #Getting the index of the table
        number = self.list_table.index(table)

        #If the line is not fixed already
        if not "fixed" in self.list_headers[number][index]:

            #Setting the header labels
            self.list_headers[number][index] += "\n(fixed)"
            table.setVerticalHeaderLabels(self.list_headers[number])

            #Make each cell non editable
            for column in range(table.columnCount()):

                item = QTableWidgetItem() 
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackgroundColor(QtCore.Qt.lightGray)

                #Replacing the old values in their cell
                if table.item(index, column):
                    old_value = table.item(index, column).text()
                    item.setText(old_value)

                table.setItem(index, column, item)

        #Make the row editable
        else:

            #Setting the header labels
            self.list_headers[number][index] = self.list_headers[number][index].replace("\n(fixed)", "")
            table.setVerticalHeaderLabels(self.list_headers[number])

            #Make the cells editable again
            for column in range(table.columnCount()):

                item = table.item(index, column)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackgroundColor(QtCore.Qt.white)


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
        self.down_widget = QTabWidget()
        self.down_widget.setMinimumHeight(600)

        letters = "ABCDEFGH"

        for letter in letters:

            #Global widget, containing the layout
            widget = QWidget()

            #Box to contain the checkboxes, in a
            #horizontal box, and the table
            vbox_down = QVBoxLayout()

            #Hbox to store a label, a spinbox and a combobox.
            #They determine what is the wells volume for one table
            hbox_volume = QHBoxLayout()
            hbox_volume.setAlignment(QtCore.Qt.AlignLeft)

            label_volume = QLabel("Volume samples : ")

            #Spinbox for the volume of the wells
            spinbox_volume = QSpinBox()
            spinbox_volume.setMinimum(0)
            spinbox_volume.setMaximum(5000)
            spinbox_volume.setSingleStep(1)

            #Combobox for the volume unit
            combobox_volume = QComboBox()
            combobox_volume.addItems(["µL", "mL", "L"])

            #Building the wells volume hbox
            hbox_volume.addWidget(label_volume)
            hbox_volume.addWidget(spinbox_volume)
            hbox_volume.addWidget(combobox_volume)

            #hbox for the checkboxes
            hbox_down = QHBoxLayout()
            hbox_down.setAlignment(QtCore.Qt.AlignLeft)

            #Adding the box to the hbox_list
            self.list_hbox.append(hbox_down)

            #TabWidget for the wells lines
            table = QTableWidget(0, 12)

            #Creating an item prototype. The table
            #will use it as default when a cell is edited
            proto_item = QTableWidgetItem()
            proto_item.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItemPrototype(proto_item)

            vbox_down.addLayout(hbox_volume)
            vbox_down.addLayout(hbox_down)
            vbox_down.addWidget(table)

            #Adding the table to the list of tables
            self.list_table.append(table)

            widget.setLayout(vbox_down)

            self.down_widget.addTab(widget, letter)


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
