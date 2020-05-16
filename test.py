import sys
from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Promotions')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.button = QtWidgets.QPushButton('Interested')
        self.button.clicked.connect(self.switch)
        layout.addWidget(self.button)

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


class profile(QtWidgets.QWidget):

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
        self.profile = profile()
        self.profile.switch_window.connect(self.show_main)
        self.profile.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
        self.profile.close()
        self.window.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.window.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_profile()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()