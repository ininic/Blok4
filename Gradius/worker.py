import threading

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time

lock = threading.Lock()

class Worker(QObject):

    # potrebni signali
    newParams = pyqtSignal()
    newParams2 = pyqtSignal()
    newParams3 = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.keys = []
        self.keyscount = 0
        self.is_done = False
        self.Time = time
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.threadcounter = 0
        # kada se nit startuje pozvace se funkcija paramUp
        self.thread.started.connect(self.paramUp)

    # metoda iz koje se salju signali
    def sendsignal(self, br):
        if br == 1:
            for i in range(165):
                print(i, 'THREAD1:', threading.current_thread())
                self.newParams.emit()
                time.sleep(0.01)
            self.threadcounter -= 1
        if br == 0:
            for i in range(165):
                print(i, 'THREAD2:', threading.current_thread())
                self.newParams2.emit()
                time.sleep(0.01)
            self.threadcounter -= 1
        if br == 2:
            for i in range(165):
                print(i, 'THREAD3:', threading.current_thread())
                self.newParams3.emit()
                time.sleep(0.01)
            self.threadcounter -= 1


    def start(self):
        """
        Start notifications.
        """
        self.thread.start()

    @pyqtSlot()
    def paramUp(self):
        broj = 0
        # svaki pritisak na space dugme poziva nit kojoj se prosleđuju parametri 0,1 ili 2
        # u zavisnosti od tih parametara metoda koju nit izvrsava salje određene signale
        # ovi brojevi se ciklicno 0-1-2-0-1-2, tako da pozvana nit uglvnom ima vremena da zavrsi
        # svoje izvrsavanje pre nego sto bude pozvana druga nit koja emituje signal ka istoj metodi
        while not self.is_done:
            time.sleep(0.001)
            # nit se kreira i poziva samo ako je dugme pritisnutow
            if self.keyscount == 1 and self.threadcounter < 3:
                    if broj == 0:
                        broj = 1
                    elif broj == 1:
                        broj = 2
                    elif broj == 2:
                        broj = 0
                    self.threadb = threading.Thread(target=self.sendsignal, args=(broj,))
                    self.threadb.start()
                    self.threadcounter += 1
                    print('brojac: ', self.threadcounter, self.keyscount)
                    self.keyscount -= 1
                    time.sleep(0.05)

    def add_key(self, key):
        self.keys.append(key)
        print('helllllloooooo')

    def rem_key(self, key):
        self.keys.remove(key)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()
