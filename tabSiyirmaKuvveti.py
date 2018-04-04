#!/usr/bin/env python3

from collections import OrderedDict
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QLineEdit, QLabel, QPushButton, QComboBox, QInputDialog, QVBoxLayout, QFrame, QMessageBox, QHBoxLayout)
from PyQt5.Qt import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont

class Tab(QWidget):
    def __init__(self, parent=None):
        super(Tab, self).__init__()
        self.YERCEKIMI_IVMESI = 9.80655
        self.karsiYayKuvvetNDeger = 0.0
        self.karsiYayKuvvetKGDeger = 0.0
        self.OZEL_GIRDI_KEY = "Özel..."
        self.OZEL_GIRDI_INDEX = -1
        self.AYIRMA_KUVVET_ORAN_TABLO = OrderedDict([
            ("Kurşun", 2.5),
            ("Kalay", 3.5),
            ("Alüminyum", 5.6),
            ("Çinko", 10.0),
            ("Bakır", 15.5),
            ("Pirinç", 22.5),
            ("Nikel", 25.0),
            ("% 0.010 C Tavlanmış Çelik", 27.5),
            ("% 0.010 C Soğuk Haddelenmiş Çelik", 30.0),
            ("% 0.020 C Tavlanmış Çelik", 30.0),
            ("% 0.020 C Soğuk Haddelenmiş Çelik", 32.5),
            ("% 0.030 C Tavlanmış Çelik", 35.0),
            ("% 0.030 C Soğuk Haddelenmiş Çelik", 47.5),
            ("Paslanmaz Çelikler", 40.0),
            ("Silisyumlu Çelikler", 45.0),
            (self.OZEL_GIRDI_KEY, 50.0)
        ])

        doubleValidator = QDoubleValidator()
        intValidator = QIntValidator()

        self.sacKalinlikGirdi = QLineEdit(maximumWidth=250)
        self.sacKalinlikGirdi.setValidator(doubleValidator)
        self.sacKalinlikGirdi.setAlignment(Qt.AlignRight)
        self.sacKalinlikLabel = QLabel("Sac\nkalınlığı:")
        self.sacKalinlikLabel.setAlignment(Qt.AlignCenter)

        self.kesmeUzunlukGirdi = QLineEdit(maximumWidth=250, minimumWidth=250)
        self.kesmeUzunlukGirdi.setValidator(doubleValidator)
        self.kesmeUzunlukGirdi.setAlignment(Qt.AlignRight)
        self.kesmeUzunlukLabel = QLabel("Kesme\nuzunluğu:")
        self.kesmeUzunlukLabel.setAlignment(Qt.AlignCenter)

        self.kesmeMukavemetGirdi = QComboBox(maximumWidth=250)
        indexForLoop = 0
        for key,value in self.AYIRMA_KUVVET_ORAN_TABLO.items():
            if value == None:
                self.kesmeMukavemetGirdi.addItem(key)
            else:
                self.kesmeMukavemetGirdi.addItem(key+" ("+str(value)+")")
            if key == self.OZEL_GIRDI_KEY:
                self.OZEL_GIRDI_INDEX = indexForLoop
            indexForLoop = indexForLoop + 1
        self.kesmeMukavemetGirdi.activated[int].connect(self.kesmeMukavemetGirdiDegisti)
        self.kesmeMukavemetLabel = QLabel("Kesme\nMukavemeti:")
        self.kesmeMukavemetLabel.setAlignment(Qt.AlignCenter)

        self.ayirmaKuvetOranGirdi = QLineEdit(maximumWidth=250, minimumWidth=250)
        self.ayirmaKuvetOranGirdi.setValidator(doubleValidator)
        self.ayirmaKuvetOranGirdi.setAlignment(Qt.AlignRight)
        self.ayirmaKuvetOranLabel = QLabel("Ayırma\nKuvveti\nOranı:")
        self.ayirmaKuvetOranLabel.setAlignment(Qt.AlignCenter)

        self.hesapButon = QPushButton("Hesapla")
        self.hesapButon.clicked.connect(self.hesapla)

        grid = QGridLayout()
        grid.addWidget(self.sacKalinlikLabel, 0, 0)
        grid.addWidget(self.sacKalinlikGirdi, 0, 1)
        grid.addWidget(QLabel("mm"), 0, 2)
        grid.addWidget(self.kesmeUzunlukLabel, 0, 3)
        grid.addWidget(self.kesmeUzunlukGirdi, 0, 4)
        grid.addWidget(QLabel("mm"), 0, 5)
        grid.addWidget(self.kesmeMukavemetLabel, 1, 0)
        grid.addWidget(self.kesmeMukavemetGirdi, 1, 1)
        grid.addWidget(QLabel("kg/mm²"), 1, 2)
        grid.addWidget(self.ayirmaKuvetOranLabel, 1, 3)
        grid.addWidget(self.ayirmaKuvetOranGirdi, 1, 4)
        grid.addWidget(QLabel("%"), 1, 5)
        #grid.addWidget(self.hesapButon, 2, 0, 1, 6)

        butonLayout = QHBoxLayout()
        butonLayout.addStretch()
        butonLayout.addWidget(self.hesapButon)
        butonLayout.addStretch()


        self.toplamKuvvetKG = QLabel(alignment=Qt.AlignRight)
        self.toplamKuvvetKG.setStyleSheet(self.styleSheetAl("green"))
        self.toplamKuvvetTON = QLabel(alignment=Qt.AlignRight)
        self.toplamKuvvetTON.setStyleSheet(self.styleSheetAl())
        #self.toplamKuvvetN = QLabel(alignment=Qt.AlignRight)

        toplamKuvvetGrid = QGridLayout()
        toplamKuvvetGrid.addWidget(QLabel(text="Toplam Kuvvet", alignment=Qt.AlignCenter), 0, 0, 1, 3)
        toplamKuvvetGrid.addWidget(self.toplamKuvvetTON, 1, 0, 1, 2)
        toplamKuvvetGrid.addWidget(QLabel(text="ton", alignment=Qt.AlignLeft), 1, 2)
        toplamKuvvetGrid.addWidget(self.toplamKuvvetKG, 2, 0, 1, 2)
        toplamKuvvetGrid.addWidget(QLabel(text="kg", alignment=Qt.AlignLeft), 2, 2)
        toplamKuvvetGrid.addWidget(QLabel(), 3, 0, 1, 3)
        #toplamKuvvetGrid.addWidget(self.toplamKuvvetN, 3, 0, 1, 2)
        #toplamKuvvetGrid.addWidget(QLabel(text="N", alignment=Qt.AlignLeft), 3, 2)


        self.karsiYayKuvvetN = QLabel()
        self.karsiYayKuvvetN.setStyleSheet(self.styleSheetAl("blue"))
        self.karsiYayKuvvetKG = QLabel()
        self.karsiYayKuvvetKG.setStyleSheet(self.styleSheetAl("green"))
        self.karsiYayKuvvetTON = QLabel(alignment=Qt.AlignRight)
        self.karsiYayKuvvetTON.setStyleSheet(self.styleSheetAl())

        self.yayBol1 = QLineEdit(maxLength=3, maximumWidth=32, alignment=Qt.AlignCenter)
        self.yayBol1.setValidator(intValidator)
        self.yayBol1.textChanged.connect(lambda:self.yayBolHesap(1))

        self.yayBolSonuc1 = QLabel()
        self.yayBolSonuc1.setStyleSheet(self.styleSheetAl("blue"))

        yayBolBox1 = QHBoxLayout()
        yayBolBox1.addStretch()
        yayBolBox1.addWidget(self.karsiYayKuvvetN)
        yayBolBox1.addWidget(QLabel("/"))
        yayBolBox1.addWidget(self.yayBol1)
        yayBolBox1.addWidget(QLabel("="))
        yayBolBox1.addWidget(self.yayBolSonuc1)
        yayBolBox1.addStretch()

        self.yayBol2 = QLineEdit(maxLength=3, maximumWidth=32, alignment=Qt.AlignCenter)
        self.yayBol2.setValidator(intValidator)
        self.yayBol2.textChanged.connect(lambda:self.yayBolHesap(2))

        self.yayBolSonuc2 = QLabel()
        self.yayBolSonuc2.setStyleSheet(self.styleSheetAl("green"))

        yayBolBox2 = QHBoxLayout()
        yayBolBox2.addStretch()
        yayBolBox2.addWidget(self.karsiYayKuvvetKG)
        yayBolBox2.addWidget(QLabel("/"))
        yayBolBox2.addWidget(self.yayBol2)
        yayBolBox2.addWidget(QLabel("="))
        yayBolBox2.addWidget(self.yayBolSonuc2)
        yayBolBox2.addStretch()

        karsiYayKuvvetGrid = QGridLayout()
        karsiYayKuvvetGrid.addWidget(QLabel(text="Sıyırma Kuvveti", alignment=Qt.AlignCenter), 0, 0, 1, 3)
        karsiYayKuvvetGrid.addWidget(self.karsiYayKuvvetTON, 1, 0, 1, 2)
        karsiYayKuvvetGrid.addWidget(QLabel(text="ton", alignment=Qt.AlignLeft), 1, 2)
        karsiYayKuvvetGrid.addLayout(yayBolBox2, 2, 0, 1, 3)
        #karsiYayKuvvetGrid.addWidget(self.karsiYayKuvvetKG, 2, 0, 1, 2)
        #karsiYayKuvvetGrid.addWidget(QLabel(text="kg", alignment=Qt.AlignLeft), 2, 2)
        karsiYayKuvvetGrid.addLayout(yayBolBox1, 3, 0, 1, 3)
        #karsiYayKuvvetGrid.addWidget(self.karsiYayKuvvetN, 3, 0, 1, 2)
        #karsiYayKuvvetGrid.addWidget(QLabel(text="N", alignment=Qt.AlignLeft), 3, 2)


        self.presKuvvetKG = QLabel(alignment=Qt.AlignRight)
        self.presKuvvetKG.setStyleSheet(self.styleSheetAl("green"))
        self.presKuvvetTON = QLabel(alignment=Qt.AlignRight)
        self.presKuvvetTON.setStyleSheet(self.styleSheetAl())
        #self.presKuvvetN = QLabel(alignment=Qt.AlignRight)

        presKuvvetGrid = QGridLayout()
        presKuvvetGrid.addWidget(QLabel(text="Pres Kuvveti", alignment=Qt.AlignCenter), 0, 0, 1, 3)
        presKuvvetGrid.addWidget(self.presKuvvetTON, 1, 0, 1, 2)
        presKuvvetGrid.addWidget(QLabel(text="ton", alignment=Qt.AlignLeft), 1, 2)
        presKuvvetGrid.addWidget(self.presKuvvetKG, 2, 0, 1, 2)
        presKuvvetGrid.addWidget(QLabel(text="kg", alignment=Qt.AlignLeft), 2, 2)
        presKuvvetGrid.addWidget(QLabel(), 3, 0, 1, 3)
        #presKuvvetGrid.addWidget(self.presKuvvetN, 3, 0, 1, 2)
        #presKuvvetGrid.addWidget(QLabel(text="N", alignment=Qt.AlignLeft), 3, 2)


        gizli = QHBoxLayout()
        gizli.addStretch()
        gizli.addLayout(toplamKuvvetGrid)
        gizli.addStretch()
        gizli.addLayout(karsiYayKuvvetGrid)
        gizli.addStretch()
        gizli.addLayout(presKuvvetGrid)
        gizli.addStretch()

        gizliv = QVBoxLayout()
        gizliv.addLayout(gizli)
        #gizliv.addLayout(yayBolBox1)

        self.frame = QFrame()
        self.frame.setLayout(gizliv)
        frameFont = QFont()
        frameFont.setPointSize(12)
        self.frame.setFont(frameFont)
        self.frame.hide()

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(grid)
        vbox.addLayout(butonLayout)
        vbox.addWidget(self.frame)
        vbox.addStretch()

        self.setLayout(vbox)
    
    def kesmeMukavemetGirdiDegisti(self, index):
        if index == self.OZEL_GIRDI_INDEX:
            girdi, onay = QInputDialog.getDouble(self, self.OZEL_GIRDI_KEY, "Kesme Mukavemeti:", self.AYIRMA_KUVVET_ORAN_TABLO[self.OZEL_GIRDI_KEY], 0.1)
            if onay:
                self.AYIRMA_KUVVET_ORAN_TABLO[self.OZEL_GIRDI_KEY] = girdi
                self.kesmeMukavemetGirdi.removeItem(self.OZEL_GIRDI_INDEX)
                self.kesmeMukavemetGirdi.addItem(self.OZEL_GIRDI_KEY+" ("+str(girdi)+") ")
                self.kesmeMukavemetGirdi.setCurrentIndex(self.OZEL_GIRDI_INDEX)

    def hesapla(self):
        sacKalinlik = self.sacKalinlikGirdi.text().strip()
        kesmeUzunluk = self.kesmeUzunlukGirdi.text().strip()
        kesmeMukavemet = list(self.AYIRMA_KUVVET_ORAN_TABLO.values())[self.kesmeMukavemetGirdi.currentIndex()]
        ayirmaKuvetOran = self.ayirmaKuvetOranGirdi.text().strip()

        if not sacKalinlik or not kesmeUzunluk or not kesmeMukavemet or not ayirmaKuvetOran:
            QMessageBox.critical(self, "Hata", "Tüm kutucuklar doldurulmalıdır.", QMessageBox.Ok)
        else:
            try:
                sacKalinlik = float(sacKalinlik)
                kesmeUzunluk = float(kesmeUzunluk)
                kesmeMukavemet = float(kesmeMukavemet)
                ayirmaKuvetOran = float(ayirmaKuvetOran)

                toplamKuvvetKG = kesmeMukavemet * sacKalinlik * kesmeUzunluk
                toplamKuvvetTON = toplamKuvvetKG / 1000.0
                #toplamKuvvetN = toplamKuvvetKG * self.YERCEKIMI_IVMESI
                toplamKuvvetKG = round(toplamKuvvetKG, 1)
                toplamKuvvetTON = round(toplamKuvvetTON, 1)

                self.toplamKuvvetKG.setText(str(toplamKuvvetKG))
                self.toplamKuvvetTON.setText(str(toplamKuvvetTON))
                #self.toplamKuvvetN.setText(str(toplamKuvvetN))

                self.karsiYayKuvvetKGDeger = toplamKuvvetKG * ayirmaKuvetOran / 100.0
                karsiYayKuvvetTON = self.karsiYayKuvvetKGDeger / 1000.0
                self.karsiYayKuvvetNDeger = self.karsiYayKuvvetKGDeger * self.YERCEKIMI_IVMESI
                self.karsiYayKuvvetKGDeger = round(self.karsiYayKuvvetKGDeger, 1)
                karsiYayKuvvetTON = round(karsiYayKuvvetTON, 1)
                self.karsiYayKuvvetNDeger = round(self.karsiYayKuvvetNDeger, 1)

                self.karsiYayKuvvetKG.setText(str(self.karsiYayKuvvetKGDeger)+"  kg")
                self.karsiYayKuvvetTON.setText(str(karsiYayKuvvetTON))
                self.karsiYayKuvvetN.setText(str(self.karsiYayKuvvetNDeger)+"  N")

                presKuvvetKG = self.karsiYayKuvvetKGDeger + toplamKuvvetKG
                presKuvvetTON = presKuvvetKG / 1000.0
                #presKuvvetN = presKuvvetKG * self.YERCEKIMI_IVMESI
                presKuvvetKG = round(presKuvvetKG, 1)
                presKuvvetTON = round(presKuvvetTON, 1)

                self.presKuvvetKG.setText(str(presKuvvetKG))
                self.presKuvvetTON.setText(str(presKuvvetTON))
                #self.presKuvvetN.setText(str(presKuvvetN))
                self.yayBolHesap()
                self.frame.show()
            except (ValueError):
                self.frame.hide()
                QMessageBox.critical(self, "Hata", "Hatalı girdi girdiniz. Ondalıklı sayıları \".\" (nokta) ile belirtiniz.")
    
    def yayBolHesap(self, girdi=1):
        if girdi == 1:
            self.yayBol2.setText(self.yayBol1.text())
        elif girdi == 2:
            self.yayBol1.setText(self.yayBol2.text())
        try:
            self.yayBolSonuc1.setText(str(round(self.karsiYayKuvvetNDeger / float(self.yayBol1.text()), 1))+"  N")
            self.yayBolSonuc2.setText(str(round(self.karsiYayKuvvetKGDeger / float(self.yayBol2.text()), 1))+"  kg")
        except (ValueError, ZeroDivisionError):
            self.yayBolSonuc1.setText("")
            self.yayBolSonuc2.setText("")
    
    def styleSheetAl(self, renk="red", punto="13"):
        return "QLabel { color : "+renk+"; font-size: "+punto+"pt; font-weight: bold }"