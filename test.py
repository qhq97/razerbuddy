import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class Promotions(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Promotions')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit() # Redundant function
#        layout.addWidget(self.line_edit)

        self.label = QtWidgets.QLabel('Event 1')
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button = QtWidgets.QPushButton('Interested')

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.switch)

        self.setLayout(layout)

    def switch(self):
        self.switch_window.emit(self.line_edit.text())


class WindowTwo(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('We found you a match!')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton('Close')
        self.button.clicked.connect(self.close)

        layout.addWidget(self.button)

        self.setLayout(layout)


class Profile(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Profile')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        details = QtWidgets.QLabel('Name: \nAge: \n...')
        details.setAlignment(QtCore.Qt.AlignCenter)
        
        self.button = QtWidgets.QPushButton('See Promo')
        self.button.clicked.connect(self.profile)

        layout.addWidget(details)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def profile(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_profile(self):
        self.profile = Profile()
        self.profile.switch_window.connect(self.show_promo)
        self.profile.show()

    def show_promo(self):
        self.promo = Promotions()
        self.promo.switch_window.connect(self.show_window_two)
        self.profile.close()
        self.promo.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.promo.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_profile()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()