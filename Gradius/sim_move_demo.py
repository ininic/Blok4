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

    def fire2(self):
        print('RAKETA2')

        if abs(self.label13.x() - self.label1.x()) < 40 and abs(self.label13.y() - self.label1.y()) < 40:
            self.label1.hide()
        if abs(self.label13.x() - self.label3.x()) < 40 and abs(self.label13.y() - self.label3.y()) < 40:
            self.label3.hide()
        if abs(self.label13.x() - self.label4.x()) < 40 and abs(self.label13.y() - self.label4.y()) < 40:
            self.label4.hide()
        if abs(self.label13.x() - self.label5.x()) < 40 and abs(self.label13.y() - self.label5.y()) < 40:
            self.label5.hide()
        if abs(self.label13.x() - self.label6.x()) < 40 and abs(self.label13.y() - self.label6.y()) < 40:
            self.label6.hide()
        if abs(self.label13.x() - self.label7.x()) < 40 and abs(self.label13.y() - self.label7.y()) < 40:
            self.label7.hide()

        if self.globalcounter2 == 0:
            self.startposx2 = self.rec2.x()
            self.startposy2 = self.rec2.y()
        self.globalcounter2 = 1

        self.globalcounter22 += 1
        if self.globalcounter22 > 165:
            self.startposy2 = self.rec2.y()
            self.startposx2 = self.rec2.x()
            self.label13.hide()
            self.globalcounter22 = 1
        else:
            self.label13.show()
            self.label13.setGeometry(self.startposx2, self.startposy2, self.rec13.width(), self.rec13.height())
            self.startposx2 += 11

    def fire(self):
        print('RAKETA1')

        self.rec8 = self.label8.geometry()

        if abs(self.label8.x() - self.label1.x()) < 40 and abs(self.label8.y() - self.label1.y()) < 40:
            self.label1.hide()
        if abs(self.label8.x() - self.label3.x()) < 40 and abs(self.label8.y() - self.label3.y()) < 40:
            self.label3.hide()
        if abs(self.label8.x() - self.label4.x()) < 40 and abs(self.label8.y() - self.label4.y()) < 40:
            self.label4.hide()
        if abs(self.label8.x() - self.label5.x()) < 40 and abs(self.label8.y() - self.label5.y()) < 40:
            self.label5.hide()
        if abs(self.label8.x() - self.label6.x()) < 40 and abs(self.label8.y() - self.label6.y()) < 40:
            self.label6.hide()
        if abs(self.label8.x() - self.label7.x()) < 40 and abs(self.label8.y() - self.label7.y()) < 40:
            self.label7.hide()

        if self.globalcounter1 == 0:
            self.startposx = self.rec2.x()
            self.startposy = self.rec2.y()
        self.globalcounter1 = 1

        self.globalcounter21 += 1
        if self.globalcounter21 > 165:
            self.startposy = self.rec2.y()
            self.startposx = self.rec2.x()
            self.label8.hide()
            self.globalcounter21 = 1
        else:
            self.label8.show()
            self.label8.setGeometry(self.startposx, self.startposy, self.rec8.width(), self.rec8.height())
            self.startposx += 11


