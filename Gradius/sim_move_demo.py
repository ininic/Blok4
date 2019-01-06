import sys
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDesktopWidget
from PyQt5 import QtTest
import multiprocessing as mp
from key_notifier import KeyNotifier
from worker import Worker

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


        self.pix12 = QPixmap('rotrock1.png')
        self.pix13 = QPixmap('rotrock2.png')
        self.pix14 = QPixmap('rotrock3.png')
        self.pix15 = QPixmap('rotrock4.png')
        self.pix8 = QPixmap('rocketa.png')

        # Objekti za manipulaciju u okviru GUI-a
        self.spaceship2_label = QLabel(self)
        self.spaceship1_label = QLabel(self)
        self.alien1_label = QLabel(self)
        self.alien2_label = QLabel(self)
        self.alien3_label = QLabel(self)
        self.alien4_label = QLabel(self)
        self.alien5_label = QLabel(self)
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
        self.alien_min_label = QLabel(self)

        self.rock1_rot_label = QLabel(self)
        self.rock2_rot_label = QLabel(self)
        self.rock3_rot_label = QLabel(self)
        self.rock4_rot_label = QLabel(self)


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

        self.spaceship2_label.setPixmap(self.pix1)
        self.spaceship2_label.setGeometry(1900, 80, 178, 77)

        self.spaceship1_label.setPixmap(self.pix2)
        self.spaceship1_label.setGeometry(0, 160, 196, 74)

        self.alien1_label.setPixmap(self.pix1)
        self.alien1_label.setGeometry(1800, 340, 178, 77)

        self.alien2_label.setPixmap(self.pix1)
        self.alien2_label.setGeometry(1900, 440, 178, 77)

        self.alien3_label.setPixmap(self.pix1)
        self.alien3_label.setGeometry(1800, 540, 178, 77)

        self.alien4_label.setPixmap(self.pix1)
        self.alien4_label.setGeometry(1700, 240, 178, 77)

        self.alien5_label.setPixmap(self.pix1)
        self.alien5_label.setGeometry(2000, 640, 178, 77)

        self.rocket1_label.setPixmap(self.pix3)
        self.rocket1_label.setGeometry(-120, 160, 178, 77)

        self.rock1_label.setPixmap(self.pix4)
        self.rock1_label.setGeometry(1300, self.shape.height() - 200, 298, 213)

        self.rock2_label.setPixmap(self.pix5)
        self.rock2_label.setGeometry(1100, self.shape.height() - 200, 200, 175)

        self.rock3_label.setPixmap(self.pix6)
        self.rock3_label.setGeometry(600, self.shape.height() - 200, 502, 226)

        self.rock4_label.setPixmap(self.pix7)
        self.rock4_label.setGeometry(10, self.shape.height() - 300, 614, 500)

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
        self.alien_missile1_label.setGeometry(10, 10, 57, 55)

        self.alien_missile2_label.setPixmap(self.pix8)
        self.alien_missile2_label.setGeometry(10, 10, 57, 55)

        self.alien_missile3_label.setPixmap(self.pix8)
        self.alien_missile3_label.setGeometry(10, 10, 57, 55)

        self.alien_missile4_label.setPixmap(self.pix8)
        self.alien_missile4_label.setGeometry(10, 10, 57, 55)

        self.alien_missile5_label.setPixmap(self.pix8)
        self.alien_missile5_label.setGeometry(10, 10, 57, 55)

        self.alien_min_label.setPixmap(self.pix8)
        self.alien_min_label.setGeometry(10, 10, 57, 55)

        # preuzimanje koordinata labela
        self.spaceship2_rec = self.spaceship2_label.geometry()
        self.alien1_rec = self.alien1_label.geometry()
        self.alien2_rec = self.alien2_label.geometry()
        self.alien3_rec = self.alien3_label.geometry()
        self.alien4_rec = self.alien4_label.geometry()
        self.alien5_rec = self.alien5_label.geometry()
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

        rock1_startpos = self.rock1_rec.x()
        rock2_startpos = self.rock2_rec.x()
        rock3_startpos = self.rock3_rec.x()
        rock4_startpos = self.rock4_rec.x()

        rock1_rot_startpos = self.rock1_rot_rec.x()
        rock2_rot_startpos = self.rock2_rot_rec.x()
        rock3_rot_startpos = self.rock3_rot_rec.x()
        rock4_rot_startpos = self.rock4_rot_rec.x()


    # naslov prozora
        self.setWindowTitle('Sim Slide')
        self.show()

    # Override metode za pritisak na dugme sa tastature
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.work.add_key(event.key())
            self.work.keyscount += 1
        else:
            self.key_notifier.add_key(event.key())

    # Override metode za puštanje pritiska sa tastatur
    def keyReleaseEvent(self, event):

        if event.key() == Qt.Key_Space:
            self.work.rem_key(event.key())
            #self.work.thread.quit()
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
        if abs(self.rocket3_label.x() - self.spaceship2_label.x()) < 40 and abs(self.rocket3_label.y() - self.spaceship2_label.y()) < 40:
            self.spaceship2_label.hide()
        if abs(self.rocket3_label.x() - self.alien1_label.x()) < 40 and abs(self.rocket3_label.y() - self.alien1_label.y()) < 40:
            self.alien1_label.hide()
        if abs(self.rocket3_label.x() - self.alien2_label.x()) < 40 and abs(self.rocket3_label.y() - self.alien2_label.y()) < 40:
            self.alien2_label.hide()
        if abs(self.rocket3_label.x() - self.alien3_label.x()) < 40 and abs(self.rocket3_label.y() - self.alien3_label.y()) < 40:
            self.alien3_label.hide()
        if abs(self.rocket3_label.x() - self.alien4_label.x()) < 40 and abs(self.rocket3_label.y() - self.alien4_label.y()) < 40:
            self.alien4_label.hide()
        if abs(self.rocket3_label.x() - self.alien5_label.x()) < 40 and abs(self.rocket3_label.y() - self.alien5_label.y()) < 40:
            self.alien5_label.hide()

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
            self.rocket3_label.setGeometry(self.startposx3, self.startposy3, self.rocket3_rec.width(), self.rocket3_rec.height())
            self.startposx3 += 11

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

    def fire2(self):
        print('RAKETA2')

        if abs(self.rocket2_label.x() - self.spaceship2_label.x()) < 40 and abs(self.rocket2_label.y() - self.spaceship2_label.y()) < 40:
            self.spaceship2_label.hide()
        if abs(self.rocket2_label.x() - self.alien1_label.x()) < 40 and abs(self.rocket2_label.y() - self.alien1_label.y()) < 40:
            self.alien1_label.hide()
        if abs(self.rocket2_label.x() - self.alien2_label.x()) < 40 and abs(self.rocket2_label.y() - self.alien2_label.y()) < 40:
            self.alien2_label.hide()
        if abs(self.rocket2_label.x() - self.alien3_label.x()) < 40 and abs(self.rocket2_label.y() - self.alien3_label.y()) < 40:
            self.alien3_label.hide()
        if abs(self.rocket2_label.x() - self.alien4_label.x()) < 40 and abs(self.rocket2_label.y() - self.alien4_label.y()) < 40:
            self.alien4_label.hide()
        if abs(self.rocket2_label.x() - self.alien5_label.x()) < 40 and abs(self.rocket2_label.y() - self.alien5_label.y()) < 40:
            self.alien5_label.hide()

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
            self.rocket2_label.setGeometry(self.startposx2, self.startposy2, self.rocket2_rec.width(), self.rocket2_rec.height())
            self.startposx2 += 11

    def fire(self):
        print('RAKETA1')

        self.rocket1_rec = self.rocket1_label.geometry()

        if abs(self.rocket1_label.x() - self.spaceship2_label.x()) < 40 and abs(self.rocket1_label.y() - self.spaceship2_label.y()) < 40:
            self.spaceship2_label.hide()
        if abs(self.rocket1_label.x() - self.alien1_label.x()) < 40 and abs(self.rocket1_label.y() - self.alien1_label.y()) < 40:
            self.alien1_label.hide()
        if abs(self.rocket1_label.x() - self.alien2_label.x()) < 40 and abs(self.rocket1_label.y() - self.alien2_label.y()) < 40:
            self.alien2_label.hide()
        if abs(self.rocket1_label.x() - self.alien3_label.x()) < 40 and abs(self.rocket1_label.y() - self.alien3_label.y()) < 40:
            self.alien3_label.hide()
        if abs(self.rocket1_label.x() - self.alien4_label.x()) < 40 and abs(self.rocket1_label.y() - self.alien4_label.y()) < 40:
            self.alien4_label.hide()
        if abs(self.rocket1_label.x() - self.alien5_label.x()) < 40 and abs(self.rocket1_label.y() - self.alien5_label.y()) < 40:
            self.alien5_label.hide()

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
            self.rocket1_label.setGeometry(self.startposx, self.startposy, self.rocket1_rec.width(), self.rocket1_rec.height())
            self.startposx += 11


