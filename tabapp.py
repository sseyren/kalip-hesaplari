#!/usr/bin/env python3

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel)
from PyQt5.Qt import Qt

import tabSiyirmaKuvveti
import tabIlerleme

class Uygulama(QMainWindow):
    def __init__(self, parent=None):
        super(Uygulama, self).__init__(parent)

        tablar = QTabWidget()
        tablar.addTab(tabSiyirmaKuvveti.Tab(), "SIYIRMA KUVVETİ HESABI")
        tablar.addTab(tabIlerleme.Tab(), "İLERLEME VE DEVİR HESABI")

        self.setCentralWidget(tablar)
        self.setWindowTitle("KALIP HESAPLARI")

if __name__ == "__main__":
    import sys
    uyg = QApplication(sys.argv)
    aryz = Uygulama()
    aryz.show()
    sys.exit(uyg.exec_())