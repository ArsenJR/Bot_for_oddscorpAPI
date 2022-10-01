from AllLibraries import *
from OctoAPI import *
import OctoAPI

LINK = ''
PORT = ''
class DialogToChoosePort(QDialog):
    def __init__(self, bk_name,parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"Choose port to {bk_name}")
        self.resize(1200, 600)

        self.txt_link = QtWidgets.QLineEdit('', self)
        self.txt_link.setGeometry((QtCore.QRect(70, 100, 250, 30)))
        self.txt_link.setPlaceholderText(f'Ссылка на {bk_name}')
        self.txt_link.setObjectName('txt_link')

        self.listView = QtWidgets.QListView(self)
        self.listView.setGeometry(QtCore.QRect(350, 20, 830, 500))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.listView.setFont(font)
        self.listView.setObjectName("listView")
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.print_octo_profiles()


        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn, self)
        self.buttonBox.setGeometry((QtCore.QRect(950, 470, 240, 200)))
        self.buttonBox.accepted.connect(self.save_port_and_link)
        self.buttonBox.rejected.connect(self.reject)

    def save_port_and_link(self):
        global LINK, PORT
        bk_link = self.txt_link.text()
        if bk_link:
            LINK = bk_link
            indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
            if indef_of_selected_item:
                text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
                #print(self.uuid_dict[text_selected_items])
                PORT = self.uuid_dict[text_selected_items]
                self.accept()
            else:
                print('Выберите порт')
        else:
            print('Введите ссылку')

    def print_octo_profiles(self):
        data = OctoAPI.get_octo_profiles(OctoAPI.OCTO_API_TOKEN)
        self.model.removeRows(0, self.model.rowCount())
        self.uuid_dict = {}
        for el in data['data']:
            if 'bk' in el['tags']:
                self.uuid_dict[el['title']] = el['uuid']
                self.model.appendRow(QtGui.QStandardItem(el['title']))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win1 = DialogToChoosePort("GGbet")
    win1.show()
    if win1.exec():
        print('Данные получены!')
        print(LINK)
        print(PORT)
        print()
        win2 = DialogToChoosePort("Pinnacle")
        win2.show()
        if win2.exec():
            print(LINK)
            print(PORT)
            print()
    sys.exit(app.exec())

