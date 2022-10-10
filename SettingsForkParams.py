from AllLibraries import *

SPORT_TYPE_LIST = []
BET_TYPE_LIST = []
PROFIT_MIN = 0.5
PROFIT_MAX = 20
LOOSE_MAX = 10
SECOND_DO_BET = 8
СOUNT_FORKS_IN_MATCH = 1
SECOND_ALIVE_TO_BETTING = 3
class DialogFilterSettings(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки")
        self.resize(640,600)

        layout = QtWidgets.QVBoxLayout()

        # Тип спорта
        self.groupbox_sequence = QtWidgets.QGroupBox()
        self.groupbox_sequence.setTitle('Вид спорта:')
        layout_sport_type = QtWidgets.QVBoxLayout()
        self.check_csgo = QtWidgets.QCheckBox('CS GO')
        self.check_dota = QtWidgets.QCheckBox('DOTA 2')
        self.check_lol = QtWidgets.QCheckBox('LOL')
        #self.check_soccer = QtWidgets.QCheckBox('Soccer')
        #self.check_tennis = QtWidgets.QCheckBox('Tennis')

        layout_sport_type.addWidget(self.check_csgo)
        layout_sport_type.addWidget(self.check_dota)
        layout_sport_type.addWidget(self.check_lol)
        #layout_sport_type.addWidget(self.check_soccer)
        #layout_sport_type.addWidget(self.check_tennis)

        self.groupbox_sequence.setLayout(layout_sport_type)
        layout.addWidget(self.groupbox_sequence)


        # Тип ставки
        self.groupbox_bet_sum = QtWidgets.QGroupBox()
        self.groupbox_bet_sum.setTitle('Тип ставки:')
        layout_bet_sum = QtWidgets.QVBoxLayout()
        self.check_win = QtWidgets.QCheckBox('WIN')
        self.check_totals = QtWidgets.QCheckBox('TOTALS')
        self.check_handicap = QtWidgets.QCheckBox('HANDICAP')

        layout_bet_sum.addWidget(self.check_win)
        layout_bet_sum.addWidget(self.check_totals)
        layout_bet_sum.addWidget(self.check_handicap)

        self.groupbox_bet_sum.setLayout(layout_bet_sum)
        layout.addWidget(self.groupbox_bet_sum)

        # Филтр вилок
        self.groupbox_bet_sum = QtWidgets.QGroupBox()
        self.groupbox_bet_sum.setTitle('Параметры проставления вилок')
        layout_bet_sum = QtWidgets.QVBoxLayout()
        self.lable_profit_range = QtWidgets.QLabel('Диапазон прибыли вилок, которые бот должен проставлять:')
        self.profit_range_min = QtWidgets.QLineEdit()
        self.profit_range_min.setPlaceholderText('Минимум (в %)')
        self.profit_range_max = QtWidgets.QLineEdit()
        self.profit_range_max.setPlaceholderText('Максимум (в %)')
        self.lable_loss_range = QtWidgets.QLabel('Максимальный процент потерь, с которым боту разрешено проставлять плечо')
        self.loss_range = QtWidgets.QLineEdit()
        self.loss_range.setPlaceholderText('Максимальные потери (в %)')
        self.lable_sec_try_do_bet = QtWidgets.QLabel('Сколько секунд бот пытается закрыть плечо:')
        self.sec_count = QtWidgets.QLineEdit()
        self.sec_count.setPlaceholderText('Кол-во секунд')
        self.lable_count_fork_in_match = QtWidgets.QLabel('Максимальное кол-во вилок в одном событии:')
        self.count_fork_in_match = QtWidgets.QLineEdit()
        self.count_fork_in_match.setPlaceholderText('Кол-во вилок')
        self.lable_count_alive_forks = QtWidgets.QLabel('Через сколько секунд проставляется вилка:')
        self.count_alive_forks = QtWidgets.QLineEdit()
        self.count_alive_forks.setPlaceholderText('Секунды')

        layout_bet_sum.addWidget(self.lable_profit_range)
        layout_bet_sum.addWidget(self.profit_range_min)
        layout_bet_sum.addWidget(self.profit_range_max)
        layout_bet_sum.addWidget(self.lable_loss_range)
        layout_bet_sum.addWidget(self.loss_range)
        layout_bet_sum.addWidget(self.lable_sec_try_do_bet)
        layout_bet_sum.addWidget(self.sec_count)
        layout_bet_sum.addWidget(self.lable_count_fork_in_match)
        layout_bet_sum.addWidget(self.count_fork_in_match)
        layout_bet_sum.addWidget(self.lable_count_alive_forks)
        layout_bet_sum.addWidget(self.count_alive_forks)

        self.groupbox_bet_sum.setLayout(layout_bet_sum)
        layout.addWidget(self.groupbox_bet_sum)


        # Кнопки ОК и Cancel
        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.get_params)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        # global переменные
        global SPORT_TYPE_LIST, BET_TYPE_LIST, PROFIT_MIN, PROFIT_MAX, LOOSE_MAX, \
            SECOND_DO_BET, СOUNT_FORKS_IN_MATCH, SECOND_ALIVE_TO_BETTING
        SPORT_TYPE_LIST = []
        BET_TYPE_LIST = []
        PROFIT_MIN = 0.5
        PROFIT_MAX = 20
        LOOSE_MAX = 10
        SECOND_DO_BET = 8
        СOUNT_FORKS_IN_MATCH = 1
        SECOND_ALIVE_TO_BETTING = 3


    def get_params(self):

        global SPORT_TYPE_LIST, BET_TYPE_LIST, PROFIT_MIN, PROFIT_MAX, LOOSE_MAX, \
            SECOND_DO_BET, СOUNT_FORKS_IN_MATCH, SECOND_ALIVE_TO_BETTING
        SPORT_TYPE_LIST = []
        BET_TYPE_LIST = []
        PROFIT_MIN = None
        PROFIT_MAX = None
        LOOSE_MAX = None
        SECOND_DO_BET = None
        СOUNT_FORKS_IN_MATCH = None
        SECOND_ALIVE_TO_BETTING = None

        profit_min = self.profit_range_min.text()
        profit_max = self.profit_range_max.text()
        loss_max = self.loss_range.text()
        second_do_bet = self.sec_count.text()
        count_forks_in_match = self.count_fork_in_match.text()
        second_alive_to_betting = self.count_alive_forks.text()

        if profit_max and profit_min and loss_max and second_do_bet and count_forks_in_match and second_alive_to_betting:

            PROFIT_MAX = float(profit_max)
            PROFIT_MIN = float(profit_min)
            LOOSE_MAX = float(loss_max)
            SECOND_DO_BET = int(float(second_do_bet))
            СOUNT_FORKS_IN_MATCH = int(float(count_forks_in_match))
            SECOND_ALIVE_TO_BETTING = int(float(second_alive_to_betting))


            if self.check_csgo.isChecked():
                SPORT_TYPE_LIST.append('esports.cs')
            if self.check_dota.isChecked():
                SPORT_TYPE_LIST.append('esports.dota2')
            if self.check_lol.isChecked():
                SPORT_TYPE_LIST.append('esports.lol')
                #SPORT_TYPE_LIST.append('tennis')
                #SPORT_TYPE_LIST.append('soccer')

            if self.check_win.isChecked():
                BET_TYPE_LIST.append('WIN')
                BET_TYPE_LIST.append('SET_WIN')
            if self.check_totals.isChecked():
                BET_TYPE_LIST.append('SETS_TOTALS')
                BET_TYPE_LIST.append('TOTALS')
            if self.check_handicap.isChecked():
                BET_TYPE_LIST.append('HANDICAP')

            if BET_TYPE_LIST and SPORT_TYPE_LIST:
                self.accept()
        else:
            print('Не заполнили все поля')






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DialogFilterSettings()
    win.show()
    sys.exit(app.exec())