#!/usr/bin/env python3

import sys
from enum import Enum
from random import shuffle
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication,
                             QMainWindow, QAction)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import tarotdeck as t


class Deck(QLabel):
    clicked = pyqtSignal('QString')

    class Composition(Enum):
        MINORS = 0
        MAJORS = 1
        BOTH = 2

    def __init__(self):
        super(QLabel, self).__init__()
        back = QPixmap('images/back/Back.jpg')
        self.setPixmap(back)
        self.set_composition(self.Composition.BOTH)

    def init_deck(self):
        if self._composition == self.Composition.MINORS:
            self._deck = t.TarotDeck()[:56]
        elif self._composition == self.Composition.MAJORS:
            self._deck = t.TarotDeck()[57:]
        elif self._composition == self.Composition.BOTH:
            self._deck = t.TarotDeck()

    def shuffle(self):
        shuffle(self._deck)

    def set_composition(self, composition):
        self._composition = composition
        self.init_deck()

    def mousePressEvent(self, QMouseEvent):
        try:
            card = self._deck.pop()
        except IndexError:
            self.init_deck()
            card = self._deck.pop()
        self.clicked.emit(card.image)


class Card(QLabel):
    def __init__(self):
        super(QLabel, self).__init__()
        self.setFixedSize(354, 658)

    @pyqtSlot('QString')
    def get_card(self, card):
        self.show_card(card)

    def show_card(self, card):
        picture = QPixmap(card)
        self.setPixmap(picture)

    def make_connection(self, deck):
        deck.clicked.connect(self.get_card)


class Table(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.deck_stack = Deck()
        self.drawn_card = Card()
        hboxlayout = QHBoxLayout()
        hboxlayout.addWidget(self.deck_stack)
        hboxlayout.addWidget(self.drawn_card)
        self.drawn_card.make_connection(self.deck_stack)
        self.setLayout(hboxlayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setStyleSheet("background-color: black;")

        self.table = Table()
        self.setCentralWidget(self.table)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('QTarot')

        shuffle_action = QAction('Shuffle', self)
        shuffle_action.triggered.connect(self.table.deck_stack.shuffle)
        majors_action = QAction('Majors', self)
        majors_action.triggered.connect(self.majors)
        minors_action = QAction('Minors', self)
        minors_action.triggered.connect(self.minors)
        full_action = QAction('Full Deck', self)
        full_action.triggered.connect(self.full)
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(shuffle_action)
        self.toolbar.addAction(majors_action)
        self.toolbar.addAction(minors_action)
        self.toolbar.addAction(full_action)
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("background-color: lightgray;")
        self.show()

    def majors(self):
        self.table.deck_stack.set_composition(self.table.deck_stack.Composition.MAJORS)
        self.table.drawn_card.show_card(None)

    def minors(self):
        self.table.deck_stack.set_composition(self.table.deck_stack.Composition.MINORS)
        self.table.drawn_card.show_card(None)

    def full(self):
        self.table.deck_stack.set_composition(self.table.deck_stack.Composition.BOTH)
        self.table.drawn_card.show_card(None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
