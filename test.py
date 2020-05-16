import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import dataClean
import match

profiles = []

class Promotions(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Promotions')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit() # Redundant function
#        layout.addWidget(self.line_edit)

        events = ['Sephora BUY 2 GET 25%','Starbucks FREE DRINK with every purchase',
        'Event 3', 'Event 4', 'Event 101']
        
        font = QtGui.QFont()
        font.setPointSize(11)
        for x in events:
            self.label = QtWidgets.QLabel(x)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setFont(font)
            self.button = QtWidgets.QPushButton('Interested')
            self.button.clicked.connect(self.switch)
            layout.addWidget(self.label)
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


class Profile(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Profile')
        self.resize(350, 560)

        layout = QtWidgets.QGridLayout()

        frame = QtWidgets.QFrame()
        frame.setFrameShape(0x3)
        frame.setFrameShadow(0x30)
        frameLayout = QtWidgets.QGridLayout()

        profiles = dataClean.get_profiles()
        user = profiles[0]
        userDetails = 'Name: ' + str(user[0]) + '\nAge: ' + str(user[1]) + '\nLanguage: ' + str(user[2]) + '\nTotal Spending: ' + str(user[3])
        userFinDetails = ''
        for key, value in user[4].items():
            userFinDetails += key.capitalize() + ': ' + str(value) + '\n'

        
        detailsA = QtWidgets.QLabel(userDetails)
        detailsA.setAlignment(QtCore.Qt.AlignCenter)

        bold = QtGui.QFont()
        bold.setBold(True)
        detailsB = QtWidgets.QLabel('\nFinancial Profile')
        detailsB.setAlignment(QtCore.Qt.AlignCenter)
        detailsB.setFont(bold)

        detailsC = QtWidgets.QLabel(userFinDetails)
        detailsC.setAlignment(QtCore.Qt.AlignCenter)
        
        self.button = QtWidgets.QPushButton('See Promo')
        self.button.clicked.connect(self.profile)

        layout.addWidget(Label("profilepic.jpg"))
        layout.addWidget(frame)
        frameLayout.addWidget(detailsA)
        frameLayout.addWidget(detailsB)
        frameLayout.addWidget(detailsC)
        layout.addWidget(self.button)

        frame.setLayout(frameLayout)
        self.setLayout(layout)

    def profile(self):
        self.switch_window.emit()

class Label(QtWidgets.QLabel):
    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(200, 200)
        self.setMinimumSize(200, 200)
        self.radius = 100 

        self.target = QtGui.QPixmap(self.size())  
        self.target.fill(QtCore.Qt.transparent)   

        p = QtGui.QPixmap(args[0]).scaled(200, 200, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

        painter = QtGui.QPainter(self.target)
        if self.Antialiasing:
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

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
