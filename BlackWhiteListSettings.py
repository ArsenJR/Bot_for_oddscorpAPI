from AllLibraries import *

class BlackWhiteList(QWidget):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтр настроек")

        self.main_window = parent

        self.is_settings_saved = False
        self.black_list_words = []
        self.white_list_words = []

        # общий слой
        layout = QGridLayout()
        self.setLayout(layout)

        # настраиваем шрифт
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        # слой для черного списка
        black_list_layout = QVBoxLayout()

        self.black_list_label = QLabel(' Черный список: ')
        self.black_list_label.setFont(font)
        black_list_layout.addWidget(self.black_list_label)

        # поле для ввода ключевых слов в черный лист
        self.txt_add_black_list = QLineEdit()
        self.txt_add_black_list.setFixedHeight(40)
        black_list_layout.addWidget(self.txt_add_black_list)

        # слой к кнопкам черного списка (плюс, минкс, убрать все)
        black_list_btn_layout = QHBoxLayout()
        self.btn_add_bl = QPushButton()
        self.btn_add_bl.setIcon(QtGui.QIcon('icons/plus.png'))
        self.btn_add_bl.setIconSize(QtCore.QSize(48, 48))
        self.btn_add_bl.setFixedWidth(80)
        self.btn_add_bl.clicked.connect(
            lambda: self.add_key_to_list(self.txt_add_black_list, self.black_list_model)
        )

        black_list_btn_layout.addWidget(self.btn_add_bl)

        self.btn_delete_bl = QPushButton()
        self.btn_delete_bl.setIcon(QtGui.QIcon('icons/minus.png'))
        self.btn_delete_bl.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete_bl.setFixedWidth(80)
        self.btn_delete_bl.clicked.connect(
            lambda: self.delete_str_from_list(self.black_listView, self.black_list_model)
        )

        black_list_btn_layout.addWidget(self.btn_delete_bl)

        self.btn_delete_all_bl = QPushButton()
        self.btn_delete_all_bl.setIcon(QtGui.QIcon('icons/delete all.png'))
        self.btn_delete_all_bl.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete_all_bl.setFixedWidth(80)
        self.btn_delete_all_bl.clicked.connect(
            lambda: self.delete_all_from_list(self.black_list_model)
        )
        black_list_btn_layout.addWidget(self.btn_delete_all_bl)
        black_list_layout.addLayout(black_list_btn_layout)

        self.black_listView = QtWidgets.QListView()
        self.black_listView.setFixedWidth(500)
        self.black_listView.setFixedHeight(400)
        self.black_list_model = QtGui.QStandardItemModel()
        self.black_listView.setModel(self.black_list_model)
        self.black_listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


        black_list_layout.addWidget(self.black_listView)

        layout.addLayout(black_list_layout, 0, 0)


        # разделительное расстаяние
        layout.addWidget(QLabel('                  '), 0, 1)

        # слой для белого списка
        white_list_layout = QVBoxLayout()

        self.white_list_label = QLabel(' Белый список: ')
        self.white_list_label.setFont(font)
        white_list_layout.addWidget(self.white_list_label)

        # поле для ввода ключевых слов в черный лист
        self.txt_add_white_list = QLineEdit()
        self.txt_add_white_list.setFixedHeight(40)
        white_list_layout.addWidget(self.txt_add_white_list)

        # слой к кнопкам white списка (плюс, минкс, убрать все)
        white_list_btn_layout = QHBoxLayout()
        self.btn_add_white = QPushButton()
        self.btn_add_white.setIcon(QtGui.QIcon('icons/plus.png'))
        self.btn_add_white.setIconSize(QtCore.QSize(48, 48))
        self.btn_add_white.setFixedWidth(80)
        self.btn_add_white.clicked.connect(
            lambda: self.add_key_to_list(self.txt_add_white_list, self.white_list_model)
        )
        white_list_btn_layout.addWidget(self.btn_add_white)

        self.btn_delete_white = QPushButton()
        self.btn_delete_white.setIcon(QtGui.QIcon('icons/minus.png'))
        self.btn_delete_white.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete_white.setFixedWidth(80)
        self.btn_delete_white.clicked.connect(
            lambda: self.delete_str_from_list(self.white_listView, self.white_list_model)
        )
        white_list_btn_layout.addWidget(self.btn_delete_white)

        self.btn_delete_all_white = QPushButton()
        self.btn_delete_all_white.setIcon(QtGui.QIcon('icons/delete all.png'))
        self.btn_delete_all_white.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete_all_white.setFixedWidth(80)
        self.btn_delete_all_white.clicked.connect(
            lambda: self.delete_all_from_list(self.white_list_model)
        )
        white_list_btn_layout.addWidget(self.btn_delete_all_white)
        white_list_layout.addLayout(white_list_btn_layout)

        self.white_listView = QtWidgets.QListView()
        self.white_listView.setFixedWidth(500)
        self.white_listView.setFixedHeight(400)
        self.white_list_model = QtGui.QStandardItemModel()
        self.white_listView.setModel(self.white_list_model)
        self.white_listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        white_list_layout.addWidget(self.white_listView)

        layout.addLayout(white_list_layout, 0,2)

        layout_with_btn = QHBoxLayout()
        self.btn_save_settings = QPushButton('Сохранить')
        self.btn_save_settings.setFixedWidth(110)
        self.btn_save_settings.clicked.connect(self.save_settings)
        layout_with_btn.addWidget(QLabel('           '))
        layout_with_btn.addWidget(self.btn_save_settings)

        layout.addLayout(layout_with_btn, 1, 2)

    def save_settings(self):

        self.is_settings_saved = False

        self.black_list_words = []
        for i in range(self.black_list_model.rowCount()):
            self.black_list_words.append(self.black_list_model.item(i).text())

        self.white_list_words = []
        for i in range(self.white_list_model.rowCount()):
            self.white_list_words.append((self.white_list_model.item(i).text()))

        self.report = QMessageBox.information(self, "Успех", "Данные успешно сохранены")
        self.is_settings_saved = True
        self.main_window.save_black_white_list()
        return


    def add_key_to_list(self, txt, model):
        text = txt.text()
        if text:
            model.appendRow(QtGui.QStandardItem(text))
            txt.setText('')
        else:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Введите текст для добавления в черный список')

    def delete_str_from_list(self, listview, model):

        try:
            idx = listview.selectionModel().selectedRows()[0]
        except:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите строку.')
            return

        model.removeRow(idx.row())




    def delete_all_from_list(self, model):

        model.removeRows(0, model.rowCount())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackWhiteList()
    window.show()
    sys.exit(app.exec())


