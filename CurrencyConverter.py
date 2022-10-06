from AllLibraries import *

is_ggbet_rub = True
is_pinnacle_rub = True
ggbet_exchange_rate = 1
pinnacle_exchange_rate = 1

class DialogCurrencyConverter(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Конвертер валют")
        self.resize(640,480)

        layout = QtWidgets.QVBoxLayout()

        # Выбор валюты GGbet
        self.groupbox_sequence = QtWidgets.QGroupBox()
        self.groupbox_sequence.setTitle('Валюта на GGBet:')
        layout_ggbet = QtWidgets.QVBoxLayout()

        self.r_btn_rub_ggbet = QtWidgets.QRadioButton('RUB')
        self.r_btn_rub_ggbet.setChecked(True)
        self.r_btn_another_ggbet = QtWidgets.QRadioButton('Другая')
        self.line_exchange_rate_ggbet = QtWidgets.QLineEdit()
        self.line_exchange_rate_ggbet.setPlaceholderText('Введите курс к рублю (если не RUB)')

        layout_ggbet.addWidget(self.r_btn_rub_ggbet)
        layout_ggbet.addWidget(self.r_btn_another_ggbet)
        layout_ggbet.addWidget(self.line_exchange_rate_ggbet)

        self.groupbox_sequence.setLayout(layout_ggbet)
        layout.addWidget(self.groupbox_sequence)

        # Выбор валюты Pinnacle
        self.groupbox_bet_sum = QtWidgets.QGroupBox()
        self.groupbox_bet_sum.setTitle('Валюта на Pinnacle:')
        layout_pinnacle = QtWidgets.QVBoxLayout()

        self.r_btn_rub_pinnacle = QtWidgets.QRadioButton('RUB')
        self.r_btn_rub_pinnacle.setChecked(True)
        self.r_btn_another_pinnacle = QtWidgets.QRadioButton('Другая')
        self.line_exchange_rate_pinnacle = QtWidgets.QLineEdit()
        self.line_exchange_rate_pinnacle.setPlaceholderText('Введите курс к рублю (если не RUB)')

        layout_pinnacle.addWidget(self.r_btn_rub_pinnacle)
        layout_pinnacle.addWidget(self.r_btn_another_pinnacle)
        layout_pinnacle.addWidget(self.line_exchange_rate_pinnacle)

        self.groupbox_bet_sum.setLayout(layout_pinnacle)
        layout.addWidget(self.groupbox_bet_sum)

        # Кнопки ОК и Cancel
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.get_params)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        global is_ggbet_rub, is_pinnacle_rub, ggbet_exchange_rate, pinnacle_exchange_rate
        is_ggbet_rub = True
        is_pinnacle_rub = True
        ggbet_exchange_rate = 1
        pinnacle_exchange_rate = 1


    def get_params(self):

        global is_ggbet_rub, is_pinnacle_rub, ggbet_exchange_rate, pinnacle_exchange_rate
        first_check = False
        second_check = False
        if self.r_btn_another_ggbet.isChecked():
            is_ggbet_rub = False
            ggbet_exchange_rate = self.line_exchange_rate_ggbet.text()
            if ggbet_exchange_rate:
                first_check = True
        else:
            is_ggbet_rub = True
            first_check = True

        if self.r_btn_another_pinnacle.isChecked():
            is_pinnacle_rub = False
            pinnacle_exchange_rate = self.line_exchange_rate_pinnacle.text()
            if pinnacle_exchange_rate:
                second_check = True
        else:
            is_pinnacle_rub = True
            second_check = True

        if first_check and second_check:
            print('GGBet:     RUB: ', is_ggbet_rub, '  коэфициент к рублю:', ggbet_exchange_rate)
            print('Pinnacle:    RUB ', is_pinnacle_rub, '  коэфициент к рублю:', pinnacle_exchange_rate)
            self.accept()
        else:
            print('Не все поля заполнены подобающим образом')

