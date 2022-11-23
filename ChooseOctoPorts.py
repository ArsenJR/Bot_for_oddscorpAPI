from AllLibraries import *
from OctoAPI import *
import OctoAPI

class ChoosePortOcto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор порта Octo")
        self.setFixedSize(1200, 700)

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

        # слой для списка порта для pinnacle
        pinnacle_port_layout = QVBoxLayout()

        self.pinnacle_label = QLabel(' Порт для Pinnacle: ')
        self.pinnacle_label.setFont(font)
        pinnacle_port_layout.addWidget(self.pinnacle_label)

        self.pinnacle_listView = QtWidgets.QListView()
        self.pinnacle_model = QtGui.QStandardItemModel()
        self.pinnacle_listView.setModel(self.pinnacle_model)
        self.pinnacle_listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        pinnacle_port_layout.addWidget(self.pinnacle_listView)

        layout.addLayout(pinnacle_port_layout, 0, 0)

        # разделительное расстаяние
        layout.addWidget(QLabel('     '), 0, 1)

        # слой для списка порта для ggbet
        ggbet_layout = QVBoxLayout()

        self.ggbet_label = QLabel(' Порт для Pinnacle: ')
        self.ggbet_label.setFont(font)
        ggbet_layout.addWidget(self.ggbet_label)

        self.ggbet_listView = QtWidgets.QListView()
        self.ggbet_model = QtGui.QStandardItemModel()
        self.ggbet_listView.setModel(self.ggbet_model)
        self.ggbet_listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        ggbet_layout.addWidget(self.ggbet_listView)

        layout.addLayout(ggbet_layout, 0, 2)

        layout_with_btn = QHBoxLayout()
        self.btn_save_ports = QPushButton('Сохранить')
        self.btn_save_ports.setFixedWidth(110)
        self.btn_save_ports.clicked.connect(self.save_octo_ports)
        layout_with_btn.addWidget(QLabel('           '))
        layout_with_btn.addWidget(self.btn_save_ports)

        layout.addLayout(layout_with_btn, 1, 2)

        self.print_octo_profiles()

    def print_octo_profiles(self):

        self.pinnacle_model.removeRows(0, self.pinnacle_model.rowCount())
        self.ggbet_model.removeRows(0, self.ggbet_model.rowCount())
        self.pinnacle_model.appendRow(QtGui.QStandardItem('pinnacle port'))
        self.ggbet_model.appendRow(QtGui.QStandardItem('ggbet port'))
        self.pinnacle_model.appendRow(QtGui.QStandardItem('pinnacle second port'))
        self.ggbet_model.appendRow(QtGui.QStandardItem('ggbet второй port'))
        return
        # когда подключим окто, проверить и добавить заполнение двух листвью
        data = OctoAPI.get_octo_profiles(OctoAPI.OCTO_API_TOKEN)
        self.uuid_dict = {}
        for el in data['data']:
            if 'bk' in el['tags']:
                self.uuid_dict[el['title']] = el['uuid']
                self.model.appendRow(QtGui.QStandardItem(el['title']))

    def save_octo_ports(self):

        idx_selected_item_pinnacle = self.pinnacle_listView.selectionModel().selectedIndexes()
        idx_selected_item_ggbet = self.ggbet_listView.selectionModel().selectedIndexes()
        if idx_selected_item_pinnacle and idx_selected_item_ggbet:
            self.pinnacle_port_name = self.pinnacle_model.itemFromIndex(idx_selected_item_pinnacle[0]).text()
            self.ggbet_port_name = self.ggbet_model.itemFromIndex(idx_selected_item_ggbet[0]).text()
            self.accept()
        else:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите два порта.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChoosePortOcto()
    window.show()
    sys.exit(app.exec())


