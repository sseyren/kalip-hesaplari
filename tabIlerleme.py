#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.Qt import Qt, QFont

from math import pi

class Tab(QWidget):
    def __init__(self, parent=None):
        super(Tab, self).__init__(parent)
        self.devirSonuc = 0.0

        doubleValidator = QDoubleValidator()
        maxGenislik = 200

        self.girdiKesmeHizi = QLineEdit(alignment=Qt.AlignRight, maximumWidth=maxGenislik)
        self.girdiKesmeHizi.setValidator(doubleValidator)

        self.girdiTaramaKafasiCapi = QLineEdit(alignment=Qt.AlignRight, maximumWidth=maxGenislik)
        self.girdiTaramaKafasiCapi.setValidator(doubleValidator)

        self.girdiTaramaKafasiAgizSayisi = QLineEdit(alignment=Qt.AlignRight, maximumWidth=maxGenislik)
        self.girdiTaramaKafasiAgizSayisi.setValidator(doubleValidator)

        self.girdiDisBasinaDusenIlerleme = QLineEdit(alignment=Qt.AlignRight, maximumWidth=maxGenislik)
        self.girdiDisBasinaDusenIlerleme.setValidator(doubleValidator)

        hesaplaButon = QPushButton("Hesapla")
        hesaplaButon.clicked.connect(self.hesapla)

        girdiLayout = QGridLayout()
        girdiLayout.addWidget(QLabel("Kesme hızı (Vc):", alignment=Qt.AlignCenter), 0, 0)
        girdiLayout.addWidget(self.girdiKesmeHizi, 0, 1)
        girdiLayout.addWidget(QLabel("m/dk"), 0, 2)
        girdiLayout.addWidget(QLabel("Tarama\nkafası çapı (D):", alignment=Qt.AlignCenter), 1, 0)
        girdiLayout.addWidget(self.girdiTaramaKafasiCapi, 1, 1)
        girdiLayout.addWidget(QLabel("mm"), 1, 2)
        girdiLayout.addWidget(QLabel("Tarama kafası\nağız sayısı (Z):", alignment=Qt.AlignCenter), 2, 0)
        girdiLayout.addWidget(self.girdiTaramaKafasiAgizSayisi, 2, 1)
        girdiLayout.addWidget(QLabel("adet"))
        girdiLayout.addWidget(QLabel("Diş başına\ndüşen ilerleme (fz):", alignment=Qt.AlignCenter), 3, 0)
        girdiLayout.addWidget(self.girdiDisBasinaDusenIlerleme, 3, 1)
        girdiLayout.addWidget(hesaplaButon, 4, 0, 1, 2)

        self.ciktiDevir = QLabel("-")
        self.ciktiIlerleme = QLabel("-")

        ciktiLayout = QGridLayout()
        ciktiLayout.setContentsMargins(0,0,0,0)
        ciktiLayout.addWidget(QLabel("Devir (S): "), 0, 0)
        ciktiLayout.addWidget(self.ciktiDevir, 0, 1)
        ciktiLayout.addWidget(QLabel("İlerleme (F): "), 1, 0)
        ciktiLayout.addWidget(self.ciktiIlerleme, 1, 1)

        ciktiWidget = QWidget()
        ciktiWidget.setLayout(ciktiLayout)
        ciktiFont = QFont()
        ciktiFont.setPointSize(13)
        ciktiWidget.setFont(ciktiFont)

        yatay = QHBoxLayout()
        yatay.addStretch()
        yatay.addLayout(girdiLayout)
        yatay.addSpacing(50)
        yatay.addWidget(ciktiWidget)
        yatay.addStretch()

        self.setLayout(yatay)
    
    def hesapla(self):
        kesmeHizi = self.girdiKesmeHizi.text().strip()
        taramaKafasiCapi = self.girdiTaramaKafasiCapi.text().strip()
        taramaKafasiAgizSayisi = self.girdiTaramaKafasiAgizSayisi.text().strip()
        disBasinaDusenIlerleme = self.girdiDisBasinaDusenIlerleme.text().strip()

        if kesmeHizi and taramaKafasiCapi:
            try:
                devirSonuc = (float(kesmeHizi) * 1000) / (pi * float(taramaKafasiCapi))
                self.ciktiDevir.setText(str(round(devirSonuc, 1)) + "   devir/dk")
                if taramaKafasiAgizSayisi and disBasinaDusenIlerleme:
                    ilerlemeSonuc = devirSonuc * float(taramaKafasiAgizSayisi) * float(disBasinaDusenIlerleme)
                    self.ciktiIlerleme.setText(str(round(ilerlemeSonuc, 1)) + "   mm/dk")
                else:
                    self.ciktiIlerleme.setText("-")
                    QMessageBox.information(self, "Uyarı", "İlerlemenin hesaplanabilmesi için \"Tarama kafası ağız sayısı\" ve \"Diş başına düşen ilerleme\" girilmelidir.", QMessageBox.Ok)
            except (ValueError):
                QMessageBox.critical(self, "Hata", "Hatalı girdi girdiniz. Ondalıklı sayıları \".\" (nokta) ile belirtiniz.")
        else:
            QMessageBox.critical(self, "Hata", "En azından devirin hesaplanabilmesi için \"Kesme hızı\" ve \"Tarama kafası hızı\"nın girilmesi gerekir.", QMessageBox.Ok)