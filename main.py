import os, sys, time, typing
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QLineEdit,
    QScrollArea, QComboBox, QTextEdit)
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ThreadWorker(QThread):
    sig = pyqtSignal()

    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath
        self.root = "/home/milk/视频/material-epg/zdk"

    def run(self):
        filename = self.filepath.split("/")[-1].split(".")[0]
        dirpath = f"{self.root}/videos/"
        command = f'mkdir {dirpath}{filename};ffmpeg -y -i {dirpath}{filename}.mp4 -f image2 -r 25 -q:v 2 {dirpath}{filename}/%d.jpg;ffmpeg -y -i {dirpath}{filename}.mp4 -vf "fps=1/5,scale=iw/4:-1,tile=8x90" {dirpath}{filename}.jpg'
        os.system(command)
        # self.framing(f"{dirpath}{filename}.jpg")
        self.sig.emit()

    def framing(self, fileName):
        image = Image.open(fileName)
        width, height = image.size
        perw = width / 8
        perh = height / 90
        font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 50)
        draw = ImageDraw.Draw(image)
        for i in range(8):
            for j in range(90):
                draw.text((i*perw, j*perh), str((i*5+j*5*8)*25+63), font=font, fill="#a20808")
        image.save("%s/2-%s"%(fileName.rsplit("/", 1)[0], fileName.rsplit("/", 1)[1]))


class MainScroll(QScrollArea):
    sig = pyqtSignal(float)

    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.buttons() == Qt.MouseButton.LeftButton:
            height, width = self.children()[0].children()[0].height(), self.children()[0].children()[0].width()
            per_x, per_y = width / 8, height / 90
            if width > 100:
                cx, cy = a0.localPos().x(), self.verticalScrollBar().value() + a0.localPos().y()
                px, py = cx // per_x, cy // per_y
                pidx = (px * 5 + py * 5 * 8) *25 + 63
                self.sig.emit(pidx)
        return super().mousePressEvent(a0)


class ClickLabel(QLabel):
    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.buttons() == Qt.MouseButton.LeftButton:
            self.sig.emit(self.filename)
        return super().mousePressEvent(ev)

    def setPixmap(self, a0: QtGui.QPixmap, filename: str) -> None:
        self.filename = filename
        return super().setPixmap(a0)


class ClickLabel2(QLabel):
    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.buttons() == Qt.MouseButton.LeftButton:
            self.sig.emit(self.filename)
        return super().mousePressEvent(ev)

    def setPixmap(self, a0: QtGui.QPixmap, filename: str) -> None:
        self.filename = filename
        return super().setPixmap(a0)


class ClickLabel3(QLabel):
    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.buttons() == Qt.MouseButton.LeftButton:
            self.sig.emit(self.filename)
        return super().mousePressEvent(ev)

    def setPixmap(self, a0: QtGui.QPixmap, filename: str) -> None:
        self.filename = filename
        return super().setPixmap(a0)


class DataLabel(QLabel):

    def __init__(self, dot, name, parent=None):
        self.dot = dot
        self.name = name
        super().__init__(parent)


