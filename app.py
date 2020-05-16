import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import dataClean
import match

profiles = []

class Promotions(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(int)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(102, 185, 51))
        self.setPalette(p)
        
        self.setWindowTitle('Promotions')
        self.resize(350, 580)

        layout = QtWidgets.QGridLayout()

        heading = QtGui.QFont()
        heading.setBold(True)
        heading.setPointSize(20)
        detailsHead = QtWidgets.QLabel("Promotions")
        detailsHead.setAlignment(QtCore.Qt.AlignCenter)
        detailsHead.setFont(heading)

        layout.addWidget(detailsHead)

        events = [('Sephora BUY 2 GET 25%', 2),('Starbucks FREE DRINK with \nevery purchase', 2),
        ('Swensons 3 mains for price of 2', 3), ('Mcdonalds 25% off family meal', 4)]
        
        font = QtGui.QFont()
        font.setPointSize(11)
        fontSmall = QtGui.QFont()
        fontSmall.setPointSize(8)
        for name, no in events:
            frame = QtWidgets.QFrame()
            frame.setFrameShape(0x3)
            frame.setFrameShadow(0x30)
            frame.setMaximumSize(350, 180)
            frame.setAutoFillBackground(True)
            p = frame.palette()
            p.setColor(frame.backgroundRole(), QtCore.Qt.white)
            frame.setPalette(p)
            frameLayout = QtWidgets.QGridLayout()
            self.labelA = QtWidgets.QLabel(name)
            self.labelA.setAlignment(QtCore.Qt.AlignCenter)
            self.labelA.setFont(font)
            self.labelB = QtWidgets.QLabel('No of pax: ' + str(no))
            self.labelB.setFont(fontSmall)
            self.button = QtWidgets.QPushButton('Interested')
            self.button.clicked.connect((lambda i:lambda: self.switch_window.emit(i))(no))
            frameLayout.addWidget(self.labelA)
            frameLayout.addWidget(self.labelB)
            frameLayout.addWidget(self.button)
            frame.setLayout(frameLayout)
            layout.addWidget(frame)

        self.setLayout(layout)


class WindowTwo(QtWidgets.QWidget):

    def __init__(self, no):
        QtWidgets.QWidget.__init__(self)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(102, 185, 51))
        self.setPalette(p)

        matches = match.find_match(profiles, no-1)
        
        self.setWindowTitle('We found you a match!')
        self.resize(350, 580)
 
        layout = QtWidgets.QGridLayout()

        heading = QtGui.QFont()
        heading.setBold(True)
        heading.setPointSize(20)
        detailsHead = QtWidgets.QLabel("We found you a match!")
        detailsHead.setAlignment(QtCore.Qt.AlignCenter)
        detailsHead.setFont(heading)

        layout.addWidget(detailsHead)

        for i in range(1, no):
            cur = matches[i]
            frame = QtWidgets.QFrame()
            frame.setFrameShape(0x3)
            frame.setFrameShadow(0x30)
            frame.setMaximumSize(350, 150)
            frame.setAutoFillBackground(True)
            p = frame.palette()
            p.setColor(frame.backgroundRole(), QtCore.Qt.white)
            frame.setPalette(p)
            frameLayout = QtWidgets.QGridLayout()

            bold = QtGui.QFont()
            bold.setBold(True)
            label = QtWidgets.QLabel('Matched With: \n')
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFont(bold)

            matchLabel = QtWidgets.QLabel('Name: ' + str(cur[0]) + '\nAge: ' + str(cur[1]) + '\nLanguage: ' + str(cur[2]))
            matchLabel.setAlignment(QtCore.Qt.AlignCenter)
            
            frameLayout.addWidget(label)
            frameLayout.addWidget(matchLabel)
            frame.setLayout(frameLayout)
            layout.addWidget(frame)

        frame = QtWidgets.QFrame()
        frame.setMaximumSize(350, 70)
        frameLayout = QtWidgets.QHBoxLayout()
        frame.setLayout(frameLayout)
        buttonReject = QtWidgets.QPushButton('Reject')
        buttonReject.clicked.connect(self.close)
        buttonChat = QtWidgets.QPushButton('Open Chat')
        buttonChat.clicked.connect(self.close)
        frameLayout.addWidget(buttonReject)
        frameLayout.addWidget(buttonChat)
        layout.addWidget(frame)
        self.setLayout(layout)


class Profile(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(102, 185, 51))
        self.setPalette(p)
        
        self.setWindowTitle('Profile')
        self.resize(350, 580)

        layout = QtWidgets.QGridLayout()

        heading = QtGui.QFont()
        heading.setBold(True)
        heading.setPointSize(20)
        detailsHead = QtWidgets.QLabel("Profile")
        detailsHead.setAlignment(QtCore.Qt.AlignCenter)
        detailsHead.setFont(heading)

        layout.addWidget(detailsHead)

        frame = QtWidgets.QFrame()
        frame.setFrameShape(0x3)
        frame.setFrameShadow(0x30)
        frame.setAutoFillBackground(True)
        p = frame.palette()
        p.setColor(frame.backgroundRole(), QtCore.Qt.white)
        frame.setPalette(p)
        frameLayout = QtWidgets.QGridLayout()

        global profiles
        profiles = dataClean.get_profiles()
        user = profiles[0]
        userDetails = 'Name: ' + str(user[0]) + '\nAge: ' + str(user[1]) + '\nLanguage: ' + str(user[2]) + '\nTotal Spending: ' + str(user[3])
        userFinDetails = ''
        level = ['Low', 'Medium', 'High']
        for key, value in user[4].items():
            userFinDetails += key.capitalize() + ': ' + level[value-1] + '\n'

        
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

    def show_window_two(self, no):
        self.window_two = WindowTwo(no)
        self.promo.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_profile()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
