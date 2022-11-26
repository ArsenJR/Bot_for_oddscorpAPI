from AllLibraries import *
from OctoAPI import *
import OctoAPI

class WidgetSettingBK(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BK Settings")

        self.is_settings_saved = False

        layout = QGridLayout()
        # первая строка (ссылка на букмекерскую контору)
        self.bk_link_label = QLabel('Ссылка на букмекерскую контору:')
        self.bk_link_txt = QLineEdit()
        self.bk_link_txt.setPlaceholderText('Ссылка / зеркало')
        layout.addWidget(self.bk_link_label, 0, 0)
        layout.addWidget(self.bk_link_txt, 0, 1)

        # логин и пароль от бк
        self.login_label = QLabel('Логин:')
        self.login_txt = QLineEdit()
        self.login_txt.setPlaceholderText('Логин')
        layout.addWidget(self.login_label, 1, 0)
        layout.addWidget(self.login_txt, 1, 1)
        self.password_label = QLabel('Пароль:')
        self.password_txt = QLineEdit()
        self.password_txt.setPlaceholderText('Пароль')
        layout.addWidget(self.password_label, 2, 0)
        layout.addWidget(self.password_txt, 2, 1)

        # Минимальный баланс
        self.min_balance_label = QLabel('Минимальный допустимый баланс:')
        self.min_balance_txt = QSpinBox()
        self.min_balance_txt.setMaximum(1000000)
        layout.addWidget(self.min_balance_label, 3, 0)
        layout.addWidget(self.min_balance_txt, 3, 1)
        self.setLayout(layout)

        # Валюта
        self.currency_label = QLabel('Валюта:')
        self.currency_box = QComboBox()
        self.currency_box.addItems(['RUB', 'Другая'])
        self.currency_box.activated.connect(self.get_rate)
        self.currency_txt = QLineEdit()
        self.currency_txt.setText('1')
        self.currency_txt.setPlaceholderText('Курс валюты')

        layout.addWidget(self.currency_label, 4, 0)
        layout.addWidget(self.currency_txt, 4, 1)
        layout.addWidget(self.currency_box, 4, 2)

        # ставить ли первым
        self.betting_first_yes = QtWidgets.QRadioButton('Да')
        self.betting_first_yes.setChecked(True)
        self.betting_first_yes.toggled.connect(self.bet_sum_field_access)
        self.betting_first_no = QtWidgets.QRadioButton('Нет')

        layout.addWidget(QLabel("Ставить первым:"), 5, 0)
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.betting_first_yes)
        windowLayout.addWidget(self.betting_first_no)
        layout.addLayout(windowLayout, 5, 1)

        # Поле с фиксированной ставкой
        layout.addWidget(QLabel("Фиксированная ставка:"), 6, 0)
        self.fixed_sum_txt = QSpinBox()
        self.fixed_sum_txt.setEnabled(True)
        self.fixed_sum_txt.setMaximum(1000000)
        layout.addWidget(self.fixed_sum_txt, 6, 1)


        # комбо бокс с портами Octo
        self.octo_profiles_box = QComboBox()
        #self.octo_profiles_box.setFixedHeight(20)
        self.set_octo_profiles()

        self.btn_update_octo_profiles = QPushButton()
        self.btn_update_octo_profiles.setIcon(QtGui.QIcon('icons/refresh.png'))
        self.btn_update_octo_profiles.clicked.connect(self.set_octo_profiles)

        layout.addWidget(QLabel('Профиль в окто:'), 7, 0)
        layout.addWidget(self.octo_profiles_box, 7, 1)
        layout.addWidget(self.btn_update_octo_profiles, 7, 2)


    def set_octo_profiles(self):

        self.octo_profiles_box.clear()
        self.octo_profiles_box.addItems(["Выберите профиль"])

        data = OctoAPI.get_octo_profiles(OctoAPI.OCTO_API_TOKEN)
        self.uuid_dict = {}
        for el in data['data']:
            if 'bk' in el['tags']:
                self.uuid_dict[el['title']] = el['uuid']
                self.octo_profiles_box.addItems([el['title']])

    def bet_sum_field_access(self):
        if self.betting_first_yes.isChecked():
            self.fixed_sum_txt.setEnabled(True)
        else:
            self.fixed_sum_txt.setEnabled(False)

    def save_settings(self, bk_name):

        self.is_settings_saved = False

        self.link = self.bk_link_txt.text()
        if not self.link:
            self.error = QMessageBox.critical(self, "Ошибка!", f'Введите ссылку для {bk_name}')
            return
        self.login = self.login_txt.text()
        if not self.login:
            self.error = QMessageBox.critical(self, "Ошибка!", f'Введите логин для {bk_name}')
            return
        self.password = self.password_txt.text()
        if not self.password:
            self.error = QMessageBox.critical(self, "Ошибка!", f'Введите пароль для {bk_name}')
            return
        self.min_balabce = self.min_balance_txt.value()
        if not self.min_balabce:
            self.error = QMessageBox.critical(self, "Ошибка!", f'Введите минимальный допустимый баланс  для {bk_name}')
            return
        self.rate = self.currency_txt.text()
        if not self.rate:
            self.error = QMessageBox.critical(self, "Ошибка!", f'Введите курс валюты (к рублю)  для {bk_name}')
            return
        else:
            self.rate = float(self.rate)
        self.is_betting_first = self.betting_first_yes.isChecked()
        if self.is_betting_first:
            self.bet_sum = self.fixed_sum_txt.value()
            if not self.bet_sum:
                self.error = QMessageBox.critical(self, "Ошибка!", f'Введит сумму ставки для {bk_name}')
                return
        else:
            self.bet_sum = None

        self.octo_profiles = self.octo_profiles_box.currentText()
        if self.octo_profiles == 'Выберите профиль':
            self.error = QMessageBox.critical(self, "Ошибка!", f'Выберите порт для {bk_name}')
            return
        self.uuid = self.uuid_dict[self.octo_profiles]

        if self.link and self.login and self.password and self.min_balabce and self.rate and self.uuid:
            self.is_settings_saved = True
            return
        else:
            self.error = QMessageBox.critical(self, f'Ошибка! (заполните все поля) для {bk_name}')
            return


    def get_rate(self):
        if self.currency_box.currentIndex() == 0:
            self.currency_txt.setText('1')
        else:
            self.currency_txt.setText('60.00')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WidgetSettingBK()
    window.show()
    sys.exit(app.exec())