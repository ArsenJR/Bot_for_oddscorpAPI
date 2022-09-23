from AllLibraries import *

class DialogToLogIn(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.resize(640,480)

        layout = QtWidgets.QVBoxLayout()

        # Последовательность проставления
        self.groupbox_sequence = QtWidgets.QGroupBox()
        self.groupbox_sequence.setTitle('Последовательность проставления')
        layout_affixing_alg = QtWidgets.QVBoxLayout()
        self.r_btn_synch = QtWidgets.QRadioButton('Синхронное проставление')
        self.r_btn_synch.setChecked(True)
        self.r_btn_first_pin = QtWidgets.QRadioButton('Первым Pinnacle, затем GGBet')
        self.r_btn_first_ggbet = QtWidgets.QRadioButton('Первым GGBet, затем Pinnacle')
        layout_affixing_alg.addWidget(self.r_btn_synch)
        layout_affixing_alg.addWidget(self.r_btn_first_pin)
        layout_affixing_alg.addWidget(self.r_btn_first_ggbet)
        self.groupbox_sequence.setLayout(layout_affixing_alg)
        layout.addWidget(self.groupbox_sequence)


        # Ограничения по сумме ставки
        self.groupbox_bet_sum = QtWidgets.QGroupBox()
        self.groupbox_bet_sum.setTitle('Ограничения по сумме ставки')
        layout_bet_sum = QtWidgets.QVBoxLayout()
        self.r_btn_total_sum = QtWidgets.QRadioButton('Максимальная общая сумма двух ставок')
        self.r_btn_total_sum.setChecked(True)
        self.r_btn_pin_sum = QtWidgets.QRadioButton('Максимальная ставка на GGBet')
        self.r_btn_ggbet_sum = QtWidgets.QRadioButton('Максимальная ставка на Pinnacle')
        self.sum_line = QtWidgets.QLineEdit()
        self.sum_line.setPlaceholderText('Введите сумму')
        layout_bet_sum.addWidget(self.r_btn_total_sum)
        layout_bet_sum.addWidget(self.r_btn_pin_sum)
        layout_bet_sum.addWidget(self.r_btn_ggbet_sum)
        layout_bet_sum.addWidget(self.sum_line)
        self.groupbox_bet_sum.setLayout(layout_bet_sum)
        layout.addWidget(self.groupbox_bet_sum)

        # Автоматическое проставление на киберспорт
        self.groupbox_auto_betting = QtWidgets.QGroupBox()
        self.groupbox_auto_betting.setTitle('Автоматическое проставление вилки')
        layout_yes_no = QtWidgets.QVBoxLayout()
        self.r_btn_yes = QtWidgets.QRadioButton('Да')
        self.r_btn_no = QtWidgets.QRadioButton('Нет')
        self.r_btn_no.setChecked(True)
        layout_yes_no.addWidget(self.r_btn_yes)
        layout_yes_no.addWidget(self.r_btn_no)
        self.groupbox_auto_betting.setLayout(layout_yes_no)
        layout.addWidget(self.groupbox_auto_betting)

        # Кнопки ОК и Cancel
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.get_params)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


    def get_params(self):

        how_do_bet = 1
        if self.r_btn_synch.isChecked():
            how_do_bet = 1
        elif self.r_btn_first_ggbet.isChecked():
            how_do_bet = 2
        elif self.r_btn_first_pin.isChecked():
            how_do_bet = 3

        limit_type = 1
        limit_sum = 0
        if self.r_btn_total_sum.isChecked():
            limit_type = 1
            limit_sum = self.sum_line.text()
        elif self.r_btn_pin_sum.isChecked():
            limit_type = 2
            limit_sum = self.sum_line.text()
        elif self.r_btn_ggbet_sum.isChecked():
            limit_type = 3
            limit_sum = self.sum_line.text()

        auto_bet = False
        if self.r_btn_yes.isChecked():
            auto_bet = True
        else:
            auto_bet = False

        if limit_sum:
            print(f'Тип последовательности проставления {how_do_bet}')
            print(f'Тип ограничений по сумме ставки {limit_type}, максимальная сумма {limit_sum}')
            print(f'Автоматическое проставление {auto_bet}')
        else:
            print('Введите сумму')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DialogToLogIn()
    win.show()
    sys.exit(app.exec())