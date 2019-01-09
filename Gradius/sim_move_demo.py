import sys
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDesktopWidget
from PyQt5 import QtTest
import multiprocessing as mp
from key_notifier import KeyNotifier
from worker import Worker
import random

lock = threading.Lock()


class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()
        # postavljanje slika u png formatu
        self.pix1 = QPixmap('flyingsaucer.png')
        self.pix2 = QPixmap('spaceship.png')
        self.pix3 = QPixmap('rocket.png')
        self.pix4 = QPixmap('rock1.png')
        self.pix5 = QPixmap('rock2.png')
        self.pix6 = QPixmap('rock3.png')
        self.pix7 = QPixmap('rock4.png')
        self.pix8 = QPixmap('rocketa.png')
        self.pix9 = QPixmap('alienmin.png')
        self.pix10 = QPixmap('spaceshipmin.png')
        self.pix11 = QPixmap('levelsymbol.png')
        self.pix12 = QPixmap('rotrock1.png')
        self.pix13 = QPixmap('rotrock2.png')
        self.pix14 = QPixmap('rotrock3.png')
        self.pix15 = QPixmap('rotrock4.png')

        # Objekti za manipulaciju u okviru GUI-a

        self.spaceship2_label = QLabel(self)
        self.spaceship1_label = QLabel(self)
        self.alien1_label = QLabel(self)
        self.alien2_label = QLabel(self)
        self.alien3_label = QLabel(self)
        self.alien4_label = QLabel(self)
        self.alien5_label = QLabel(self)
        self.alien6_label = QLabel(self)
        self.alien7_label = QLabel(self)
        self.rocket1_label = QLabel(self)
        self.rock1_label = QLabel(self)
        self.rock2_label = QLabel(self)
        self.rock3_label = QLabel(self)
        self.rock4_label = QLabel(self)
        self.rocket2_label = QLabel(self)
        self.rocket3_label = QLabel(self)
        self.alien_missile1_label = QLabel(self)
        self.alien_missile2_label = QLabel(self)
        self.alien_missile3_label = QLabel(self)
        self.alien_missile4_label = QLabel(self)
        self.alien_missile5_label = QLabel(self)
        self.alien_missile6_label = QLabel(self)
        self.alien_missile7_label = QLabel(self)
        self.rock1_rot_label = QLabel(self)
        self.rock2_rot_label = QLabel(self)
        self.rock3_rot_label = QLabel(self)
        self.rock4_rot_label = QLabel(self)
        self.background1_label = QLabel(self)
        self.name_label = QLabel(self)

        self.alien_min_label = QLabel(self)
        self.spaceship_min_label = QLabel(self)
        self.levelsymbol_min_label = QLabel(self)

        self.score_label = QLabel(self)
        self.lives_label = QLabel(self)
        self.level_label = QLabel(self)

        self.spaceship_min_label.setStyleSheet("background-color:white;")
        self.alien_min_label.setStyleSheet("background-color:white;")
        self.levelsymbol_min_label.setStyleSheet("background-color:white;")

        self.score_label.setStyleSheet("background-color:white;")
        self.lives_label.setStyleSheet("background-color:white;")
        self.level_label.setStyleSheet("background-color:white;")
        self.background1_label.setStyleSheet("background-color:white;")
        self.name_label.setStyleSheet("background-color:white;")
        # maksimalna veliina prozora i inicijalizovanje UI-a
        self.setWindowState(Qt.WindowMaximized)

        self.__init_ui__()

        # pomocna promanljiva
        self.startpos = 0

        # instance klasa
        self.key_notifier = KeyNotifier()
        self.work = Worker()

        # mapiranje signala na odgovarajuce metode
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.work.newParams.connect(self.fire)
        self.work.newParams2.connect(self.fire2)
        self.work.newParams3.connect(self.fire3)

        # pokretanje osnovnih niti
        self.work.start()
        self.key_notifier.start()

        # pokretanje procesa koji upravlja kretanjem vanzemaljaca i reljefa
        self.p1 = mp.Process(target=self.send(), args=())
        self.p1.start()

    # metoda ze generisanje korisnickog interfejsa
    def __init_ui__(self):

        self.shape = QDesktopWidget().screenGeometry()
        print(self.shape.width())
        print(self.shape.height())

        self.lives = 5
        self.level = 1
        self.score = 0

        self.spaceship2_label.setPixmap(self.pix2)
        self.spaceship2_label.setGeometry(0, 260, 196, 74)

        self.spaceship1_label.setPixmap(self.pix2)
        self.spaceship1_label.setGeometry(0, 160, 196, 74)

        self.alien1_label.setPixmap(self.pix1)
        self.alien1_label.setGeometry(self.shape.width() * 2, 340, 178, 77)

        self.alien2_label.setPixmap(self.pix1)
        self.alien2_label.setGeometry(self.shape.width() * 2, 440, 178, 77)

        self.alien3_label.setPixmap(self.pix1)
        self.alien3_label.setGeometry(self.shape.width() * 2, 540, 178, 77)

        self.alien4_label.setPixmap(self.pix1)
        self.alien4_label.setGeometry(self.shape.width() * 2, 240, 178, 77)

        self.alien5_label.setPixmap(self.pix1)
        self.alien5_label.setGeometry(self.shape.width() * 2, 480, 178, 77)

        self.alien6_label.setPixmap(self.pix1)
        self.alien6_label.setGeometry(self.shape.width() * 2, 300, 178, 77)

        self.alien7_label.setPixmap(self.pix1)
        self.alien7_label.setGeometry(self.shape.width() * 2, 500, 178, 77)

        self.rocket1_label.setPixmap(self.pix3)
        self.rocket1_label.setGeometry(-120, 160, 178, 77)

        self.rock1_label.setPixmap(self.pix4)
        self.rock1_label.setGeometry(1300, self.shape.height() - 200, 298, 213)

        self.rock2_label.setPixmap(self.pix5)
        self.rock2_label.setGeometry(1100, self.shape.height() - 200, 200, 175)

        self.rock3_label.setPixmap(self.pix6)
        self.rock3_label.setGeometry(600, self.shape.height() - 200, 502, 226)

        self.rock4_label.setPixmap(self.pix7)
        self.rock4_label.setGeometry(10, self.shape.height() - 210, 427, 288)

        self.rock1_rot_label.setPixmap(self.pix12)
        self.rock1_rot_label.setGeometry(1300, -80, 298, 213)

        self.rock2_rot_label.setPixmap(self.pix13)
        self.rock2_rot_label.setGeometry(1100, -40, 200, 175)

        self.rock3_rot_label.setPixmap(self.pix14)
        self.rock3_rot_label.setGeometry(600, -80, 502, 226)

        self.rock4_rot_label.setPixmap(self.pix15)
        self.rock4_rot_label.setGeometry(10, -140, 427, 288)

        self.rocket2_label.setPixmap(self.pix3)
        self.rocket2_label.setGeometry(-120, 11, 178, 77)

        self.rocket3_label.setPixmap(self.pix3)
        self.rocket3_label.setGeometry(-120, 11, 178, 77)

        self.alien_missile1_label.setPixmap(self.pix8)
        self.alien_missile1_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile2_label.setPixmap(self.pix8)
        self.alien_missile2_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile3_label.setPixmap(self.pix8)
        self.alien_missile3_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile4_label.setPixmap(self.pix8)
        self.alien_missile4_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile5_label.setPixmap(self.pix8)
        self.alien_missile5_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile6_label.setPixmap(self.pix8)
        self.alien_missile6_label.setGeometry(-60, 10, 57, 55)

        self.alien_missile7_label.setPixmap(self.pix8)
        self.alien_missile7_label.setGeometry(-60, 10, 57, 55)

        self.alien_min_label.setPixmap(self.pix9)
        self.alien_min_label.setGeometry(60, 30, 66, 32)

        self.score_label.setText(str(self.score))
        self.score_label.setGeometry(90, 65, 25, 15)

        self.lives_label.setText(str(self.lives))
        self.lives_label.setGeometry(165, 65, 25, 15)

        self.spaceship_min_label.setPixmap(self.pix10)
        self.spaceship_min_label.setGeometry(140, 30, 76, 32)

        self.levelsymbol_min_label.setPixmap(self.pix11)
        self.levelsymbol_min_label.setGeometry(230, 30, 42, 32)

        self.level_label.setText(str(self.level))
        self.level_label.setGeometry(235, 65, 25, 15)

        self.background1_label.setText(" ")
        self.background1_label.setGeometry(60, 30, 220, 50)

        self.name_label.setText("                              Играч 1")
        self.name_label.setGeometry(60, 10, 220, 20)

        # preuzimanje koordinata labela
        self.spaceship2_rec = self.spaceship2_label.geometry()
        self.alien1_rec = self.alien1_label.geometry()
        self.alien2_rec = self.alien2_label.geometry()
        self.alien3_rec = self.alien3_label.geometry()
        self.alien4_rec = self.alien4_label.geometry()
        self.alien5_rec = self.alien5_label.geometry()
        self.alien6_rec = self.alien6_label.geometry()
        self.alien7_rec = self.alien7_label.geometry()
        self.spaceship1_rec = self.spaceship1_label.geometry()
        self.rocket1_rec = self.rocket1_label.geometry()
        self.rock1_rec = self.rock1_label.geometry()
        self.rock2_rec = self.rock2_label.geometry()
        self.rock3_rec = self.rock3_label.geometry()
        self.rock4_rec = self.rock4_label.geometry()
        self.rock1_rot_rec = self.rock1_rot_label.geometry()
        self.rock2_rot_rec = self.rock2_rot_label.geometry()
        self.rock3_rot_rec = self.rock3_rot_label.geometry()
        self.rock4_rot_rec = self.rock4_rot_label.geometry()
        self.rocket2_rec = self.rocket2_label.geometry()
        self.rocket3_rec = self.rocket3_label.geometry()
        self.alien_missile1_rec = self.alien_missile1_label.geometry()
        self.alien_missile2_rec = self.alien_missile2_label.geometry()
        self.alien_missile3_rec = self.alien_missile3_label.geometry()
        self.alien_missile4_rec = self.alien_missile4_label.geometry()
        self.alien_missile5_rec = self.alien_missile5_label.geometry()
        self.alien_missile6_rec = self.alien_missile4_label.geometry()
        self.alien_missile7_rec = self.alien_missile5_label.geometry()
        self.alienmin_missile_rec = self.alien_min_label.geometry()

        # pomoćne promeljive
        self.startposy = self.spaceship1_rec.y()
        self.startposx = self.spaceship1_rec.x()
        self.startposy2 = self.spaceship1_rec.y()
        self.startposx2 = self.spaceship1_rec.x()
        self.startposy3 = self.spaceship1_rec.y()
        self.startposx3 = self.spaceship1_rec.x()
        self.globalcounter1 = 0
        self.globalcounter2 = 0
        self.globalcounter3 = 0
        self.globalcounter21 = 0
        self.globalcounter22 = 0
        self.globalcounter23 = 0

        # naslov prozora
        self.setWindowTitle('GRADIUS')
        self.show()

    # Override metode za pritisak na dugme sa tastature
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.work.add_key(event.key())
            self.work.keyscount = 1
        else:
            self.key_notifier.add_key(event.key())

    # Override metode za puštanje pritiska sa tastatur
    def keyReleaseEvent(self, event):

        if event.key() == Qt.Key_Space:
            self.work.rem_key(event.key())
            self.work.keyscount = 0
            # self.work.thread.quit()
        else:
            self.key_notifier.rem_key(event.key())

    # крај свега
    def closeEvent(self, event):
        self.key_notifier.die()
        self.work.die()

    # Metoda za ispaljivanje jedne od raketa
    # Druge dve metode su skoro identične, potrebno objediniti sve u jednu metodu kasnije
    def fire3(self):
        print('RAKETA3')

        # provera da li je raketa pogodila nekog od svemiraca
        # ako jeste svemirac "sakriva"
        if abs(self.rocket3_label.x() - self.spaceship2_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.spaceship2_label.y()) < 40:
            if self.spaceship2_label.x() < self.shape.width():
                self.score += 1
                self.spaceship2_label.hide()
        if abs(self.rocket3_label.x() - self.alien1_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien1_label.y()) < 40:
            if self.alien1_label.x() < self.shape.width():
                self.score += 1
                self.alien1_label.hide()
        if abs(self.rocket3_label.x() - self.alien2_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien2_label.y()) < 40:
            if self.alien2_label.x() < self.shape.width():
                self.score += 1
                self.alien2_label.hide()
        if abs(self.rocket3_label.x() - self.alien3_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien3_label.y()) < 40:
            if self.alien3_label.x() < self.shape.width():
                self.score += 1
                self.alien3_label.hide()
        if abs(self.rocket3_label.x() - self.alien4_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien4_label.y()) < 40:
            if self.alien4_label.x() < self.shape.width():
                self.score += 1
                self.alien4_label.hide()
        if abs(self.rocket3_label.x() - self.alien5_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien5_label.y()) < 40:
            if self.alien5_label.x() < self.shape.width():
                self.score += 1
                self.alien5_label.hide()
        if abs(self.rocket3_label.x() - self.alien6_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien6_label.y()) < 40:
            if self.alien6_label.x() < self.shape.width():
                self.score += 1
                self.alien6_label.hide()
        if abs(self.rocket3_label.x() - self.alien7_label.x()) < 40 and abs(
                self.rocket3_label.y() - self.alien7_label.y()) < 40:
            if self.alien7_label.x() < self.shape.width():
                self.score += 1
                self.alien7_label.hide()

        # potrebno za prvo pozivanje metode - globalna promanljiva
        if self.globalcounter3 == 0:
            self.startposx3 = self.spaceship1_rec.x()
            self.startposy3 = self.spaceship1_rec.y()
        self.globalcounter3 = 1

        self.globalcounter23 += 1
        # provera da li je lokani brojac izbrojao do 165 - toliko je potrebno da se pređe ceo ekran
        # ako jeste, setuju se nove koordinate i resetuje se brojač
        if self.globalcounter23 > 165:
            self.startposy3 = self.spaceship1_rec.y()
            self.startposx3 = self.spaceship1_rec.x()
            self.rocket3_label.hide()
            self.globalcounter23 = 1
        else:
            # u običnim prolazima raketa se samo pomera za po 11 jedinica po x osi
            self.rocket3_label.show()
            self.rocket3_label.setGeometry(self.startposx3, self.startposy3, self.rocket3_rec.width(),
                                           self.rocket3_rec.height())
            self.startposx3 += 11

        self.score_label.setText(str(self.score))

    def fire2(self):
        print('RAKETA2')

        if abs(self.rocket2_label.x() - self.spaceship2_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.spaceship2_label.y()) < 40:
            if self.spaceship2_label.x() < self.shape.width():
                self.score += 1
                self.spaceship2_label.hide()
        if abs(self.rocket2_label.x() - self.alien1_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien1_label.y()) < 40:
            if self.alien1_label.x() < self.shape.width():
                self.score += 1
                self.alien1_label.hide()
        if abs(self.rocket2_label.x() - self.alien2_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien2_label.y()) < 40:
            if self.alien2_label.x() < self.shape.width():
                self.score += 1
                self.alien2_label.hide()
        if abs(self.rocket2_label.x() - self.alien3_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien3_label.y()) < 40:
            if self.alien3_label.x() < self.shape.width():
                self.score += 1
                self.alien3_label.hide()
        if abs(self.rocket2_label.x() - self.alien4_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien4_label.y()) < 40:
            if self.alien4_label.x() < self.shape.width():
                self.score += 1
                self.alien4_label.hide()
        if abs(self.rocket2_label.x() - self.alien5_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien5_label.y()) < 40:
            if self.alien5_label.x() < self.shape.width():
                self.score += 1
                self.alien5_label.hide()
        if abs(self.rocket2_label.x() - self.alien6_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien6_label.y()) < 40:
            if self.alien6_label.x() < self.shape.width():
                self.score += 1
                self.alien6_label.hide()
        if abs(self.rocket2_label.x() - self.alien7_label.x()) < 40 and abs(
                self.rocket2_label.y() - self.alien7_label.y()) < 40:
            if self.alien7_label.x() < self.shape.width():
                self.score += 1
                self.alien7_label.hide()

        if self.globalcounter2 == 0:
            self.startposx2 = self.spaceship1_rec.x()
            self.startposy2 = self.spaceship1_rec.y()
        self.globalcounter2 = 1

        self.globalcounter22 += 1
        if self.globalcounter22 > 165:
            self.startposy2 = self.spaceship1_rec.y()
            self.startposx2 = self.spaceship1_rec.x()
            self.rocket2_label.hide()
            self.globalcounter22 = 1
        else:
            self.rocket2_label.show()
            self.rocket2_label.setGeometry(self.startposx2, self.startposy2, self.rocket2_rec.width(),
                                           self.rocket2_rec.height())
            self.startposx2 += 11

        self.score_label.setText(str(self.score))

    def fire(self):
        print('RAKETA1')

        self.rocket1_rec = self.rocket1_label.geometry()

        if abs(self.rocket1_label.x() - self.spaceship2_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.spaceship2_label.y()) < 40:
            if self.spaceship2_label.x() < self.shape.width():
                self.score += 1
                self.spaceship2_label.hide()
        if abs(self.rocket1_label.x() - self.alien1_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien1_label.y()) < 40:
            if self.alien1_label.x() < self.shape.width():
                self.score += 1
                self.alien1_label.hide()
        if abs(self.rocket1_label.x() - self.alien2_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien2_label.y()) < 40:
            if self.alien2_label.x() < self.shape.width():
                self.score += 1
                self.alien2_label.hide()
        if abs(self.rocket1_label.x() - self.alien3_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien3_label.y()) < 40:
            if self.alien3_label.x() < self.shape.width():
                self.score += 1
                self.alien3_label.hide()
        if abs(self.rocket1_label.x() - self.alien4_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien4_label.y()) < 40:
            if self.alien4_label.x() < self.shape.width():
                self.score += 1
                self.alien4_label.hide()
        if abs(self.rocket1_label.x() - self.alien5_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien5_label.y()) < 40:
            if self.alien5_label.x() < self.shape.width():
                self.score += 1
                self.alien5_label.hide()
        if abs(self.rocket1_label.x() - self.alien6_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien6_label.y()) < 40:
            if self.alien6_label.x() < self.shape.width():
                self.score += 1
                self.alien6_label.hide()
        if abs(self.rocket1_label.x() - self.alien7_label.x()) < 40 and abs(
                self.rocket1_label.y() - self.alien7_label.y()) < 40:
            if self.alien7_label.x() < self.shape.width():
                self.score += 1
                self.alien7_label.hide()

        if self.globalcounter1 == 0:
            self.startposx = self.spaceship1_rec.x()
            self.startposy = self.spaceship1_rec.y()
        self.globalcounter1 = 1

        self.globalcounter21 += 1
        if self.globalcounter21 > 165:
            self.startposy = self.spaceship1_rec.y()
            self.startposx = self.spaceship1_rec.x()
            self.rocket1_label.hide()
            self.globalcounter21 = 1
        else:
            self.rocket1_label.show()
            self.rocket1_label.setGeometry(self.startposx, self.startposy, self.rocket1_rec.width(),
                                           self.rocket1_rec.height())
            self.startposx += 11

        self.score_label.setText(str(self.score))

    # metoda koja omogućava kretanje svemiraca i reljefa(stena)
    def send(self, ):
        print('Hello from proccess!')
        # početne pozicije elemenata
        alien1_startpos = self.alien1_rec.x()
        alien2_startpos = self.alien2_rec.x()
        alien3_startpos = self.alien3_rec.x()
        alien4_startpos = self.alien4_rec.x()
        alien5_startpos = self.alien5_rec.x()
        alien6_startpos = self.alien6_rec.x()
        alien7_startpos = self.alien7_rec.x()
        rock1_startpos = self.rock1_rec.x()
        rock2_startpos = self.rock2_rec.x()
        rock3_startpos = self.rock3_rec.x()
        rock4_startpos = self.rock4_rec.x()

        missile1_startpos = self.alien1_rec.x()
        missile2_startpos = self.alien2_rec.x()
        missile3_startpos = self.alien3_rec.x()
        missile4_startpos = self.alien4_rec.x()
        missile5_startpos = self.alien5_rec.x()
        missile6_startpos = self.alien6_rec.x()
        missile7_startpos = self.alien7_rec.x()

        alien1_new_y = self.alien1_rec.y()
        alien1_old_y = 0

        alien2_new_y = self.alien2_rec.y()
        alien2_old_y = 0

        alien3_new_y = self.alien3_rec.y()
        alien3_old_y = 0

        alien4_new_y = self.alien4_rec.y()
        alien4_old_y = 0

        alien5_new_y = self.alien5_rec.y()
        alien5_old_y = 0

        alien6_new_y = self.alien6_rec.y()
        alien6_old_y = 0

        alien7_new_y = self.alien7_rec.y()
        alien7_old_y = 0

        flag1 = 0
        flag2 = 0
        flag3 = 0
        flag4 = 0
        flag5 = 0
        flag6 = 0
        flag7 = 0

        motion_indicator1 = 0
        motion_indicator2 = 0
        motion_indicator3 = 0
        motion_indicator4 = 0
        motion_indicator5 = 0
        motion_indicator6 = 0
        motion_indicator7 = 0
        motion_missile_indicator1 = 1
        motion_missile_indicator2 = 1
        motion_missile_indicator3 = 1
        motion_missile_indicator4 = 1
        motion_missile_indicator5 = 1
        motion_missile_indicator6 = 1
        motion_missile_indicator7 = 1
        for x in range(0, 77715):
            # prelazak na sledeci nivo na svakih deset poena, bonus poeni na prelazak na sledeci nivo
            if self.score % 80 == 0 and self.score > 0:
                self.score += 1
                self.level += 1
                self.lives = 5
                self.level_label.setText(str(self.level))
                self.lives_label.setText(str(self.lives))
                self.score_label.setText(str(self.score))
                print('#######')
            # postavke brzina kretanja određenih elemenata u zavisnosti od nivoa
            alien1_startpos -= (self.level * 0.3 + 1.2)
            if (self.score - ((self.level - 1) * 80)) > 3 or motion_indicator2 == 1:
                alien2_startpos -= (self.level * 0.3 + 1.6)
            if (self.score - ((self.level - 1) * 80)) > 6 or motion_indicator3 == 1:
                alien3_startpos -= (self.level * 0.3 + 1.4)
            if (self.score - ((self.level - 1) * 80)) > 12 or motion_indicator4 == 1:
                alien4_startpos -= (self.level * 0.3 + 1.3)
            if (self.score - ((self.level - 1) * 80)) > 24 or motion_indicator5 == 1:
                alien5_startpos -= (self.level * 0.3 + 2)
            if (self.score - ((self.level - 1) * 80)) > 40 or motion_indicator6 == 1:
                alien6_startpos -= (self.level * 0.3 + 1.7)
            if (self.score - ((self.level - 1) * 80)) > 60 or motion_indicator7 == 1:
                alien7_startpos -= (self.level * 0.3 + 1.8)

            rock1_startpos -= (self.level * 0.3)
            rock2_startpos -= (self.level * 0.3)
            rock3_startpos -= (self.level * 0.3)
            rock4_startpos -= (self.level * 0.3)
            missile1_startpos -= (self.level * 0.3 + 6)
            missile2_startpos -= (self.level * 0.3 + 6)
            missile3_startpos -= (self.level * 0.3 + 6)
            missile4_startpos -= (self.level * 0.3 + 6)
            missile5_startpos -= (self.level * 0.3 + 6)
            missile6_startpos -= (self.level * 0.3 + 6)
            missile7_startpos -= (self.level * 0.3 + 6)

            # svemirac 1
            self.alien1_label.setGeometry(alien1_startpos, alien1_new_y, self.alien1_rec.width(),
                                          self.alien1_rec.height())
            if x % 514 == 0 and x > 311 and self.alien1_label.x() < self.shape.width():
                missile1_startpos = alien1_startpos
                flag1 = 1
            if flag1 == 1:
                if self.alien_missile1_label.x() >= -30 and self.alien1_label.x() >= self.shape.width():
                    self.alien_missile1_label.setGeometry(missile1_startpos, alien1_old_y,
                                                          self.alien_missile1_rec.width(),
                                                          self.alien_missile1_rec.height())
                else:
                    self.alien_missile1_label.setGeometry(missile1_startpos, alien1_new_y,
                                                          self.alien_missile1_rec.width(),
                                                          self.alien_missile1_rec.height())
            if self.alien1_label.isHidden():
                self.alien1_label.setGeometry(2000, alien1_new_y, self.alien1_rec.width(), self.alien1_rec.height())
                alien1_old_y = alien1_new_y
                alien1_new_y = random.randint(150, self.shape.height() - 300) 
                self.alien1_label.show()
                alien1_startpos = self.shape.width() * 2
            """
            Кретање свемираца - опис логике

            Помоћне променљиве:
            -alien_startpos
            -missile_startpos
            -alien_new_y
            -alien_old_y
            -flag
            -motion_indicator
            -motion_missile_indicator

            Кретање летећег тањира или његовог пројектила се дешава ако један од следећих услова испуњен
            -Постоји довољан број поена(индикатор колико је дати ниво одммакао)
            -почело је кретање ванземаљског пројектила
            -почело је кретање летећег тањира а да при том исти није на почетној позицији

            У свакој итерацији X координата се постаља на вредност alien_startpos која се на почетку итерације смањује
            у зависности од подешенњ брзине кретања. Индикатор кретања поставља се на 1. Проверава се да ли су испуњени
            услови за испаљивање пројектила и ако јесу X координата летећег тањира се поставља за почетну X координату
            ванземаљског пројектила. Постоји помоћна променљива која указује на то да је пројектил први пут испаљен.            
            У зависности од тога се поставља нова вредност XY координатa пројектила - први пут кад је пројектил замакао
            за ивицу а летећи тањир је на својој почетној позицији Y координата се сетује на нову вредност, односно на 
            нову Y координату летећег тањира. Ако је пројектил прошао ван ивице екрана, индикатор за кретање пројектила 
            биће 0 у супротном биће 1, ово је битно за наставак кретања пројектила кад је летећи тањир уништен након што
            је испалио пројектил а прешло се у нови ниво и изгубили су се услови за кретање брода у датом тренутку.

            Када ракета уништи свемирски брод он постане sakriven "hidden" што се проверава након сваког померања тањира 
            и ако се установи да је дошло до уништења индикатор кретања (motion_indicator2) се поставља на 0, координате
            летећег тањира се постављају на две дужине екрана за X i произвољна вредност "random" za Y координату Затим
            се летећи тањир поново открива ".show"

            """
            # svemirac 2
            if (self.score - ((self.level - 1) * 80)) > 3 or motion_missile_indicator2 == 1 or (
                    motion_indicator2 == 1 and self.alien2_label.x() != self.shape.width() * 2):
                self.alien2_label.setGeometry(alien2_startpos, alien2_new_y, self.alien2_rec.width(),
                                              self.alien2_rec.height())
                if self.alien2_label.x() < self.shape.width():
                    motion_indicator2 = 1
                if x % 781 == 0 and x > 400 and self.alien2_label.x() < self.shape.width():
                    missile2_startpos = alien2_startpos
                    flag2 = 1
                if flag2 == 1:
                    if self.alien_missile2_label.x() >= -30 and self.alien2_label.x() >= self.shape.width():
                        self.alien_missile2_label.setGeometry(missile2_startpos, alien2_old_y,
                                                              self.alien_missile2_rec.width(),
                                                              self.alien_missile2_rec.height())
                        motion_missile_indicator2 = 1

                    else:
                        self.alien_missile2_label.setGeometry(missile2_startpos, alien2_new_y,
                                                              self.alien_missile2_rec.width(),
                                                              self.alien_missile2_rec.height())
                    if self.alien_missile2_label.x() < -60:
                        motion_missile_indicator2 = 0
                    else:
                        motion_missile_indicator2 = 1

                if self.alien2_label.isHidden():
                    motion_indicator2 = 0
                    self.alien2_label.setGeometry(self.shape.width() * 2, alien2_new_y, self.alien2_rec.width(),
                                                  self.alien2_rec.height())
                    alien2_old_y = alien2_new_y
                    alien2_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien2_label.show()
                    alien2_startpos = self.shape.width() * 2

            # svemirac 3

            if (self.score - ((self.level - 1) * 80)) > 6 or motion_missile_indicator3 == 1 or (
                    motion_indicator3 == 1 and self.alien3_label.x() != self.shape.width() * 2):
                self.alien3_label.setGeometry(alien3_startpos, alien3_new_y, self.alien3_rec.width(),
                                              self.alien3_rec.height())
                if self.alien3_label.x() < self.shape.width():
                    motion_indicator3 = 1
                if x % 681 == 0 and x > 400 and self.alien3_label.x() < self.shape.width():
                    missile3_startpos = alien3_startpos
                    flag3 = 1
                if flag3 == 1:
                    if self.alien_missile3_label.x() >= -30 and self.alien3_label.x() >= self.shape.width():
                        self.alien_missile3_label.setGeometry(missile3_startpos, alien3_old_y,
                                                              self.alien_missile3_rec.width(),
                                                              self.alien_missile3_rec.height())
                        motion_missile_indicator3 = 1
                    else:
                        self.alien_missile3_label.setGeometry(missile3_startpos, alien3_new_y,
                                                              self.alien_missile3_rec.width(),
                                                              self.alien_missile3_rec.height())
                    if self.alien_missile3_label.x() < -60:
                        motion_missile_indicator3 = 0
                    else:
                        motion_missile_indicator3 = 1
                if self.alien3_label.isHidden():
                    motion_indicator3 = 0
                    self.alien3_label.setGeometry(self.shape.width() * 2, alien3_new_y, self.alien3_rec.width(),
                                                  self.alien3_rec.height())
                    alien3_old_y = alien3_new_y
                    alien3_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien3_label.show()
                    alien3_startpos = self.shape.width() * 2

            # svemirac 4
            if (self.score - ((self.level - 1) * 80)) > 12 or motion_missile_indicator4 == 1 or (
                    motion_indicator4 == 1 and self.alien4_label.x() != self.shape.width() * 2):
                self.alien4_label.setGeometry(alien4_startpos, alien4_new_y, self.alien4_rec.width(),
                                              self.alien4_rec.height())
                if self.alien4_label.x() < self.shape.width():
                    motion_indicator4 = 1
                if x % 581 == 0 and x > 400 and self.alien4_label.x() < self.shape.width():
                    missile4_startpos = alien4_startpos
                    flag4 = 1
                if flag4 == 1:
                    if self.alien_missile4_label.x() >= -30 and self.alien4_label.x() >= self.shape.width():
                        self.alien_missile4_label.setGeometry(missile4_startpos, alien4_old_y,
                                                              self.alien_missile4_rec.width(),
                                                              self.alien_missile4_rec.height())
                        motion_missile_indicator4 = 1

                    else:
                        self.alien_missile4_label.setGeometry(missile4_startpos, alien4_new_y,
                                                              self.alien_missile4_rec.width(),
                                                              self.alien_missile4_rec.height())
                    if self.alien_missile4_label.x() < -60:
                        motion_missile_indicator4 = 0
                    else:
                        motion_missile_indicator4 = 1

                if self.alien4_label.isHidden():
                    motion_indicator4 = 0
                    self.alien4_label.setGeometry(self.shape.width() * 2, alien4_new_y, self.alien4_rec.width(),
                                                  self.alien4_rec.height())
                    alien4_old_y = alien4_new_y
                    alien4_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien4_label.show()
                    alien4_startpos = self.shape.width() * 2

            # svemirac 5
            if (self.score - ((self.level - 1) * 80)) > 24 or motion_missile_indicator5 == 1 or (
                    motion_indicator5 == 1 and self.alien5_label.x() != self.shape.width() * 2):
                self.alien5_label.setGeometry(alien5_startpos, alien5_new_y, self.alien5_rec.width(),
                                              self.alien5_rec.height())
                if self.alien5_label.x() < self.shape.width():
                    motion_indicator5 = 1
                if x % 881 == 0 and x > 400 and self.alien5_label.x() < self.shape.width():
                    missile5_startpos = alien5_startpos
                    flag5 = 1
                if flag5 == 1:
                    if self.alien_missile5_label.x() >= -30 and self.alien5_label.x() >= self.shape.width():
                        self.alien_missile5_label.setGeometry(missile5_startpos, alien5_old_y,
                                                              self.alien_missile5_rec.width(),
                                                              self.alien_missile5_rec.height())
                        motion_missile_indicator5 = 1

                    else:
                        self.alien_missile5_label.setGeometry(missile5_startpos, alien5_new_y,
                                                              self.alien_missile5_rec.width(),
                                                              self.alien_missile5_rec.height())
                    if self.alien_missile5_label.x() < -60:
                        motion_missile_indicator5 = 0
                    else:
                        motion_missile_indicator5 = 1

                if self.alien5_label.isHidden():
                    motion_indicator5 = 0
                    self.alien5_label.setGeometry(self.shape.width() * 2, alien5_new_y, self.alien5_rec.width(),
                                                  self.alien5_rec.height())
                    alien5_old_y = alien5_new_y
                    alien5_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien5_label.show()
                    alien5_startpos = self.shape.width() * 2

            # svemirac 6
            if (self.score - ((self.level - 1) * 80)) > 40 or motion_missile_indicator6 == 1 or (
                    motion_indicator6 == 1 and self.alien6_label.x() != self.shape.width() * 2):
                self.alien6_label.setGeometry(alien6_startpos, alien6_new_y, self.alien6_rec.width(),
                                              self.alien6_rec.height())
                if self.alien6_label.x() < self.shape.width():
                    motion_indicator6 = 1
                if x % 611 == 0 and x > 400 and self.alien6_label.x() < self.shape.width():
                    missile6_startpos = alien6_startpos
                    flag6 = 1
                if flag6 == 1:
                    if self.alien_missile6_label.x() >= -30 and self.alien6_label.x() >= self.shape.width():
                        self.alien_missile6_label.setGeometry(missile6_startpos, alien6_old_y,
                                                              self.alien_missile6_rec.width(),
                                                              self.alien_missile6_rec.height())
                        motion_missile_indicator6 = 1

                    else:
                        self.alien_missile6_label.setGeometry(missile6_startpos, alien6_new_y,
                                                              self.alien_missile6_rec.width(),
                                                              self.alien_missile6_rec.height())
                    if self.alien_missile6_label.x() < -60:
                        motion_missile_indicator6 = 0
                    else:
                        motion_missile_indicator6 = 1

                if self.alien6_label.isHidden():
                    motion_indicator6 = 0
                    self.alien6_label.setGeometry(self.shape.width() * 2, alien6_new_y, self.alien6_rec.width(),
                                                  self.alien6_rec.height())
                    alien6_old_y = alien6_new_y
                    alien6_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien6_label.show()
                    alien6_startpos = self.shape.width() * 2

            # svemirac 7
            if (self.score - ((self.level - 1) * 80)) > 60 or motion_missile_indicator7 == 1 or (
                    motion_indicator7 == 1 and self.alien7_label.x() != self.shape.width() * 2):
                self.alien7_label.setGeometry(alien7_startpos, alien7_new_y, self.alien7_rec.width(),
                                              self.alien7_rec.height())
                if self.alien7_label.x() < self.shape.width():
                    motion_indicator7 = 1
                if x % 752 == 0 and x > 400 and self.alien7_label.x() < self.shape.width():
                    missile7_startpos = alien7_startpos
                    flag7 = 1
                if flag7 == 1:
                    if self.alien_missile7_label.x() >= -30 and self.alien7_label.x() >= self.shape.width():
                        self.alien_missile7_label.setGeometry(missile7_startpos, alien7_old_y,
                                                              self.alien_missile7_rec.width(),
                                                              self.alien_missile7_rec.height())
                        motion_missile_indicator7 = 1

                    else:
                        self.alien_missile7_label.setGeometry(missile7_startpos, alien7_new_y,
                                                              self.alien_missile7_rec.width(),
                                                              self.alien_missile7_rec.height())
                    if self.alien_missile7_label.x() < -60:
                        motion_missile_indicator7 = 0
                    else:
                        motion_missile_indicator7 = 1

                if self.alien7_label.isHidden():
                    motion_indicator7 = 0
                    self.alien7_label.setGeometry(self.shape.width() * 2, alien7_new_y, self.alien7_rec.width(),
                                                  self.alien7_rec.height())
                    alien7_old_y = alien7_new_y
                    alien7_new_y = random.randint(150, self.shape.height() - 300)
                    self.alien7_label.show()
                    alien7_startpos = self.shape.width() * 2

            # kretanje stena, koje se pojavljuju iznova nakon što stignu do ivice ekrana - donja strana ekrana
            self.rock1_label.setGeometry(rock1_startpos, self.rock1_rec.y(), self.rock1_rec.width(),
                                         self.rock1_rec.height())
            self.rock1_rec = self.rock1_label.geometry()
            if self.rock1_rec.x() < -300:
                self.rock1_label.hide()

            if self.rock1_label.isHidden():
                self.rock1_label.setGeometry(1600, self.rock1_rec.y(), self.rock1_rec.width(), self.rock1_rec.height())
                self.rock1_label.show()
                rock1_startpos = 1600

            self.rock2_label.setGeometry(rock2_startpos, self.rock2_rec.y(), self.rock2_rec.width(),
                                         self.rock2_rec.height())
            self.rock2_rec = self.rock2_label.geometry()
            if self.rock2_rec.x() < -300:
                self.rock2_label.hide()

            if self.rock2_label.isHidden():
                self.rock2_label.setGeometry(1600, self.rock2_rec.y(), self.rock2_rec.width(), self.rock2_rec.height())
                self.rock2_label.show()
                rock2_startpos = 1600

            self.rock3_label.setGeometry(rock3_startpos, self.rock3_rec.y(), self.rock3_rec.width(),
                                         self.rock3_rec.height())
            self.rock3_rec = self.rock3_label.geometry()
            if self.rock3_rec.x() < -300:
                self.rock3_label.hide()

            if self.rock3_label.isHidden():
                self.rock3_label.setGeometry(1600, self.rock3_rec.y(), self.rock3_rec.width(), self.rock3_rec.height())
                self.rock3_label.show()
                rock3_startpos = 1600

            self.rock4_label.setGeometry(rock4_startpos, self.rock4_rec.y(), self.rock4_rec.width(),
                                         self.rock4_rec.height())
            self.rock4_rec = self.rock4_label.geometry()
            if self.rock4_rec.x() < -300:
                self.rock4_label.hide()

            if self.rock4_label.isHidden():
                self.rock4_label.setGeometry(1600, self.rock4_rec.y(), self.rock4_rec.width(), self.rock4_rec.height())
                self.rock4_label.show()
                rock4_startpos = 1600

            # kretanje stena, koje se pojavljuju iznova nakon što stignu do ivice ekrana - goranja strana ekrana
            self.rock1_rot_label.setGeometry(rock1_startpos, self.rock1_rot_rec.y(), self.rock1_rot_rec.width(),
                                             self.rock1_rot_rec.height())
            self.rock1_rot_rec = self.rock1_rot_label.geometry()
            if self.rock1_rec.x() < -300:
                self.rock1_rot_label.hide()

            if self.rock1_rot_label.isHidden():
                self.rock1_rot_label.setGeometry(1600, self.rock1_rot_rec.y(), self.rock1_rot_rec.width(),
                                                 self.rock1_rot_rec.height())
                self.rock1_rot_label.show()
                rock1_startpos = 1600

            self.rock2_rot_label.setGeometry(rock2_startpos, self.rock2_rot_rec.y(), self.rock2_rot_rec.width(),
                                             self.rock2_rot_rec.height())
            self.rock2_rot_rec = self.rock2_rot_label.geometry()
            if self.rock2_rot_rec.x() < -300:
                self.rock2_rot_label.hide()

            if self.rock2_rot_label.isHidden():
                self.rock2_rot_label.setGeometry(1600, self.rock2_rot_rec.y(), self.rock2_rot_rec.width(),
                                                 self.rock2_rot_rec.height())
                self.rock2_rot_label.show()
                rock2_startpos = 1600

            self.rock3_rot_label.setGeometry(rock3_startpos, self.rock3_rot_rec.y(), self.rock3_rot_rec.width(),
                                             self.rock3_rot_rec.height())
            self.rock3_rot_rec = self.rock3_rot_label.geometry()
            if self.rock3_rot_rec.x() < -300:
                self.rock3_rot_label.hide()

            if self.rock3_rot_label.isHidden():
                self.rock3_rot_label.setGeometry(1600, self.rock3_rot_rec.y(), self.rock3_rot_rec.width(),
                                                 self.rock3_rot_rec.height())
                self.rock3_rot_label.show()
                rock3_startpos = 1600

            self.rock4_rot_label.setGeometry(rock4_startpos, self.rock4_rot_rec.y(), self.rock4_rot_rec.width(),
                                             self.rock4_rot_rec.height())
            self.rock4_rot_rec = self.rock4_rot_label.geometry()
            if self.rock4_rot_rec.x() < -300:
                self.rock1_rot_label.hide()

            if self.rock4_rot_label.isHidden():
                self.rock4_rot_label.setGeometry(1600, self.rock4_rot_rec.y(), self.rock4_rot_rec.width(),
                                                 self.rock4_rot_rec.height())
                self.rock4_rot_label.show()
                rock4_startpos = 1600

            # proverava se da li je svemirski brod udario vanzemaljca
            # i ako jeste, svemirac nestaje, a igrač gubi život.
            if abs(self.alien1_label.x() - self.spaceship1_label.x()) < 80 and abs(
                    self.alien1_label.y() - self.spaceship1_label.y()) < 60:
                self.alien1_label.hide()
                self.lives -= 1

            if abs(self.alien2_label.x() - self.spaceship1_label.x()) < 80 and abs(
                    self.alien2_label.y() - self.spaceship1_label.y()) < 60:
                self.alien2_label.hide()
                self.lives -= 1

            if abs(self.alien3_label.x() - self.spaceship1_label.x()) < 80 and abs(
                    self.alien3_label.y() - self.spaceship1_label.y()) < 60:
                self.alien3_label.hide()
                self.lives -= 1

            if abs(self.alien4_label.x() - self.spaceship1_label.x()) < 80 and abs(
                    self.alien4_label.y() - self.spaceship1_label.y()) < 60:
                self.alien4_label.hide()
                self.lives -= 1

            if abs(self.alien5_label.x() - self.spaceship1_label.x()) < 80 and abs(
                    self.alien5_label.y() - self.spaceship1_label.y()) < 60:
                self.alien5_label.hide()
                self.lives -= 1

            # kada svemirci stignu do ivice ekrana postaju sakriveni "hidden"
            # što će u sledećoj iteraciji biti indikator da se vrate na početne koordinate
            if self.alien1_label.x() < 0:
                self.alien1_label.hide()

            if self.alien2_label.x() < 0:
                self.alien2_label.hide()

            if self.alien3_label.x() < 0:
                self.alien3_label.hide()

            if self.alien4_label.x() < 0:
                self.alien4_label.hide()

            if self.alien5_label.x() < 0:
                self.alien5_label.hide()

            if self.alien6_label.x() < 0:
                self.alien6_label.hide()

            if self.alien7_label.x() < 0:
                self.alien7_label.hide()

            if abs(self.alien_missile1_label.x() - self.spaceship1_label.x()) < 40 and abs(
                    self.alien_missile1_label.y() - self.spaceship1_label.y()) < 30:
                self.lives -= 1
                missile1_startpos = -30

            if abs(self.alien_missile2_label.x() - self.spaceship1_label.x()) < 40 and abs(
                    self.alien_missile2_label.y() - self.spaceship1_label.y()) < 30:
                self.lives -= 1
                missile2_startpos = -30

            if abs(self.alien_missile3_label.x() - self.spaceship1_label.x()) < 40 and abs(
                    self.alien_missile3_label.y() - self.spaceship1_label.y()) < 30:
                self.lives -= 1
                missile3_startpos = -30

            if abs(self.alien_missile4_label.x() - self.spaceship1_label.x()) < 40 and abs(
                    self.alien_missile4_label.y() - self.spaceship1_label.y()) < 30:
                self.lives -= 1
                missile4_startpos = -30

            if abs(self.alien_missile5_label.x() - self.spaceship1_label.x()) < 40 and abs(
                    self.alien_missile5_label.y() - self.spaceship1_label.y()) < 30:
                self.lives -= 1
                missile5_startpos = -30

            # udaranje o kamen

            if abs((self.spaceship1_label.x() + 98) - (self.rock1_label.x() + 159)) < 159 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock1_label.y() + 106)) < 106:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1
            #
            if abs((self.spaceship1_label.x() + 98) - (self.rock2_label.x() + 94)) < 94 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock2_label.y() + 79)) < 79:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1

            # zbog apsolutnih zagrada mora ovako
            # i ne vaze pravila nejednacina, vec postoje dva slucaja ako bi se uklanjale apsolutne

            # if ((self.spaceship1_label.x()) - (self.rock3_label.x() )) < 404 and (
            # (self.spaceship1_label.y()) - (self.rock3_label.y())) < 150:
            #     if ((self.spaceship1_label.x()) - (self.rock3_label.x() )) > -98 and (
            #     (self.spaceship1_label.y()) - (self.rock3_label.y())) > -37:
            #        self.spaceship1_label.setGeometry(0, 400, 196, 74)

            if abs((self.spaceship1_label.x() + 98) - (self.rock3_label.x() + 250)) < 251 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock3_label.y() + 113)) < 113:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1

            if abs((self.spaceship1_label.x() + 98) - (self.rock4_label.x() + 213)) < 213 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock4_label.y() + 144)) < 144:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1

            # gornja strana ekrana
            if abs((self.spaceship1_label.x() + 98) - (self.rock1_rot_label.x() + 159)) < 159 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock1_rot_label.y() + 106)) < 106:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1
            #
            if abs((self.spaceship1_label.x() + 98) - (self.rock2_rot_label.x() + 94)) < 94 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock2_rot_label.y() + 79)) < 79:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1

            if abs((self.spaceship1_label.x() + 98) - (self.rock3_rot_label.x() + 250)) < 251 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock3_rot_label.y() + 113)) < 113:
                self.spaceship1_label.setGeometry(0, 400, 196, 74)
                self.lives -= 1

            if abs((self.spaceship1_label.x() + 98) - (self.rock4_rot_label.x() + 213)) < 213 and abs(
                    (self.spaceship1_label.y() + 37) - (self.rock4_rot_label.y() + 144)) < 144:
                self.lives -= 1
                # ovo verovatno nece moci za 2 igraca - treptanje nakon poginuća
                """
                self.spaceship1_label.hide()
                QtTest.QTest.qWait(244)
                self.spaceship1_label.show()
                QtTest.QTest.qWait(244)
                self.spaceship1_label.hide()
                QtTest.QTest.qWait(244)
                self.spaceship1_label.show()
                """
                self.spaceship1_label.setGeometry(0, 400, 196, 74)

            self.lives_label.setText(str(self.lives))

            if self.lives < 0:
                self.spaceship1_label.hide()
                self.spaceship1_label.setGeometry(99999, 99999, self.spaceship1_label.width(),
                                                  self.spaceship1_label.height())

            # "čekanje" procesa
            QtTest.QTest.qWait(5)
        return

    # metoda za kretanje igrača
    def __update_position__(self, key):

        rec1 = self.spaceship2_label.geometry()
        rec2 = self.spaceship1_label.geometry()
        self.spaceship1_rec = self.spaceship1_label.geometry()

        # u zavisnosti od pritisnutog dugmeta igrač(svemirski brod) se pomera za 5 po određenoj osi
        # metoda se poziva iz treda sve dok je dugme pritisnuto u intervalima od po 0.01 ms
        if key == Qt.Key_Right:
            self.spaceship2_label.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.spaceship2_label.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.spaceship2_label.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.spaceship2_label.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())

        # kretanje drugog igrača
        if key == Qt.Key_D:
            self.spaceship1_label.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_S:
            self.spaceship1_label.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            self.spaceship1_label.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
        elif key == Qt.Key_A:
            self.spaceship1_label.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())

        self.spaceship1_rec = self.spaceship1_label.geometry()


# Главни програм
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())
