import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPixmap


class MyWidget(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        uic.loadUi('calc.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.search)
        self.listWidgetItem = QListWidgetItem()


    def search(self):
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        if self.comboBox.currentText() == 'Автор':
            res = 'SELECT * FROM book WHERE author_name LIKE "{}%" '.format(self.lineEdit.text())
            self.result = cur.execute(res).fetchall()
        elif self.comboBox.currentText() == 'Название':
            res = 'SELECT * FROM book WHERE name LIKE "{}%" '.format(self.lineEdit.text())
            self.result = cur.execute(res).fetchall()
        for i in self.result:
            newButton = QPushButton(i[1], self)
            newButton.resize(100, 50)
            newButton.clicked.connect(lambda x: self.showSecond(newButton.text()))
            self.listWidgetItem.setSizeHint(newButton.sizeHint())
            self.listWidget.addItem(self.listWidgetItem)
            self.listWidget.setItemWidget(self.listWidgetItem, newButton)
            self.listWidget.scrollToItem(self.listWidgetItem)
        con.close()

    def showSecond(self, name):
        for i in self.result:
            if i[1] == name:
                self.result = i
                break
        self.second = SecondMain(i)
        self.second.show()


class SecondMain(QMainWindow):
    def __init__(self, root, **kwargs):
        super().__init__()
        uic.loadUi('calc_1.ui', self)
        self.root = root
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('notFound.jpg')
        self.label_9.setPixmap(pixmap)
        self.label_5.setText(str(self.root[1]))
        self.label_6.setText(str(self.root[2]))
        self.label_7.setText(str(self.root[3]))
        self.label_8.setText(str(self.root[4]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())