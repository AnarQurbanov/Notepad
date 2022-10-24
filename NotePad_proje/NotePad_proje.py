from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import * 
import sys,os

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()

        self.editor = QPlainTextEdit() #Yazi yazmamiz icin yer olusturur
        self.setCentralWidget(self.editor) #editoru pencereye gonderir

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont) #Yazi turunu,olcusunu degismekte yardimci oluyor.sistem fontlarini(yazi tiplerini) cagiriyor
        font.setPointSize(12) #Yaziya olcu veriyor
        self.editor.setFont(font) #Fontu editorun icine veriyor

        self.dosya_ad = None

        status = QStatusBar() #StatusBar (Altta bosluk alan) olusturur
        self.setStatusBar(status) #Olusturdugumuz statusbari Pencereye ekliyor

        tool = QToolBar() #ToolBar olusturur(ustte bosluk alan) 
        tool.setIconSize(QSize(30,30)) #ToolBara eklenen sekmelerin,objelerin boyutunu ayarliyoruz
        self.addToolBar(tool) #Olusturdugumuz toolbari pencereye ekliyor

        menubar = QMenuBar()
        menubar = self.menuBar() 
        dosya_menu = menubar.addMenu("Dosya") 
        ekle_menu = menubar.addMenu("Ekle")  

        dosya_ac = QAction(QIcon(os.path.join("dosya_ac.png")),"Dosya Aç",self) #QIcon(os.path.join()) ile action onune resim ekliyor
        dosya_ac.setStatusTip("Dışarıdan Bir Text Dosyasını NotePad'de Açmanızı Sağlar") #Statusbarda ne yazilacagini yaziyoruz
        dosya_ac.setShortcut("Ctrl+O")
        tool.addAction(dosya_ac)
        dosya_menu.addAction(dosya_ac) 

        kaydet = QAction(QIcon(os.path.join("kaydet.png")),"Kaydet",self)
        kaydet.setStatusTip("Girdiğiniz Notları txt Dosyası Olarak Kaydediyor") 
        kaydet.setShortcut("Ctrl+S") 
        tool.addAction(kaydet) 
        dosya_menu.addAction(kaydet) 

        farkli_kaydet = QAction(QIcon(os.path.join("farkli_kaydet.png")),"Farklı Kaydet",self)
        farkli_kaydet.setStatusTip("Girdiğiniz Notları Farklı Kaydetmemizi Sağlar") 
        tool.addAction(farkli_kaydet)
        dosya_menu.addAction(farkli_kaydet) 

        yazdir = QAction(QIcon(os.path.join("yazdir.png")),"Yazdır",self) 
        yazdir.setStatusTip("Dosyanı Yazdırmanızı Sağlar") 
        yazdir.setShortcut("Ctrl+P")
        dosya_menu.addAction(yazdir) 

        geri_al = QAction(QIcon(os.path.join("geri_al.png")),"Geri Al",self)
        geri_al.setStatusTip("Yaptığınız Son Değişikliği Geri Almanızı Sağlar") 
        geri_al.setShortcut("Ctrl+Z") 
        tool.addAction(geri_al) 
        ekle_menu.addAction(geri_al)  

        ileri_al = QAction(QIcon(os.path.join("ileri_al.png")),"İleri Al",self)
        ileri_al.setStatusTip("Geri Aldığınız Son İşlemi Tekrar Yapmanızı Sağlar") 
        ileri_al.setShortcut("Ctrl+Y") 
        tool.addAction(ileri_al) 
        ekle_menu.addAction(ileri_al)  

        kes = QAction(QIcon(os.path.join("kes.png")),"Kes",self)
        kes.setStatusTip("Seçtiğiniz Öğeleri Kesmenizi Sağlar") 
        kes.setShortcut("Ctrl+X") 
        tool.addAction(kes) 
        ekle_menu.addAction(kes) 

        kopyala = QAction(QIcon(os.path.join("kopyala.png")),"Kopyala",self)
        kopyala.setStatusTip("Seçtiğiniz Öğeleri Kopyalamanızı Sağlar") 
        kopyala.setShortcut("Ctrl+C") 
        tool.addAction(kopyala) 
        ekle_menu.addAction(kopyala) 

        yapistir = QAction(QIcon(os.path.join("yapistir.png")),"Yapıştır",self)
        yapistir.setStatusTip("Kopyaladığınız Öğeleri Yapştırmanızı Sağlar") 
        yapistir.setShortcut("Ctrl+V") 
        tool.addAction(yapistir) 
        ekle_menu.addAction(yapistir)  

        hepsini_sec = QAction(QIcon(os.path.join("hepsini_sec.png")),"Hepsini Seç",self)
        hepsini_sec.setStatusTip("Dosyanızda Bulunan Tüm Öğelerin Hepsini Seçmemizi Sağlar") 
        hepsini_sec.setShortcut("Ctrl+A") 
        tool.addAction(hepsini_sec) 
        ekle_menu.addAction(hepsini_sec) 

        dosya_ac.triggered.connect(self.dosya_ac_def) 
        kaydet.triggered.connect(self.kaydet_def) 
        farkli_kaydet.triggered.connect(self.farkli_kaydet_def) 
        yazdir.triggered.connect(self.yazdir_def)
        geri_al.triggered.connect(self.editor.undo) #editor isminde olusturdugumuz PlainTextin kendine ozel fonksiyonlari var
        ileri_al.triggered.connect(self.editor.redo) 
        kes.triggered.connect(self.editor.cut) 
        kopyala.triggered.connect(self.editor.copy) 
        yapistir.triggered.connect(self.editor.paste)
        hepsini_sec.triggered.connect(self.editor.selectAll)

        self.basligi_guncelle()
        self.setGeometry(100,100,500,500)
        self.show() 

    def basligi_guncelle(self) :
        self.setWindowTitle("{} - NotePad".format(os.path.basename(self.dosya_ad) if self.dosya_ad else "Untitled"))
        #os.path.basename() dosyanin adini string olarak yaziyor 

    def hata_mesaj(self,mesaj) :
        hata = QMessageBox() #Mesaj olusturur
        hata.setText(mesaj) 
        hata.setIcon(QMessageBox.critical) #critical ile carpi isaresi koyulur
        hata.show()

    def dosya_ac_def(self) :
        path,_ = QFileDialog.getOpenFileName(self,"Dosya Aç","","Text Dosyaları (*.txt)") #Dosya aciyor

        if path :
            try :
                with open(path,"r") as fp :
                    text = fp.read()  
            except Exception as e :
                self.hata_mesaj(e)
            else :
                self.editor.setPlainText(text) #Editorun icindeki yazilari silir ve text'i yazdirir 
                self.dosya_ad = path 
                self.basligi_guncelle()
            

    def kaydet_def(self) :
        if self.dosya_ad == None :
            return self.farkli_kaydet_def() 
        
        text = self.editor.toPlainText() 

        try :
            with open(self.dosya_ad,"w") as fp :
                fp.write(text)
        except Exception as e :
            self.hata_mesaj(e)
            

    def farkli_kaydet_def(self) :
        path , _= QFileDialog.getSaveFileName(self,"Farklı Kaydet","","Text Dosyaları (*.txt)") 
        #Dosyanin kaydedilmesini sagliyor.ilk once self,sonra cikacak olan pencereye isim veriyoruz,ucuncu dosya ismi girecegimiz yeri,sonda ise dosya turleri giriyoruz 
        #path demet donuyor ama path,_ yazdigimizda ise dosyaya verdigimiz isim path olarak ,string olarak donuyor

        text = self.editor.toPlainText() #editorun icindeki yazilari text seklinde kaydediyor

        if not path : #Eger dosya bossa bos return et ve fonksiyon sonlansin
            return   

        try :
            with open(path,"w") as fp : 
                fp.write(text)
        except Exception as e: #Surda olusan exceptionlarin tamamini e'ye atiyor
            self.hata_mesaj(e)
        else : #except blogu calismasa else calisacak
            self.dosya_ad = path 
            self.basligi_guncelle()
        
    def yazdir_def(self) :
        mesaj = QPrintDialog() #Bilgisayarin yazdirma islemi ekranina baglanacak 
        if mesaj.exec_() : #yazdir islemine bastiysa 
            self.editor.print_(mesaj.printer()) #kullanici yazdir butonuna bastiginda yazdirma islemi calisacak

if __name__ == "__main__" : 
    app = QApplication(sys.argv) 
    app.setApplicationName("NotePad") #Projeye isim verir

    window = MainWindow() 

    app.exec_()