from PyQt5.QtWidgets import (QApplication, QInputDialog, QLineEdit, QLineEdit, QListWidget, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup, QTextEdit, QFileDialog )
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter

app = QApplication([])
win = QWidget()

lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_chb = QPushButton('Ч/Б')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_r = QPushButton('Резкость')

win.resize(700,400)
win.setWindowTitle('Easy Editor')
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)

row_tool = QHBoxLayout()
row_tool.addWidget(btn_dir)
row_tool.addWidget(btn_chb)
row_tool.addWidget(btn_left)
row_tool.addWidget(btn_right)
row_tool.addWidget(btn_mirror)
row_tool.addWidget(btn_r)
col2.addLayout(row_tool)

row.addLayout(col1)
row.addLayout(col2)
win.setLayout(row)
win.show()
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

def filter(files, extensions):
    result = []
    for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
    return result

btn_dir.clicked.connect(showFilenamesList)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_rez(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir, workimage.filename )
        workimage.showImage(image_path)


workimage = ImageProcessor() 
lw_files.currentRowChanged.connect(showChosenImage)
btn_chb.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_right.clicked.connect(workimage.do_right)
btn_left.clicked.connect(workimage.do_left)
btn_r.clicked.connect(workimage.do_rez)
app.exec()