class EnterLineEdit(QLineEdit):
    jump = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Return:
            self.jump.emit()
        return super().keyPressEvent(a0)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.root = "/home/milk/视频/material-epg/zdk"
        self.piclist = []
        self.picdir = ""
        self.file = ""
        self.datalist = []
        self.nameList = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("demo")
        self.resize(2200, 1000)

        self.button1 = QPushButton("视频分帧", self)
        self.button1.setGeometry(20, 10, 90, 30)
        self.button1.clicked.connect(self.openFile)
        self.button2 = QPushButton("选择图片文件夹", self)
        self.button2.setGeometry(20, 50, 120, 30)
        self.button2.clicked.connect(self.openDir)
        self.button3 = QPushButton("跳转", self)
        self.button3.setGeometry(300, 50, 50, 30)
        self.button3.clicked.connect(self.jumpPage)

        self.label1 = QLabel(self)
        self.label1.move(120, 15)
        self.label2 = QLabel(self)
        self.label2.move(600, 15)
        self.plabel = QLabel(self)
        self.plabel.move(1460, 90)
        self.plabel2 = QLabel(self)

        self.flabel1 = ClickLabel(self)
        self.flabel1.move(10, 780)
        self.flabel1.sig.connect(self.setPicH)
        self.flabel2 = ClickLabel(self)
        self.flabel2.move(10+370, 780)
        self.flabel2.sig.connect(self.setPicH)
        self.flabel3 = ClickLabel(self)
        self.flabel3.move(10+370*2, 780)
        self.flabel3.sig.connect(self.setPicH)
        self.flabel4 = ClickLabel(self)
        self.flabel4.move(10+370*3, 780)
        self.flabel4.sig.connect(self.setPicH)
        self.flabel5 = ClickLabel(self)
        self.flabel5.move(10+370*4, 780)
        self.flabel5.sig.connect(self.setPicH)

        self.hlabel1 = ClickLabel2(self)
        self.hlabel1.move(10, 780+210)
        self.hlabel1.sig.connect(self.setPicG)
        self.hlabel2 = ClickLabel2(self)
        self.hlabel2.move(10+370, 780+210)
        self.hlabel2.sig.connect(self.setPicG)
        self.hlabel3 = ClickLabel2(self)
        self.hlabel3.move(10+370*2, 780+210)
        self.hlabel3.sig.connect(self.setPicG)
        self.hlabel4 = ClickLabel2(self)
        self.hlabel4.move(10+370*3, 780+210)
        self.hlabel4.sig.connect(self.setPicG)
        self.hlabel5 = ClickLabel2(self)
        self.hlabel5.move(10+370*4, 780+210)
        self.hlabel5.sig.connect(self.setPicG)

        self.glabel1 = ClickLabel3(self)
        self.glabel1.move(10, 780+210*2)
        self.glabel1.sig.connect(self.setPicR)
        self.glabel2 = ClickLabel3(self)
        self.glabel2.move(10+370, 780+210*2)
        self.glabel2.sig.connect(self.setPicR)
        self.glabel3 = ClickLabel3(self)
        self.glabel3.move(10+370*2, 780+210*2)
        self.glabel3.sig.connect(self.setPicR)
        self.glabel4 = ClickLabel3(self)
        self.glabel4.move(10+370*3, 780+210*2)
        self.glabel4.sig.connect(self.setPicR)
        self.glabel5 = ClickLabel3(self)
        self.glabel5.move(10+370*4, 780+210*2)
        self.glabel5.sig.connect(self.setPicR)

        self.textbox = EnterLineEdit(self)
        self.textbox.setGeometry(160, 50, 120, 30)
        self.textbox.setValidator(QIntValidator())
        self.textbox.jump.connect(self.jumpPage)

        self.mscroll = MainScroll(self)
        self.mscroll.setWidget(self.plabel2)
        self.mscroll.setGeometry(10, 90, 1440, 680)
        self.mscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mscroll.sig.connect(self.setPicF)

        win1 = QWidget(self)
        vbox = QVBoxLayout(win1)
        hbox = QHBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.textwin = QTextEdit()
        self.textwin.setReadOnly(True)
        self.vbox2.addWidget(self.textwin)
        # self.vbox2.addStretch(1)
        self.slabel = QLabel("")
        self.tbutton = QPushButton("确定")
        self.tbutton.clicked.connect(self.addEle)
        self.combo = QComboBox()
        self.combo.addItems(self.nameList)
        self.combo.setEditable(True)
        self.combo.setCurrentText("")
        hbox.addWidget(self.slabel)
        hbox.addWidget(self.combo)
        # hbox.addStretch(1)
        hbox.addWidget(self.tbutton)
        # hbox.setStretch(0, 2)
        hbox.setStretch(1, 16)
        hbox.setStretch(2, 4)
        # hbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addLayout(self.vbox2)
        vbox.addStretch(1)
        vbox.setStretch(0, 1)
        vbox.setStretch(1, 9)
        # vbox.addWidget(self.slabel, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # vbox.addWidget(combo)
        # vbox.addWidget(button, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        win1.setGeometry(10+370*5, 780, 400, 600)
        # win1.setStyleSheet("border: 1px solid black;")

        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self.file:
            return super().keyPressEvent(a0)
        if a0.key() == Qt.Key.Key_D:
            index = self.piclist.index(self.file)
            self.file = self.piclist[index+1]
            pixmap = QPixmap(os.path.join(self.picdir, self.file))
            self.plabel.setPixmap(pixmap.scaledToWidth(720))
            self.setWindowTitle(self.file)
        if a0.key() == Qt.Key.Key_S:
            index = self.piclist.index(self.file)
            self.file = self.piclist[index-1]
            pixmap = QPixmap(os.path.join(self.picdir, self.file))
            self.plabel.setPixmap(pixmap.scaledToWidth(720))
            self.setWindowTitle(self.file)
        if a0.key() == Qt.Key.Key_C:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.file.split(".")[0])
        return super().keyPressEvent(a0)

    def jumpPage(self):
        self.textbox.clearFocus()
        filename = self.textbox.text()
        # self.textbox.clear()
        if not filename:
            filename = "1"
        self.file = f"{filename}.jpg"
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))

        self.setWindowTitle(self.file)

    def addEle(self):
        self.datalist.append((self.file.split(".")[0], self.combo.currentText()))
        if self.combo.currentText() not in self.nameList:
            self.nameList.append(self.combo.currentText())
            self.combo.addItem(self.combo.currentText())
        self.textwin.setText("\n".join(["%s %s"%ele for ele in self.datalist]))


    def openFile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选取视频文件", self.root, "*.mp4")
        if not filepath:
            return
        self.label1.setText(filepath)
        self.label1.adjustSize()
        self.thread = ThreadWorker(filepath)
        self.thread.sig.connect(self.handleFinish)
        self.thread.start()

    def handleFinish(self):
        self.label2.setText("完成")
        self.label2.adjustSize()

    def setPicF(self, pidx):
        self.file = f"{int(pidx)}.jpg"
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))

        fpixmap1 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-100]))
        self.flabel1.setPixmap(fpixmap1.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-100])
        self.flabel1.adjustSize()
        fpixmap2 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-75]))
        self.flabel2.setPixmap(fpixmap2.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-75])
        self.flabel2.adjustSize()
        fpixmap3 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-50]))
        self.flabel3.setPixmap(fpixmap3.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-50])
        self.flabel3.adjustSize()
        fpixmap4 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-25]))
        self.flabel4.setPixmap(fpixmap4.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-25])
        self.flabel4.adjustSize()
        fpixmap5 = QPixmap(os.path.join(self.picdir, self.file))
        self.flabel5.setPixmap(fpixmap5.scaledToHeight(200), self.file)
        self.flabel5.adjustSize()

        self.setWindowTitle(self.file)

    def setPicH(self, filename):
        self.file = filename
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))
        
        hpixmap1 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-20]))
        self.hlabel1.setPixmap(hpixmap1.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-20])
        self.hlabel1.adjustSize()
        hpixmap2 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-15]))
        self.hlabel2.setPixmap(hpixmap2.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-15])
        self.hlabel2.adjustSize()
        hpixmap3 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-10]))
        self.hlabel3.setPixmap(hpixmap3.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-10])
        self.hlabel3.adjustSize()
        hpixmap4 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-5]))
        self.hlabel4.setPixmap(hpixmap4.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-5])
        self.hlabel4.adjustSize()
        hpixmap5 = QPixmap(os.path.join(self.picdir, self.file))
        self.hlabel5.setPixmap(hpixmap5.scaledToHeight(200), self.file)
        self.hlabel5.adjustSize()

        self.setWindowTitle(self.file)

    def setPicG(self, filename):
        self.file = filename
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))
        
        gpixmap1 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-4]))
        self.glabel1.setPixmap(gpixmap1.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-4])
        self.glabel1.adjustSize()
        gpixmap2 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-3]))
        self.glabel2.setPixmap(gpixmap2.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-3])
        self.glabel2.adjustSize()
        gpixmap3 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-2]))
        self.glabel3.setPixmap(gpixmap3.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-2])
        self.glabel3.adjustSize()
        gpixmap4 = QPixmap(os.path.join(self.picdir, self.piclist[self.piclist.index(self.file)-1]))
        self.glabel4.setPixmap(gpixmap4.scaledToHeight(200), self.piclist[self.piclist.index(self.file)-1])
        self.glabel4.adjustSize()
        gpixmap5 = QPixmap(os.path.join(self.picdir, self.file))
        self.glabel5.setPixmap(gpixmap5.scaledToHeight(200), self.file)
        self.glabel5.adjustSize()

        self.setWindowTitle(self.file)

    def setPicR(self, filename):
        self.file = filename
        framenum = filename.split(".")[0]
        dot = datetime.strptime("2022-10-15 02:59:35", "%Y-%m-%d %H:%M:%S").timestamp() + round(int(framenum)/25, 2)
        dtime = datetime.fromtimestamp(dot).strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        self.slabel.setText(dtime)
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))

        self.setWindowTitle(self.file)

    def openDir(self):
        self.picdir = QFileDialog.getExistingDirectory(self, "选取图片文件夹", self.root)
        if not self.picdir:
            return
        self.piclist = os.listdir(self.picdir)
        self.piclist.sort(key=lambda x: int(x.split(".")[0]))
        self.file = self.piclist[0]
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap.scaledToWidth(720))
        self.plabel.adjustSize()

        pixmap2 = QPixmap("%s/%s.jpg"%(self.picdir.rsplit("/", 1)[0], self.picdir.rsplit("/", 1)[1]))
        self.plabel2.setPixmap(pixmap2.scaledToWidth(1440))
        self.plabel2.adjustSize()

        self.mscroll.verticalScrollBar().setValue(0)
        self.setWindowTitle(self.file)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
