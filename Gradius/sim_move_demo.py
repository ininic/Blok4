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
        self.pix8 = QPixmap('rocketa.png')

        # Objekti za manipulaciju u okviru GUI-a
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)
        self.label9 = QLabel(self)
        self.label10 = QLabel(self)
        self.label11 = QLabel(self)
        self.label12 = QLabel(self)
        self.label13 = QLabel(self)
        self.label14 = QLabel(self)
        self.label15 = QLabel(self)
        self.label16 = QLabel(self)
        self.label17 = QLabel(self)
        self.label18 = QLabel(self)
        self.label19 = QLabel(self)
        self.label20 = QLabel(self)




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


        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(1900, 80, 178, 77)

        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(0, 160, 196, 74)

        self.label3.setPixmap(self.pix1)
        self.label3.setGeometry(1800, 340, 178, 77)

        self.label4.setPixmap(self.pix1)
        self.label4.setGeometry(1900, 440, 178, 77)

        self.label5.setPixmap(self.pix1)
        self.label5.setGeometry(1800, 540, 178, 77)

        self.label6.setPixmap(self.pix1)
        self.label6.setGeometry(1700, 240, 178, 77)

        self.label7.setPixmap(self.pix1)
        self.label7.setGeometry(2000, 640, 178, 77)

        self.label8.setPixmap(self.pix3)
        self.label8.setGeometry(-120, 160, 178, 77)

        self.label9.setPixmap(self.pix4)
        self.label9.setGeometry(1300, self.shape.height()-200, 298, 213)

        self.label10.setPixmap(self.pix5)
        self.label10.setGeometry(1100, self.shape.height()-200, 200, 175)

        self.label11.setPixmap(self.pix6)
        self.label11.setGeometry(600, self.shape.height()-200, 502, 226)

        self.label12.setPixmap(self.pix7)
        self.label12.setGeometry(10, self.shape.height()-300, 614, 500)

        self.label13.setPixmap(self.pix3)
        self.label13.setGeometry(-120, 11, 178, 77)

        self.label14.setPixmap(self.pix3)
        self.label14.setGeometry(-120, 11, 178, 77)

        self.label15.setPixmap(self.pix8)
        self.label15.setGeometry(10, 10, 57, 55)

        self.label16.setPixmap(self.pix8)
        self.label16.setGeometry(10, 10, 57, 55)

        self.label17.setPixmap(self.pix8)
        self.label17.setGeometry(10, 10, 57, 55)

        self.label18.setPixmap(self.pix8)
        self.label18.setGeometry(10, 10, 57, 55)

        self.label19.setPixmap(self.pix8)
        self.label19.setGeometry(10, 10, 57, 55)

        self.label20.setPixmap(self.pix8)
        self.label20.setGeometry(10, 10, 57, 55)

        # preuzimanje koordinata labela
        self.rec1 = self.label1.geometry()
        self.rec3 = self.label3.geometry()
        self.rec4 = self.label4.geometry()
        self.rec5 = self.label5.geometry()
        self.rec6 = self.label6.geometry()
        self.rec7 = self.label7.geometry()
        self.rec2 = self.label2.geometry()
        self.rec8 = self.label8.geometry()
        self.rec9 = self.label9.geometry()
        self.rec10 = self.label10.geometry()
        self.rec11 = self.label11.geometry()
        self.rec12 = self.label12.geometry()
        self.rec13 = self.label13.geometry()
        self.rec14 = self.label14.geometry()
        self.rec15 = self.label15.geometry()
        self.rec16 = self.label16.geometry()
        self.rec17 = self.label17.geometry()
        self.rec18 = self.label18.geometry()
        self.rec19 = self.label19.geometry()
        self.rec20 = self.label20.geometry()

        # pomoćne promeljive
        self.startposy = self.rec2.y()
        self.startposx = self.rec2.x()
        self.startposy2 = self.rec2.y()
        self.startposx2 = self.rec2.x()
        self.startposy3 = self.rec2.y()
        self.startposx3 = self.rec2.x()
        self.globalcounter1 = 0
        self.globalcounter2 = 0
        self.globalcounter3 = 0
        self.globalcounter21 = 0
        self.globalcounter22 = 0
        self.globalcounter23 = 0

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
        if abs(self.label14.x() - self.label1.x()) < 40 and abs(self.label14.y() - self.label1.y()) < 40:
            self.label1.hide()
        if abs(self.label14.x() - self.label3.x()) < 40 and abs(self.label14.y() - self.label3.y()) < 40:
            self.label3.hide()
        if abs(self.label14.x() - self.label4.x()) < 40 and abs(self.label14.y() - self.label4.y()) < 40:
            self.label4.hide()
        if abs(self.label14.x() - self.label5.x()) < 40 and abs(self.label14.y() - self.label5.y()) < 40:
            self.label5.hide()
        if abs(self.label14.x() - self.label6.x()) < 40 and abs(self.label14.y() - self.label6.y()) < 40:
            self.label6.hide()
        if abs(self.label14.x() - self.label7.x()) < 40 and abs(self.label14.y() - self.label7.y()) < 40:
            self.label7.hide()

        # potrebno za prvo pozivanje metode - globalna promanljiva
        if self.globalcounter3 == 0:
            self.startposx3 = self.rec2.x()
            self.startposy3 = self.rec2.y()
        self.globalcounter3 = 1

        self.globalcounter23 += 1
        # provera da li je lokani brojac izbrojao do 165 - toliko je potrebno da se pređe ceo ekran
        # ako jeste, setuju se nove koordinate i resetuje se brojač
        if self.globalcounter23 > 165:
            self.startposy3 = self.rec2.y()
            self.startposx3 = self.rec2.x()
            self.label14.hide()
            self.globalcounter23 = 1
        else:
            # u običnim prolazima raketa se samo pomera za po 11 jedinica po x osi
            self.label14.show()
            self.label14.setGeometry(self.startposx3, self.startposy3, self.rec14.width(), self.rec14.height())
            self.startposx3 += 11

    # metoda za kretanje igrača
    def __update_position__(self, key):

        rec1 = self.label1.geometry()
        rec2 = self.label2.geometry()
        self.rec2 = self.label2.geometry()

        # u zavisnosti od pritisnutog dugmeta igrač(svemirski brod) se pomera za 5 po određenoj osi
        # metoda se poziva iz treda sve dok je dugme pritisnuto u intervalima od po 0.01 ms
        if key == Qt.Key_Right:
            self.label1.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.label1.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())

        # kretanje drugog igrača
        if key == Qt.Key_D:
            self.label2.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_S:
            self.label2.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            self.label2.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
        elif key == Qt.Key_A:
            self.label2.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())

        self.rec2 = self.label2.geometry()


# Главни програм...
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())
