from email.charset import QP
import os, sys, time
from PIL import ImageFont, ImageDraw, Image
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QLineEdit,
    QScrollArea)
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
        self.framing(f"{dirpath}{filename}.jpg")
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


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.root = "/home/milk/视频/material-epg/zdk"
        self.piclist = []
        self.picdir = ""
        self.file = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("demo")
        self.resize(2200, 800)

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
        self.plabel.resize(720, 560)
        self.plabel.move(1460, 100)
        self.plabel2 = QLabel(self)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(160, 50, 120, 30)
        self.textbox.setValidator(QIntValidator())

        scroll = QScrollArea(self)
        scroll.setWidget(self.plabel2)
        scroll.setGeometry(10, 100, 1440, 680)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_D:
            index = self.piclist.index(self.file)
            self.file = self.piclist[index+1]
            pixmap = QPixmap(os.path.join(self.picdir, self.file))
            self.plabel.setPixmap(pixmap)
            self.setWindowTitle(self.file)
        if a0.key() == Qt.Key.Key_S:
            index = self.piclist.index(self.file)
            self.file = self.piclist[index-1]
            pixmap = QPixmap(os.path.join(self.picdir, self.file))
            self.plabel.setPixmap(pixmap)
            self.setWindowTitle(self.file)
        if a0.key() == Qt.Key.Key_C:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.file.split(".")[0])
        return super().keyPressEvent(a0)

    def jumpPage(self):
        filename = self.textbox.text()
        if not filename:
            filename = "1"
        self.file = f"{filename}.jpg"
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap)
        self.setWindowTitle(self.file)

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

    def openDir(self):
        self.picdir = QFileDialog.getExistingDirectory(self, "选取图片文件夹", self.root)
        if not self.picdir:
            return
        self.piclist = os.listdir(self.picdir)
        self.piclist.sort(key=lambda x: int(x.split(".")[0]))
        self.file = self.piclist[0]
        pixmap = QPixmap(os.path.join(self.picdir, self.file))
        self.plabel.setPixmap(pixmap)

        pixmap2 = QPixmap("%s/2-%s.jpg"%(self.picdir.rsplit("/", 1)[0], self.picdir.rsplit("/", 1)[1]))
        self.plabel2.setPixmap(pixmap2)
        self.plabel2.adjustSize()

        self.setWindowTitle(self.file)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
