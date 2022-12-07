from AllLibraries import *
from OctoAPI import *
import OctoAPI

class AddConnect(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила проставления")

        self.main_window = parent

        # общий слой
        layout = QGridLayout()
        self.setLayout(layout)

        self.first_bk_box = QComboBox()
        self.first_bk_box.addItems(['pinnacle', 'fonbet', 'gg_bet'])
        layout.addWidget(QLabel('Первая БК:'), 0, 0)
        layout.addWidget(self.first_bk_box, 1, 0)

        self.second_bk_box = QComboBox()
        self.second_bk_box.addItems(['pinnacle', 'fonbet', 'gg_bet'])
        layout.addWidget(QLabel('Вторая БК:'), 4, 0)
        layout.addWidget(self.second_bk_box, 5, 0)

        self.first_rb = QRadioButton('Ставить первой')
        self.first_rb.setChecked(True)
        self.delete_pair = QRadioButton('Исключить пару')
        self.second_rb = QRadioButton('Ставить первой')

        layout.addWidget(QLabel('  '), 2, 1)
        layout.addWidget(self.first_rb, 1, 2)
        layout.addWidget(self.delete_pair, 3, 2)
        layout.addWidget(self.second_rb, 5, 2)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.get_params)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(QLabel('   '), 6, 2)
        layout.addWidget(self.buttonBox, 7, 2)

    def get_params(self):
        self.first_bk_name = self.first_bk_box.currentText()
        self.second_bk_name = self.second_bk_box.currentText()
        if self.first_bk_name == self.second_bk_name:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите разные конторы.')
            return

        self.connect_type = None
        if self.first_rb.isChecked():
            self.connect_type = 1
        if self.second_rb.isChecked():
            self.connect_type = 2
        if self.delete_pair.isChecked():
            self.connect_type = 3

        self.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddConnect()
    window.show()
    sys.exit(app.exec())


