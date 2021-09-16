import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("netsuiteinvoice.ui", self)
        self.browse.clicked.connect(self.browse_files)
        self.upload.clicked.connect(self.upload_file)
        self.changenetsuite.clicked.connect(self.netsuite_path)

    def browse_files(self):
        file_name = QFileDialog.getOpenFileName(self, 'Upload Invoice', '')
        self.filename.setText(file_name[0])

    def upload_file(self):
        self.filename.clear()

    def netsuite_path(self):
        path = "ahthhhahthhahthhthalth"
        self.netsuiteedit.setText(path)


app = QApplication(sys.argv)
main_window = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_window)
widget.setFixedWidth(800)
widget.setFixedHeight(500)
widget.show()
sys.exit(app.exec_())
