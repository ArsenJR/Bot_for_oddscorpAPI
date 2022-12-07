from AllLibraries import *
from CommunSettings import AddConnect

class BKOrderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтр настроек")

        self.main_window = parent

        # общий слой
        layout = QGridLayout()
        self.setLayout(layout)

        # настраиваем шрифт
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.list_name = QLabel(' Порядок проставления: ')
        self.list_name.setFont(font)
        layout.addWidget(self.list_name, 0, 0)

        self.ruls_list = QtWidgets.QListView()
        #self.black_listView.setFixedWidth(500)
        #self.black_listView.setFixedHeight(400)
        self.ruls_list_model = QtGui.QStandardItemModel()
        self.ruls_list.setModel(self.ruls_list_model)
        self.ruls_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        layout.addWidget(self.ruls_list, 1, 0)

        layout.addWidget(QLabel('     '), 0, 1)

        btn_layout = QHBoxLayout()

        # btn add
        self.btn_add = QPushButton()
        self.btn_add.setIcon(QtGui.QIcon('icons/plus.png'))
        self.btn_add.setIconSize(QtCore.QSize(48, 48))
        self.btn_add.setFixedWidth(80)
        self.btn_add.clicked.connect(self.add_ruel_to_list)

        self.btn_delete = QPushButton()
        self.btn_delete.setIcon(QtGui.QIcon('icons/minus.png'))
        self.btn_delete.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete.setFixedWidth(80)
        self.btn_delete.clicked.connect(self.delete_str_from_list)

        self.btn_delete_all = QPushButton()
        self.btn_delete_all.setIcon(QtGui.QIcon('icons/delete all.png'))
        self.btn_delete_all.setIconSize(QtCore.QSize(48, 48))
        self.btn_delete_all.setFixedWidth(80)
        self.btn_delete_all.clicked.connect(self.delete_all_from_list)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_delete_all)

        layout.addLayout(btn_layout, 1, 2)

        self.save_settings_btn = QPushButton('Сохранить')
        self.save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_btn, 2, 2)


    def save_settings(self):

        self.is_settings_saved = False

        list_ruels = []
        for i in range(self.ruls_list_model.rowCount()):
            list_ruels.append(self.ruls_list_model.item(i).text())

        if not list_ruels:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Добавьте правло проставления.')
            return

        self.ruels_dict = {}
        for ruel in list_ruels:
            dict_warp = ruel.replace('-', '').replace('>', '').replace('  ', ' ').split(' ')
            if len(dict_warp) == 3:
                if dict_warp[2] != 'сбой':
                    self.ruels_dict[dict_warp[0]+ ' - ' + dict_warp[1]] = dict_warp[2]
                else:
                    self.ruels_dict[dict_warp[0] + ' - ' + dict_warp[1]] = 'None'
            else:
                self.ruels_dict[dict_warp[0] + ' - ' + dict_warp[1]] = 'None'

        self.report = QMessageBox.information(self, "Успех", "Данные успешно сохранены")
        self.is_settings_saved = True
        self.main_window.save_order_ruels()
        return


    def add_ruel_to_list(self):

        self.dialod_creat_ruels = AddConnect(self)
        if self.dialod_creat_ruels.exec():
            connect_type = self.dialod_creat_ruels.connect_type
            first_bk = self.dialod_creat_ruels.first_bk_name
            second_bk = self.dialod_creat_ruels.second_bk_name

            connect_name = 'сбой'
            if connect_type == 1:
                connect_name = first_bk
            if connect_type == 2:
                connect_name = second_bk
            if connect_type == 3:
                connect_name = 'не ставить'

            self.ruls_list_model.appendRow(QtGui.QStandardItem(first_bk+' - '+second_bk+' ---> '+connect_name))

        return


    def delete_str_from_list(self):
        try:
            idx = self.ruls_list.selectionModel().selectedRows()[0]
        except:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите строку.')
            return

        self.ruls_list_model.removeRow(idx.row())




    def delete_all_from_list(self):
        self.ruls_list_model.removeRows(0, self.ruls_list_model.rowCount())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BKOrderWidget()
    window.show()
    sys.exit(app.exec())


