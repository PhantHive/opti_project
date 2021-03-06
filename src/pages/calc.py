from decimal import Decimal

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QRadioButton, \
    QGraphicsDropShadowEffect
from src.canvas.Canvas import Canvas
from src.maths.functions import Functions
from src.maths.gradient import Gradient
from src.maths.graph import Graph


class Calculator(object):

    intervalx = [None, None]
    intervaly = [None, None]
    equation = 1

    def __init__(self):
        '''
        every possible configuration
        '''
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = int(self.screen.width() * 0.70)
        self.height = int(self.screen.height() * 0.50)

        self.lang = None
        self.back_bt = None

        self.functions = ["f", "Rosenbrock", "g1", "g2", "g3"]
        self.fct_der = ["f_der", "Ros_der", "g1_der", "g2_der", "g3_der"]
        self.fct_h = ["H_f", "H_Ros", "H_g1", "H_g2", "H_g3"]

        self.x0_1 = np.array([1.2, 1.2]).T
        self.pas_1 = 10 ** -2
        self.grad = Gradient(self.x0_1, self.pas_1, 10 ** -4, 10 ** 5, self.fct_der[int(Calculator.equation) - 1], self.fct_h[int(Calculator.equation) - 1])
        self.x_fixe, xlist, i = self.grad.gradientPasFixe()
        self.x_opti, xlist2, i2 = self.grad.gradientPasOptimal()

    def setupUI(self, Calc):
        Calc.setGeometry(500, 100, 1200, 600)
        Calc.setFixedSize(1200, 600)
        Calc.setWindowTitle(self.lang["app-title"] + " \ " + self.lang["start"] + " \ " + self.lang["calc"])

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(Qt.black)
        shadow.setBlurRadius(25)
        shadow.setOffset(1, 1)


        self.CWidgets = QWidget(Calc)
        self.ChoiceWidgets = QWidget(self.CWidgets)

        self.layout = QVBoxLayout(self.ChoiceWidgets)

        self.method_1 = QRadioButton("Gradient Pas Fixe")
        self.method_1.setChecked(True)

        self.method_2 = QRadioButton("Gradient Pas Optimal")

        #self.method_3 = QRadioButton("Gradient 3")

        self.layout.addWidget(self.method_1)
        self.layout.addWidget(self.method_2)
        #self.layout.addWidget(self.method_3)

        self.method_1.toggled.connect(lambda: self.btn_state(self.method_1))
        self.method_2.toggled.connect(lambda: self.btn_state(self.method_2))
        #self.method_3.toggled.connect(lambda: self.btn_state(self.method_3))

        self.method_1.setGraphicsEffect(shadow)
        self.method_2.setGraphicsEffect(shadow)
        #self.method_3.setGraphicsEffect(shadow)

        self.layout.setSpacing(50)

        Calc.setLayout(self.layout)

        # extremum
        self.extr = QLabel(self.CWidgets)
        self.extr.setText(f"x = {self.x_fixe}")
        self.extr.resize(450, 50)
        self.extr.setProperty("type", 1)

        self.entry_widgets()
        self.result_widgets()
        self.move_widgets()

        Calc.setCentralWidget(self.CWidgets)

    def btn_state(self, btn):


        if btn.text() == "Gradient Pas Fixe":
            self.extr.setText(f"x = {self.x_fixe}")

            if btn.isChecked() == True:
                self.method_2.setChecked(False)


                #self.method_3.isChecked(False)

        if btn.text() == "Gradient Pas Optimal":
            self.extr.setText(f"x = {self.x_opti}")

            if btn.isChecked() == True:
                self.method_1.setChecked(False)

                #self.method_3.isChecked(False)


        '''if btn.text() == "method_3":
            if btn.isChecked() == True:
                self.method_1.isChecked(False)
                self.method_2.isChecked(False)'''

    def entry_widgets(self):

        self.language = QPushButton(self.CWidgets)
        self.language.setText(self.lang["language"])

        self.back_bt = QPushButton(self.CWidgets)
        self.back_bt.setText(self.lang["back"])
        self.back_bt.resize(130, 55)
        self.back_bt.setProperty("type", 1)


        # function graph representation
        fct = Functions(None, None)
        # graphical part

        print(self.functions[int(Calculator.equation) - 1])
        self.canvas = Canvas(self.CWidgets)
        self.canvas.resize(450, 275)
        print(int(Calculator.equation))
        self.canvas.surface(Calculator.intervalx[0], Calculator.intervalx[1], 0.1, fct, self.functions[int(Calculator.equation) - 1],
                            Calculator.intervaly[0], Calculator.intervaly[1])

        self.fct_comment = QLabel(self.CWidgets)
        self.fct_comment.setText("Lorem ipsum dolor sit amet. Et ducimus omnis nam dolores \n"
                                 "quaerat quo perferendis soluta. \n"
                                 "Ad vero culpa vel placeat unde hic quia veniam et nihil ipsa. \n"
                                 "Et harum harum aut voluptatibus dolorum et laborum aperiam \n"
                                 "non velit repellendus.")
        self.fct_comment.resize(450, 150)
        self.fct_comment.setProperty("type", 2)



    def result_widgets(self):

        pass

    def move_widgets(self):


        self.language.move(int(self.width * 0.85), int(self.height * 0.01))

        self.back_bt.move(int(self.width * 0.78), int(self.height * 0.97))

        self.canvas.move(int(self.width * 0.45), int(self.height * 0.15))

        self.fct_comment.move(int(self.width * 0.45), int(self.height * 0.7))

        self.ChoiceWidgets.move(int(self.width * 0.15), int(self.height * 0.4))
        self.extr.move(int(self.width * 0.05), int(self.height * 0.7))

    def calculate(self):

        pass
