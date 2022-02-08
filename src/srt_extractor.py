import sys, os

from PyQt5 import QtWidgets, QtCore, QtGui
import qdarkstyle

from helper_functions import has_srt, extract_srt, system
from gui import Ui_Form
from config import *

def makefolders(folders):
  for folder in folders:
    if not os.path.isdir(folder):
      os.mkdir(folder)

init_folders = lambda: makefolders(default_folders)

class MyWindow(QtWidgets.QWidget):

    def __init__(self):
      super(MyWindow, self).__init__()
      self.ui = Ui_Form() 
      self.ui.setupUi(self)
      #self.showMaximized()
      self.ui.tableWidget.setAcceptDrops(True)
      self.ui.tableWidget.viewport().installEventFilter(self)
      types = ['text/uri-list']
      types.extend(self.ui.tableWidget.mimeTypes())
      self.ui.tableWidget.mimeTypes = lambda: types
      self.ui.btn_extract_srt.clicked.connect(self.extract_srt)
      self.ui.btn_open_srt.clicked.connect(self.open_srt)
      self.ui.btn_open_txt.clicked.connect(self.open_txt)

    def open_srt(self):
      system(f'explorer {output_folder_srt}')

    def open_txt(self):
      system(f'explorer {output_folder_txt}')

    def extract_srt(self):
      init_folders()
      cc = self.ui.tableWidget.columnCount()
      data = [i.data(0) for i in self.ui.tableWidget.selectedItems()]
      videos = data[::cc]
      videos_srt = data[1::cc]
      for vid, vid_srt in zip(videos, videos_srt):
        if vid_srt == "Sim":
          try:
            extract_srt(vid)
            self.ui.plainTextEdit.insertPlainText(f"Legenda extraída -> {vid}\n")
          except Exception as e:
            self.ui.plainTextEdit.insertPlainText(f"Erro -> {str(e)}\n")
        else:
          self.ui.plainTextEdit.insertPlainText(f"Não possui legenda -> {vid}\n")

    def eventFilter(self, source, event):
      if (event.type() == QtCore.QEvent.Drop and
        event.mimeData().hasUrls()):
        for url in event.mimeData().urls():
          print(url)
          self.addFile(url.toLocalFile())
      return super().eventFilter(source, event)

    def addFile(self, filepath):
      has_subtitle = 'Sim' if has_srt(filepath) else 'Não'

      self.insert_row(filepath, has_subtitle)
      for col in range(2):
        self.ui.tableWidget.resizeColumnToContents(col)

    def insert_row(self, *args):
      row_idx = self.ui.tableWidget.rowCount()
      tbl = self.ui.tableWidget
      tbl.insertRow(row_idx)
      for col_idx, arg in enumerate(args):
        tbl.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(arg))

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon('../icon.ico'))
application = MyWindow()
application.show()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
sys.exit(app.exec())