# metoda koja omogućava kretanje svemiraca i reljefa(stena)
    def send(self,):
        print('Hello from proccess!')
        # početne pozicije elemenata
        a = self.alien1_rec.x()
        b = self.alien2_rec.x()
        c = self.alien2_rec.x()
        d = self.alien2_rec.x()
        e = self.alien2_rec.x()
        f = self.alien2_rec.x()

        g = self.rock1_rec.x()
        h = self.rock2_rec.x()
        i = self.rock3_rec.x()
        j = self.rock4_rec.x()

        g_rot = self.rock1_rot_rec.x()
        h_rot = self.rock2_rot_rec.x()
        i_rot = self.rock3_rot_rec.x()
        j_rot = self.rock4_rot_rec.x()

        k = self.alien1_rec.x()
        m = self.alien2_rec.x()
        n = self.alien3_rec.x()
        o = self.alien4_rec.x()
        p = self.alien5_rec.x()
        r = self.rocket1_rec.x()
        s = self.rock1_rec.x()

        rock1_startpos = self.rock1_rec.x()
        rock2_startpos = self.rock2_rec.x()
        rock3_startpos = self.rock3_rec.x()
        rock4_startpos = self.rock4_rec.x()


        for x in range(0, 12715):
            # postavke brzina kretanja određenih elemenata
            a -= 2
            b -= 2
            c -= 1
            d -= 2
            e -= 3
            f -= 1
            g -= 1
            h -= 1
            i -= 1
            j -= 1
            k -= 7
            m -= 7
            n -= 7
            o -= 7
            p -= 7
            r -= 7
            s -= 7

            rock1_startpos -= (self.level * 0.3)
            rock2_startpos -= (self.level * 0.3)
            rock3_startpos -= (self.level * 0.3)
            rock4_startpos -= (self.level * 0.3)

            #rock1_rot_startpos -= (self.level * 0.3)
            #rock2_rot_startpos -= (self.level * 0.3)
            #rock3_rot_startpos -= (self.level * 0.3)
            #rock4_rot_startpos -= (self.level * 0.3)


            # kretanje svemiraca, koji se pojavljuju iznova ako su ubijeni, odnosno "sakriveni" (isHidden)
            self.alien1_label.setGeometry(a, self.alien1_rec.y(), self.alien1_rec.width(), self.alien1_rec.height())
            if x % 500 == 0:
                k = a
            self.alien_missile1_label.setGeometry(k, self.alien1_rec.y(), self.alien_missile1_rec.width(), self.alien_missile1_rec.height())
            if self.alien1_label.isHidden():
                self.alien1_label.setGeometry(2000, self.alien1_rec.y(), self.alien1_rec.width(), self.alien1_rec.height())
                self.alien1_label.show()
                a = 2000

            self.alien2_label.setGeometry(b, self.alien2_rec.y(), self.alien2_rec.width(), self.alien2_rec.height())
            if x % 550 == 0:
                m = b
            self.alien_missile2_label.setGeometry(m, self.alien2_rec.y(), self.alien_missile2_rec.width(), self.alien_missile2_rec.height())
            if self.alien2_label.isHidden():
                self.alien2_label.setGeometry(2000, self.alien2_rec.y(), self.alien2_rec.width(), self.alien2_rec.height())
                self.alien2_label.show()
                b = 2000

            self.alien3_label.setGeometry(c, self.alien3_rec.y(), self.alien3_rec.width(), self.alien3_rec.height())
            if x % 450 == 0:
                n = c
            self.alien_missile3_label.setGeometry(n, self.alien3_rec.y(), self.alien_missile3_rec.width(), self.alien_missile3_rec.height())
            if self.alien3_label.isHidden():
                self.alien3_label.setGeometry(2000, self.alien3_rec.y(), self.alien3_rec.width(), self.alien3_rec.height())
                self.alien3_label.show()
                c = 2000


            self.alien4_label.setGeometry(d, self.alien4_rec.y(), self.alien4_rec.width(), self.alien4_rec.height())
            if x % 600 == 0:
                o = d
            self.alien_missile4_label.setGeometry(o, self.alien4_rec.y(), self.alien_missile4_rec.width(), self.alien_missile4_rec.height())
            if self.alien4_label.isHidden():
                self.alien4_label.setGeometry(2000, self.alien4_rec.y(), self.alien4_rec.width(), self.alien4_rec.height())
                self.alien4_label.show()
                d = 2000
            self.alien5_label.setGeometry(e, self.alien5_rec.y(), self.alien5_rec.width(), self.alien5_rec.height())
            if self.alien5_label.isHidden():
                self.alien5_label.setGeometry(2000, self.alien5_rec.y(), self.alien5_rec.width(), self.alien5_rec.height())
                self.alien5_label.show()
                e = 2000
            self.spaceship2_label.setGeometry(f, self.spaceship2_rec.y(), self.spaceship2_rec.width(), self.spaceship2_rec.height())
            if self.spaceship2_label.isHidden():
                self.spaceship2_label.setGeometry(2000, self.spaceship2_rec.y(), self.spaceship2_rec.width(), self.spaceship2_rec.height())
                self.spaceship2_label.show()
                f = 2000

            # kretanje stena, koje se pojavljuju iznova nakon što stignu do ivice ekrana
            self.rock1_label.setGeometry(g, self.rock1_rec.y(), self.rock1_rec.width(), self.rock1_rec.height())
            self.rock1_rec = self.rock1_label.geometry()
            if self.rock1_rec.x() < -300:
                self.rock1_label.hide()

            if self.rock1_label.isHidden():
                self.rock1_label.setGeometry(1600, self.rock1_rec.y(), self.rock1_rec.width(), self.rock1_rec.height())
                self.rock1_label.show()
                g = 1600


            self.rock1_rot_label.setGeometry(g, self.rock1_rot_rec.y(), self.rock1_rot_rec.width(), self.rock1_rot_rec.height() )
            self.rock1_rot_rec = self.rock1_rot_label.geometry()
            if self.rock1_rot_rec.x() < -300:
                self.rock1_rot_label.hide()

            if self.rock1_rot_label.isHidden():
                self.rock1_rot_label.setGeometry(1600, self.rock1_rot_rec.y(), self.rock1_rot_rec.width(), self.rock1_rot_rec.height())
                self.rock1_rot_label.show()
                g = 1600

            self.rock2_label.setGeometry(h, self.rock2_rec.y(), self.rock2_rec.width(), self.rock2_rec.height())
            self.rock2_rec = self.rock2_label.geometry()
            if self.rock2_rec.x() < -300:
                self.rock2_label.hide()

            if self.rock2_label.isHidden():
                self.rock2_label.setGeometry(1600, self.rock2_rec.y(), self.rock2_rec.width(), self.rock2_rec.height())
                self.rock2_label.show()
                h = 1600

            self.rock2_rot_label.setGeometry(h, self.rock2_rot_rec.y(), self.rock2_rot_rec.width(), self.rock2_rot_rec.height())
            self.rock2_rot_rec = self.rock2_rot_label.geometry()
            if self.rock2_rot_rec.x() < -300:
                self.rock2_rot_label.hide()

            if self.rock2_rot_label.isHidden():
                self.rock2_rot_label.setGeometry(1600, self.rock2_rot_rec.y(), self.rock2_rot_rec.width(), self.rock2_rot_rec.height())
                self.rock2_rot_label.show()
                h = 1600

            self.rock3_label.setGeometry(i, self.rock3_rec.y(), self.rock3_rec.width(), self.rock3_rec.height())
            self.rock3_rec = self.rock3_label.geometry()
            if self.rock3_rec.x() < -300:
                self.rock3_label.hide()

            if self.rock3_label.isHidden():
                self.rock3_label.setGeometry(1600, self.rock3_rec.y(), self.rock3_rec.width(), self.rock3_rec.height())
                self.rock3_label.show()
                i = 1600

            self.rock3_rot_label.setGeometry(i, self.rock3_rot_rec.y(), self.rock3_rot_rec.width(), self.rock3_rot_rec.height())
            self.rock3_rec = self.rock3_rot_label.geometry()
            if self.rock3_rec.x() < -300:
                self.rock3_rot_label.hide()

            if self.rock3_rot_label.isHidden():
                self.rock3_rot_label.setGeometry(1600, self.rock3_rot_rec.y(), self.rock3_rot_rec.width(), self.rock3_rot_rec.height())
                self.rock3_rot_label.show()
                i = 1600

            self.rock4_label.setGeometry(j, self.rock4_rec.y(), self.rock4_rec.width(), self.rock4_rec.height())
            self.rock4_rec = self.rock4_label.geometry()
            if self.rock4_rec.x() < -300:
                self.rock4_label.hide()

            if self.rock4_label.isHidden():
                self.rock4_label.setGeometry(1600, self.rock4_rec.y(), self.rock4_rec.width(), self.rock4_rec.height())
                self.rock4_label.show()
                j = 1600


            self.rock4_rot_label.setGeometry(j, self.rock4_rot_rec.y(), self.rock4_rot_rec.width(), self.rock4_rot_rec.height())
            self.rock4_rot_rec = self.rock4_rot_label.geometry()
            if self.rock4_rot_rec.x() < -300:
                self.rock4_rot_label.hide()

            if self.rock4_rot_label.isHidden():
                self.rock4_rot_label.setGeometry(1600, self.rock4_rot_rec.y(), self.rock4_rot_rec.width(), self.rock4_rot_rec.height())
                self.rock4_rot_label.show()
                j = 1600

                # kretanje stena, koje se pojavljuju iznova nakon što stignu do ivice ekrana - gornja strana ekrana
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
            if abs(self.spaceship2_label.x() - self.spaceship1_label.x()) < 80 and abs(self.spaceship2_label.y() - self.spaceship1_label.y()) < 60:
                self.spaceship2_label.hide()

            if abs(self.alien1_label.x() - self.spaceship1_label.x()) < 80 and abs(self.alien1_label.y() - self.spaceship1_label.y()) < 60:
                self.alien1_label.hide()

            if abs(self.alien2_label.x() - self.spaceship1_label.x()) < 80 and abs(self.alien2_label.y() - self.spaceship1_label.y()) < 60:
                self.alien2_label.hide()

            if abs(self.alien3_label.x() - self.spaceship1_label.x()) < 80 and abs(self.alien3_label.y() - self.spaceship1_label.y()) < 60:
                self.alien3_label.hide()

            if abs(self.alien4_label.x() - self.spaceship1_label.x()) < 80 and abs(self.alien4_label.y() - self.spaceship1_label.y()) < 60:
                self.alien4_label.hide()

            if abs(self.alien5_label.x() - self.spaceship1_label.x()) < 80 and abs(self.alien5_label.y() - self.spaceship1_label.y()) < 60:
                self.alien5_label.hide()

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

            if abs((self.spaceship1_label.x() + 98) - (self.rock3_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock3_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1

            if abs((self.spaceship1_label.x() + 98) - (self.rock4_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock4_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1

            if abs((self.spaceship1_label.x() + 98) - (self.rock1_rot_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock1_rot_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1


            if abs((self.spaceship1_label.x() + 98) - (self.rock2_rot_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock2_rot_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1


            if abs((self.spaceship1_label.x() + 98) - (self.rock3_rot_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock3_rot_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1


            if abs((self.spaceship1_label.x() + 98) - (self.rock4_rot_label.x() + 159)) < 159 and abs(
                        (self.spaceship1_label.y() + 37) - (self.rock4_rot_label.y() + 106)) < 106:
                    self.spaceship1_label.setGeometry(0, 400, 196, 74)
                    self.lives -= 1


            # "čekanje" procesa
            QtTest.QTest.qWait(5)
        return
# Главни програм...
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())