# metoda koja omogućava kretanje svemiraca i reljefa(stena)
def send(self,):
    print('Hello from proccess!')
    # početne pozicije elemenata
    a = self.rec3.x()
    b = self.rec4.x()
    c = self.rec4.x()
    d = self.rec4.x()
    e = self.rec4.x()
    f = self.rec4.x()
    g = self.rec9.x()
    h = self.rec10.x()
    i = self.rec11.x()
    j = self.rec12.x()

    k = self.rec3.x()
    m = self.rec4.x()
    n = self.rec5.x()
    o = self.rec6.x()
    p = self.rec7.x()
    r = self.rec8.x()
    s = self.rec9.x()
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


        # kretanje svemiraca, koji se pojavljuju iznova ako su ubijeni, odnosno "sakriveni" (isHidden)
        self.label3.setGeometry(a, self.rec3.y(), self.rec3.width(), self.rec3.height())
        if x % 500 == 0:
            k = a
        self.label15.setGeometry(k, self.rec3.y(), self.rec15.width(), self.rec15.height())
        if self.label3.isHidden():
            self.label3.setGeometry(2000, self.rec3.y(), self.rec3.width(), self.rec3.height())
            self.label3.show()
            a = 2000

        self.label4.setGeometry(b, self.rec4.y(), self.rec4.width(), self.rec4.height())
        if x % 550 == 0:
            m = b
        self.label16.setGeometry(m, self.rec4.y(), self.rec16.width(), self.rec16.height())
        if self.label4.isHidden():
            self.label4.setGeometry(2000, self.rec4.y(), self.rec4.width(), self.rec4.height())
            self.label4.show()
            b = 2000

        self.label5.setGeometry(c, self.rec5.y(), self.rec5.width(), self.rec5.height())
        if x % 450 == 0:
            n = c
        self.label17.setGeometry(n, self.rec5.y(), self.rec17.width(), self.rec17.height())
        if self.label5.isHidden():
            self.label5.setGeometry(2000, self.rec5.y(), self.rec5.width(), self.rec5.height())
            self.label5.show()
            c = 2000


        self.label6.setGeometry(d, self.rec6.y(), self.rec6.width(), self.rec6.height())
        if x % 600 == 0:
            o = d
        self.label18.setGeometry(o, self.rec6.y(), self.rec18.width(), self.rec18.height())
        if self.label6.isHidden():
            self.label6.setGeometry(2000, self.rec6.y(), self.rec6.width(), self.rec6.height())
            self.label6.show()
            d = 2000
        self.label7.setGeometry(e, self.rec7.y(), self.rec7.width(), self.rec7.height())
        if self.label7.isHidden():
            self.label7.setGeometry(2000, self.rec7.y(), self.rec7.width(), self.rec7.height())
            self.label7.show()
            e = 2000
        self.label1.setGeometry(f, self.rec1.y(), self.rec1.width(), self.rec1.height())
        if self.label1.isHidden():
            self.label1.setGeometry(2000, self.rec1.y(), self.rec1.width(), self.rec1.height())
            self.label1.show()
            f = 2000

        # kretanje stena, koje se pojavljuju iznova nakon što stignu do ivice ekrana
        self.label9.setGeometry(g, self.rec9.y(), self.rec9.width(), self.rec9.height())
        self.rec9 = self.label9.geometry()
        if self.rec9.x() < -300:
            self.label9.hide()

        if self.label9.isHidden():
            self.label9.setGeometry(1600, self.rec9.y(), self.rec9.width(), self.rec9.height())
            self.label9.show()
            g = 1600

        self.label10.setGeometry(h, self.rec10.y(), self.rec10.width(), self.rec10.height())
        self.rec10 = self.label10.geometry()
        if self.rec10.x() < -300:
            self.label10.hide()

        if self.label10.isHidden():
            self.label10.setGeometry(1600, self.rec10.y(), self.rec10.width(), self.rec10.height())
            self.label10.show()
            h = 1600

        self.label11.setGeometry(i, self.rec11.y(), self.rec11.width(), self.rec11.height())
        self.rec11 = self.label11.geometry()
        if self.rec11.x() < -300:
            self.label11.hide()

        if self.label11.isHidden():
            self.label11.setGeometry(1600, self.rec11.y(), self.rec11.width(), self.rec11.height())
            self.label11.show()
            i = 1600

        self.label12.setGeometry(j, self.rec12.y(), self.rec12.width(), self.rec12.height())
        self.rec12 = self.label12.geometry()
        if self.rec12.x() < -300:
            self.label12.hide()

        if self.label12.isHidden():
            self.label12.setGeometry(1600, self.rec12.y(), self.rec12.width(), self.rec12.height())
            self.label12.show()
            j = 1600

        # proverava se da li je svemirski brod udario vanzemaljca
        # i ako jeste, svemirac nestaje, a igrač gubi život.
        if abs(self.label1.x() - self.label2.x()) < 80 and abs(self.label1.y() - self.label2.y()) < 60:
            self.label1.hide()

        if abs(self.label3.x() - self.label2.x()) < 80 and abs(self.label3.y() - self.label2.y()) < 60:
            self.label3.hide()

        if abs(self.label4.x() - self.label2.x()) < 80 and abs(self.label4.y() - self.label2.y()) < 60:
            self.label4.hide()

        if abs(self.label5.x() - self.label2.x()) < 80 and abs(self.label5.y() - self.label2.y()) < 60:
            self.label5.hide()

        if abs(self.label6.x() - self.label2.x()) < 80 and abs(self.label6.y() - self.label2.y()) < 60:
            self.label6.hide()

        if abs(self.label7.x() - self.label2.x()) < 80 and abs(self.label7.y() - self.label2.y()) < 60:
            self.label7.hide()

        # "čekanje" procesa
        QtTest.QTest.qWait(5)
    return
# Главни програм...
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())
