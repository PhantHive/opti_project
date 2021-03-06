from decimal import Decimal

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QRadioButton, \
    QGraphicsDropShadowEffect
from src.canvas.Canvas import Canvas
from src.maths.functions import Functions
from src.maths.graph import Graph


class SpeFct(object):
    intervalx = [None, None]
    intervaly = [None, None]

    def __init__(self):
        '''
        This window focus on one function only.
        This function was given by our school teacher as the final exam
        of Optimization 2 course.

        We study both 3D and Contour graphics.
        '''

        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = int(self.screen.width() * 0.70)
        self.height = int(self.screen.height() * 0.50)

        self.lang = None
        self.back_bt = None

        # 3D
        self.min_3d = -30
        self.max_3d = 30
        # Outline
        self.target_area = [[-5, 5], [-2.805, 3.131], [3.584, -1.848], [3.385, 0.074], [-3.073, -0.081], [0.087, 2.884],
                            [3, 2], [-3.779, -3.283], [-0.128, -1.954], [-0.271, -0.923]]
        self.min_o = -5
        self.max_o = 5
        self.contour_i = 1

        # 3D graph
        self.graph_i = 1
        self.g_3dinterval = ["[-30 30]", "[-5 5]"]

        self.onlyInt = QIntValidator()

    def setupUI(self, SpeFct):
        SpeFct.setGeometry(500, 100, 1200, 750)
        SpeFct.setFixedSize(1200, 750)
        SpeFct.setWindowTitle(self.lang["app-title"] + " \ " + self.lang["start"] + " \ " + self.lang["spe-function"])

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(Qt.black)
        shadow.setBlurRadius(25)
        shadow.setOffset(1, 1)

        self.CWidgets = QWidget(SpeFct)
        self.ChoiceWidgets = QWidget(self.CWidgets)

        self.entry_widgets()
        self.move_widgets()

        SpeFct.setCentralWidget(self.CWidgets)

    def entry_widgets(self):

        self.language = QPushButton(self.CWidgets)
        self.language.setText(self.lang["language"])

        self.back_bt = QPushButton(self.CWidgets)
        self.back_bt.setText(self.lang["back"])
        self.back_bt.resize(130, 55)
        self.back_bt.setProperty("type", 1)

        # function graph representation
        self.fct = Functions(None, None)

        # graphical part
        # ===
        # 3D
        self.canvas_3d = Canvas(self.CWidgets)
        self.canvas_3d.resize(400, 250)
        self.canvas_3d.surface(self.min_3d, self.max_3d, 0.1, self.fct, "s")
        # ===
        # Contour
        self.canvas_outline = Canvas(self.CWidgets)
        self.canvas_outline.resize(400, 250)
        self.canvas_outline.contour(self.min_o, self.max_o, 0.1, self.fct, "s", [i ** 3 for i in range(12)])
        # ===

        # Contour graph change

        self.contour_ch = QPushButton(self.CWidgets)
        self.contour_ch.setText(str(self.target_area[self.contour_i - 1]))
        self.contour_ch.resize(130, 55)
        self.contour_ch.setProperty("type", 2)

        # 3D Graph change graph

        self.graph_change = QPushButton(self.CWidgets)
        self.graph_change.setText(self.g_3dinterval[self.graph_i - 1])
        self.graph_change.resize(130, 55)
        self.graph_change.setProperty("type", 2)

        self.fct_comment = QLabel(self.CWidgets)
        self.fct_comment.setText("Pour l'??tude de cette fonction nous allons commencer par repr??senter en 3D "
                                "\nla fonction ?? ??tudier (voir sur le cot??) ."
                                "\nOn peut remarquer et supposer qu'?? l'infini la fonction tend elle aussi vers l'infini ."
                                "\nOn remarque ??galement que nous devons trouver au moins "
                                "\nun point critique minimal ."
                                "\n\n\nNous allons maintenant d??finir le gradient et la hessienne d'une fonction." 
                                "\nLe gradient d'une fonction se repr??sente sous la forme d'un vecteur "
                                "\ndont les composant sont les d??riv??s par rapport ?? la composante de l'indice." 
                                "\nLa hessienne est quand ?? elle un matrice carr?? dont les composantes sont "
                                "\nles d??riv??s du gradient par rapport ?? la composante de l'indice"
                                "\n\nDans le compl??ment (.pdf), nous avons fait tous les calculs analytiques "
                                "\net nous avons remarqu?? que la d??termination des points critiques "
                                "\npar un syst??me d'??quations ??tait impossible."
                                "\n\n\nMaintenant nous allons nous concentrer sur la repr??sentation graphique "
                                "\nde la fonction passant d'un intervalle [-30,30] ?? un intervalle [-5,5]."
                                "\nOn va pouvoir rep??rer neuf points critiques qui nous semblent coh??rents "
                                "\net on va estimer leurs valeurs gr??ce ?? la m??thode du gradient de Newton "
                                "\nqui est la plus pr??cise de toutes les m??thodes. "
                                "\nSi nous n'arrivons pas ?? d??terminer leurs valeurs, on va utiliser "
                                "\nla m??thode du gradient pr??conditionn?? ?? pas optimal." 
                                "\n\nGr??ce aux diff??rentes m??thodes cit??es auparavant, on a pu d??terminer "
                                "\nles diff??rents points critiques qui sont relativement proche de nos estimations. "
                                "\nLa nature des points critiques (Max/Min/Point Scelle) se d??termine "
                                "\ngr??ce aux contours qui sont affich??s sous la courbe. "
                                "\nSi nous distinguons une ellipse, c'est une max/min "
                                "\net si nous distinguons une hyperbole, c'est un point scelle. "
                                "\nPour conclure sur cette partie, nous pouvons calculer le minimum global qui est x*(3,2).")

        self.fct_comment.resize(615, 750)
        self.fct_comment.setProperty("type", 3)

        # connect btn
        self.graph_change.clicked.connect(self.change_3d_graph)
        self.contour_ch.clicked.connect(self.change_contour)

    def change_contour(self):

        if self.contour_i == len(self.target_area):
            self.contour_i = 1
            self.min_o = self.target_area[self.contour_i - 1][0]
            self.max_o = self.target_area[self.contour_i - 1][1]

            if self.contour_i in [2, 3, 4, 7]:
                lst = [i for i in range(12)]
            else:
                lst = [i ** 3 for i in range(12)]

            self.canvas_outline.contour(self.min_o, self.max_o, 0.1, self.fct, "s", lst)
        else:
            self.contour_i += 1
            self.min_o = self.target_area[self.contour_i - 1][0]
            self.max_o = self.target_area[self.contour_i - 1][1]

            if self.contour_i in [2, 3, 4, 7]:
                lst = [i for i in range(12)]
            else:
                lst = [i ** 3 for i in range(12)]

            self.canvas_outline.contour(self.min_o, self.max_o, 0.1, self.fct, "s", lst)

        self.canvas_outline.draw()
        self.contour_ch.setText(str(self.target_area[self.contour_i - 1]))

    def change_3d_graph(self):

        if self.graph_i == 1:
            self.graph_i = 2
            self.min_3d = -5
            self.max_3d = 5
            self.canvas_3d.surface(self.min_3d, self.max_3d, 0.1, self.fct, "s")
        else:
            self.graph_i = 1
            self.min_3d = -30
            self.max_3d = 30
            self.canvas_3d.surface(self.min_3d, self.max_3d, 0.1, self.fct, "s")

        self.canvas_3d.draw()
        self.graph_change.setText(self.g_3dinterval[self.graph_i - 1])

    def move_widgets(self):

        self.language.move(int(self.width * 0.87), int(self.height * 0.01))
        self.back_bt.move(int(self.width * 0.78), 675)

        # graphical widget
        self.canvas_3d.move(int(self.width * 0.55), int(self.height * 0.05))
        self.graph_change.move(int(self.width * 0.65), int(self.height * 0.55))

        self.canvas_outline.move(int(self.width * 0.55), int(self.height * 0.7))
        self.contour_ch.move(int(self.width * 0.65), int(self.height * 1.2))
        # ===

        self.fct_comment.move(int(self.width * 0.05), int(self.height * 0))
