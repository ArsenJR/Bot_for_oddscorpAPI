import math

import GGBetDriver
import PinnacleDriver
from ForkScanerClass import *
import ForkScanerClass
from QDialodToLogin import *
import QDialodToLogin
from SetParamToBetting import *
import SetParamToBetting
from GGBetDriver import *
from PinnacleDriver import *
from GetToOddscorp import *
from ChoosePort import *
import ChoosePort
from CurrencyConverter import *
import CurrencyConverter
from BetAmountCalculator import bet_calc

class Window(QMainWindow, QObject, object):

    signal_to_logIn_ggbet = pyqtSignal(list)
    signal_to_logIn_pinnacle = pyqtSignal(list)
    signal_to_send_bet_parameter_to_ggbet = pyqtSignal(dict)
    signal_to_send_bet_parameter_to_pinnacle = pyqtSignal(dict)
    signal_do_bet_pinnacle = pyqtSignal(list)
    signal_do_bet_ggbet = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

        # определяем переменные класса
        self.auto_betting = False   # автоматическое проставление
        self.is_ports_open = False  # открыты ли порты
        self.is_settings_defined = False    # заданы ли настройки
        self.auto_betting = False   # автоматическое проставление
        self.limit_type = None      # по какой бк брать фиксированную ставку
        self.limit_sum = None       # фиксированная сумма ставки (общая или в одной из бк)
        self.how_do_bet = None      # как ставить (какую первую)
        # данные по валютам в бк
        self.is_ggbet_rub = True
        self.is_pinnacle_rub = True
        self.ggbet_exchange_rate = 1
        self.pinnacle_exchange_rate = 1

    def setupUi(self):
        self.setWindowTitle("Сканер вилок с автоматизированным проставлением")
        self.setFixedSize(1500, 800)

        # создаем menubar
        self.menu = self.menuBar()
        self.start_menu = self.menu.addMenu("&Начало")
        self.settings_menu = self.menu.addMenu("&Настройки")
        self.help_menu = self.menu.addMenu("&Помощь")

        # cоздаем QActions, которыми будем заполнять menuBar

        # кнопка выбора порта
        self.btn_choose_port = QAction("&Выбор порта", self)
        self.btn_choose_port.setStatusTip("Choose port from Octo Browser")
        self.btn_choose_port.triggered.connect(self.open_port_choose_dialog)
        self.btn_choose_port.setEnabled(True)
        # кнопка входа на аккаунт в портах
        self.btn_log_in = QAction("&Авторизоваться", self)
        self.btn_log_in.setStatusTip("Log in BK")
        # self.btn_log_in.triggered.connect(self.open_logIn_dialog)
        self.btn_log_in.setEnabled(False)

        # кнопка общих настроек
        self.btn_settings = QAction("&Настройки бота", self)
        self.btn_settings.setStatusTip("Settings")
        self.btn_settings.triggered.connect(self.open_settings_dialog)
        # кнопка с настройкой валюты
        self.btn_currency_converter = QAction("&Конвертер валют", self)
        self.btn_currency_converter.setStatusTip("Currency Converter")
        self.btn_currency_converter.triggered.connect(self.open_currency_converter_dialog)


        # кнопка со справкой
        self.btn_reference = QAction("&Справка", self)
        self.btn_reference.setStatusTip("Referens")
        # self.btn_reference.triggered.connect(self.onMyToolBarButtonClick)
        # кнопка c описанием бота
        self.btn_description = QAction("&О боте", self)
        self.btn_description.setStatusTip("Description")
        # self.btn_description.triggered.connect(self.onMyToolBarButtonClick)

        # заполняем start menu
        self.start_menu.addAction(self.btn_choose_port)
        self.start_menu.addSeparator()
        self.start_menu.addAction(self.btn_log_in)

        # заполняем settings menu
        self.settings_menu.addAction(self.btn_settings)
        self.settings_menu.addSeparator()
        self.settings_menu.addAction(self.btn_currency_converter)

        # заполняем help menu
        self.help_menu.addAction(self.btn_reference)
        self.help_menu.addAction(self.btn_description)

        # создаем для обращение к окну приложения
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Создаем listView для вывода информации о ставках
        self.listView = QtWidgets.QListView(self.centralWidget)
        self.listView.setGeometry(QtCore.QRect(400, 50, 1050, 670))
        # выбираем настройки шрифта в listView
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.listView.setFont(font)
        self.listView.setObjectName("listView")
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # создаем кнопку окончания работы сканера
        self.btn_scaner_end = QtWidgets.QPushButton('Закончить сканирование', self)
        self.btn_scaner_end.setGeometry((QtCore.QRect(150, 500, 200, 30)))
        self.btn_scaner_end.setObjectName('btn_scaner_end')
        self.btn_scaner_end.clicked.connect(self.scanerEnd)
        self.btn_scaner_end.setEnabled(False)

        # создаем кнопку начало сканирования
        self.btn_scaner_start = QtWidgets.QPushButton('Начать сканирование', self)
        self.btn_scaner_start.setGeometry(QtCore.QRect(150, 600, 200, 30))
        self.btn_scaner_start.setObjectName("btn_start_scan")
        self.btn_scaner_start.setEnabled(False)
        self.btn_scaner_start.clicked.connect(self.scanerStartInThread)

        # кнопка "Сделать ставку"
        self.btn_do_bet = QtWidgets.QPushButton('Сделать ставку', self)
        self.btn_do_bet.setGeometry(QtCore.QRect(150, 700, 200, 30))
        self.btn_do_bet.setObjectName("btn_do_bet")
        self.btn_do_bet.setEnabled(False)
        self.btn_do_bet.clicked.connect(self.get_cf_bet_limit)

        # логические значения (приняты ли данные о кф и лимите ставки из бк)
        self.is_ggbet_data_received = False
        self.is_pinnacle_data_received = False

        # Параметры для ставки
        self.limit_sum = None

        # лист с id нужных вилок
        self.list_forks_auto_betting = []


    def save_cf_and_bet_limit_from_pinnacle(self, data):
        self.pinnacle_cf = None
        self.pinnacle_limit_sum = None
        print('Accsesed pinnacle')

        self.pinnacle_cf = float(data[0])
        self.pinnacle_limit_sum = int(float(data[1].replace(',', '.')))

        print(self.pinnacle_cf, type(self.pinnacle_cf))
        print(self.pinnacle_limit_sum, type(self.pinnacle_limit_sum))

        self.is_pinnacle_data_received = True

        if self.is_ggbet_data_received:
            sum_two_bets = bet_calc(pin_cf=self.pinnacle_cf, ggbet_cf=self.ggbet_cf,
                                    pin_limit=self.pinnacle_limit_sum, ggbet_limit=self.ggbet_limit_sum,
                                    is_rub_pin=self.is_pinnacle_rub, is_rub_ggbet=self.is_ggbet_rub,
                                    ggbet_exchange_rate=self.ggbet_exchange_rate,
                                    pin_exchange_rate=self.pinnacle_exchange_rate,
                                    settings_type_limit=self.limit_type,
                                    settings_sum_limit=float(self.limit_sum))
            if sum_two_bets != 0:
                pinnacle_bet = sum_two_bets[0]
                ggbet_bet = sum_two_bets
                print(pinnacle_bet)
                print(ggbet_bet)
            #self.bet_calc()

    def save_cf_and_bet_limit_from_ggbet(self, data):
        self.ggbet_cf = None
        self.ggbet_limit_sum = None
        print('Accsesed ggbet')

        self.ggbet_cf = float(data[0])
        self.ggbet_limit_sum = int(float(data[1]))

        print(self.ggbet_cf, type(self.ggbet_cf))
        print(self.ggbet_limit_sum, type(self.ggbet_limit_sum))

        self.is_ggbet_data_received = True

        if self.is_pinnacle_data_received:
            sum_two_bets = bet_calc(pin_cf=self.pinnacle_cf, ggbet_cf=self.ggbet_cf,
                                    pin_limit=self.pinnacle_limit_sum, ggbet_limit=self.ggbet_limit_sum,
                                    is_rub_pin=self.is_pinnacle_rub, is_rub_ggbet=self.is_ggbet_rub,
                                    ggbet_exchange_rate=self.ggbet_exchange_rate,
                                    pin_exchange_rate=self.pinnacle_exchange_rate,
                                    settings_type_limit=self.limit_type,
                                    settings_sum_limit=float(self.limit_sum))
            if sum_two_bets != 0:
                pinnacle_bet = sum_two_bets[0]
                ggbet_bet = sum_two_bets
                print(pinnacle_bet)
                print(ggbet_bet)
            #self.bet_calc()

    def bet_calc(self):

        print('Pinnacle    ', self.pinnacle_cf, self.pinnacle_limit_sum)
        print('GGbet    ', self.ggbet_cf, self.ggbet_limit_sum)

        total_prob = 1 / self.ggbet_cf + 1 / self.pinnacle_cf
        print(total_prob)

        if total_prob < 1:
            if self.limit_sum:
                pinnacle_sum_bet = float(self.limit_sum)
            else:
                pinnacle_sum_bet = float(500)
            ggbet_sum_bet = (pinnacle_sum_bet * self.pinnacle_cf) / self.ggbet_cf
            if ggbet_sum_bet > self.ggbet_limit_sum:
                ggbet_sum_bet = self.ggbet_limit_sum
                pinnacle_sum_bet = (ggbet_sum_bet * self.ggbet_cf) / self.pinnacle_cf
            self.signal_do_bet_pinnacle.emit([int(math.ceil(pinnacle_sum_bet / 63)), self.pinnacle_cf])
            self.signal_do_bet_ggbet.emit([int(ggbet_sum_bet), self.ggbet_cf])

    def open_currency_converter_dialog(self):
        dialog = DialogCurrencyConverter(self)
        dialog.show()
        if dialog.exec():
            self.is_ggbet_rub = CurrencyConverter.is_ggbet_rub
            self.is_pinnacle_rub = CurrencyConverter.is_pinnacle_rub
            self.ggbet_exchange_rate = CurrencyConverter.ggbet_exchange_rate
            self.pinnacle_exchange_rate = CurrencyConverter.pinnacle_exchange_rate
            print('Данные по валютам получены')
        else:
            print('Cansel!')

    def open_port_choose_dialog(self):  # Открытие поля с выбором порта Octo Browser
        dialog = DialogToChoosePort(bk_name="ggbet", parent=self)
        dialog.show()
        if dialog.exec():
            print('Данные по GGBet получены!')
            ggbet_link = ChoosePort.LINK
            ggbet_port = ChoosePort.PORT
            dialog = DialogToChoosePort(bk_name="pinnacle", parent=self)
            dialog.show()
            if dialog.exec():
                print('Данные по PINNACLE получены!')
                pinnacle_link = ChoosePort.LINK
                pinnacle_port = ChoosePort.PORT

                GGBetDriver.GGBET_PORT = ggbet_port
                GGBetDriver.GGBET_LINK = ggbet_link
                PinnacleDriver.PINNACLE_PORT = pinnacle_port
                PinnacleDriver.PINNACLE_LINK = pinnacle_link

                if pinnacle_port != ggbet_port:
                    self.open_pinnacle_driver()
                    self.open_ggbet_driver()
                    self.btn_log_in.setEnabled(True)
                    self.is_ports_open = True
                    # открываем дроступ к кнопке начать сканирование по условию
                    if self.is_settings_defined:
                        self.btn_scaner_start.setEnabled(True)


    def open_ggbet_driver(self):
        self.ggbet_thread = QThread()
        self.ggbet_driver = ggbetDriver()
        self.ggbet_driver.moveToThread(self.ggbet_thread)
        self.ggbet_thread.started.connect(self.ggbet_driver.doWebDriver)
        #self.signal_to_logIn_ggbet.connect(self.ggbet_driver.log_in)
        self.signal_to_send_bet_parameter_to_ggbet.connect(self.ggbet_driver.do_bet)
        self.ggbet_driver.signal_with_cf_and_bet_limit.connect(self.save_cf_and_bet_limit_from_ggbet)
        self.signal_do_bet_ggbet.connect(self.ggbet_driver.betting)

        self.ggbet_thread.start()


    def open_pinnacle_driver(self):
        self.pinnacle_thread = QThread()
        self.pinnacle_driver = pinnacleDriver()
        self.pinnacle_driver.moveToThread(self.pinnacle_thread)
        self.pinnacle_thread.started.connect(self.pinnacle_driver.doWebDriver)
        #self.signal_to_logIn_pinnacle.connect(self.pinnacle_driver.log_in)
        self.signal_to_send_bet_parameter_to_pinnacle.connect(self.pinnacle_driver.do_bet)
        self.pinnacle_driver.signal_with_cf_and_bet_limit.connect(self.save_cf_and_bet_limit_from_pinnacle)
        self.signal_do_bet_pinnacle.connect(self.pinnacle_driver.betting)

        self.pinnacle_thread.start()

    """_____Проставление вилки_____"""
    def auto_get_cf_bet_limit(self, fork):
        fork_for_bet = fork
        self.signal_to_send_bet_parameter_to_ggbet.emit(fork_for_bet)
        self.signal_to_send_bet_parameter_to_pinnacle.emit(fork_for_bet)
        self.is_ggbet_data_received = False
        self.is_pinnacle_data_received = False
        self.pinnacle_cf = None
        self.ggbet_cf = None
        self.pinnacle_limit_sum = None
        self.ggbet_limit_sum = None
        self.btn_scaner_end.click()

    def get_cf_bet_limit(self):
        name = None
        indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
        if indef_of_selected_item:
            text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
            text_selected_items = " | ".join(text_selected_items.split(' | ')[:-1])
            name = text_selected_items
            print(name)
        else:
            print('Выберите ставку')

        if name:
            fork_now, fork_now_key, fork_now_dict = get_fork_to_bet()
            try:
                for i in range(len(fork_now)):
                    if name == fork_now[i]:
                        fork_key = fork_now_key[i]
                        break
                if fork_key:
                    for fork in fork_now_dict:
                        if fork['fork_id'] == fork_key:
                            fork_for_bet = fork
                            self.signal_to_send_bet_parameter_to_ggbet.emit(fork_for_bet)
                            self.signal_to_send_bet_parameter_to_pinnacle.emit(fork_for_bet)
                            self.is_ggbet_data_received = False
                            self.is_pinnacle_data_received = False
                            self.btn_scaner_end.clicked()
            except:
                print("Вилка пропала")


    """_____Работа сканера в потоке_____"""
    def reportProgress(self, n):
        fork_now, fork_alive_now, forks_data = n
        for fork_data in forks_data:
            if self.is_auto_work:
                if fork_data['fork_id'] not in self.list_forks_auto_betting:
                    if fork_data['alive_sec'] > 2:
                        if fork_data['sport'] == 'esports.cs':
                            self.is_auto_work = False
                            print('Нашел новую вилку CS  ', fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.btn_scaner_end.click()
                            self.auto_get_cf_bet_limit(fork_data)
                            return

                        if fork_data['sport'] == 'esports.dota2':
                            self.is_auto_work = False
                            print('Нашел новую вилку DOTA2  ', fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.btn_scaner_end.click()
                            self.auto_get_cf_bet_limit(fork_data)
                            return

                        if fork_data['sport'] == 'esports.lol':
                            self.is_auto_work = False
                            print('Нашел новую вилку LOL  ', fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.auto_get_cf_bet_limit(fork_data)
                            return

                    if fork_data['sport'] == 'tennis':
                        if fork_data['bet_type'] == 'TOTALS':
                            self.is_auto_work = False
                            print('Нашел новую вилку tennis  ', fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.list_forks_auto_betting.append(fork_data['fork_id'])
                            self.auto_get_cf_bet_limit(fork_data)
                            return


        # получаем выбранный эллемент
        indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
        # получаем текст выбранного эллемента
        name = None
        if indef_of_selected_item:
            text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
            text_selected_items = " | ".join(text_selected_items.split(' | ')[:-1])
            name = text_selected_items

        self.model.removeRows(0, self.model.rowCount())
        row_number = 1000
        for i in range(len(fork_now)):

            self.model.appendRow(QtGui.QStandardItem(fork_now[i] + f' | {fork_alive_now[i]}'))
            if name == fork_now[i]:
                row_number = i

        if row_number != 1000:
            index = self.model.index(row_number, 0)
            sm = self.listView.selectionModel()
            sm.select(index, QItemSelectionModel.Select)

    def scanerEnd(self):
        ForkScanerClass.CHEK = False

    def scanerStartInThread(self):
        if self.auto_betting:
            self.is_auto_work = True
            self.btn_do_bet.setEnabled(False)
        else:
            self.is_auto_work = False
            self.btn_do_bet.setEnabled(True)
        ForkScanerClass.CHEK = True

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.scanner = ForkScaner()
        # Step 4: Move worker to the thread
        self.scanner.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.scanner.get_forks_from_oddscorp)
        self.scanner.finished.connect(self.thread.quit)
        self.scanner.finished.connect(self.scanner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.scanner.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        self.btn_scaner_start.setEnabled(False)
        self.btn_scaner_end.setEnabled(True)
        self.thread.finished.connect(
            lambda: self.btn_scaner_start.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.btn_scaner_end.setEnabled(False)
        )
        self.thread.finished.connect(
            lambda: self.btn_do_bet.setEnabled(False)
        )
        self.thread.finished.connect(
            lambda: self.model.removeRows(0, self.model.rowCount())
        )

    """_____Настройки проставления_____"""
    def open_settings_dialog(self):
        self.scanerEnd()
        dialog = DialogSettings(self)
        if dialog.exec():
            print('Данные получены!')
            self.limit_type = SetParamToBetting.limit_type
            self.limit_sum = SetParamToBetting.limit_sum
            self.auto_betting = SetParamToBetting.auto_bet
            self.how_do_bet = SetParamToBetting.how_do_bet

            # настройки установлены
            self.is_settings_defined = True
            # открываем дроступ к кнопке начать сканирование по условию
            if self.is_ports_open:
                self.btn_scaner_start.setEnabled(True)
        else:
            print('Cansel!')

    """_____Log In BK_____"""
    def open_logIn_dialog(self):
        self.scanerEnd()
        ggbet_dialog = DialogToLogIn("GGbet")
        if ggbet_dialog.exec():
            ggbet_login = QDialodToLogin.Login
            ggbet_password = QDialodToLogin.Password
            pinnacle_dialog = DialogToLogIn("PINNACLE")
            if pinnacle_dialog.exec():
                pinnacle_login = QDialodToLogin.Login
                pinnacle_password = QDialodToLogin.Password
                # авторизуемся в конторах
                self.signal_to_logIn_ggbet.emit([ggbet_login, ggbet_password])
                self.signal_to_logIn_pinnacle.emit([pinnacle_login, pinnacle_password])

                self.btn_bk_logIn.setEnabled(False)
                self.btn_do_bet.setEnabled(True)
        else:
            print("Cancel!")


    """
        
    

    

    def bet_calc(self, dict):
        if dict['BK1_name'] == 'gg_bet':
            ggbet_cf = dict['BK1_cf']
            pinnacle_cf = dict['BK2_cf']
        elif dict['BK2_name'] == 'gg_bet':
            ggbet_cf = dict['BK2_cf']
            pinnacle_cf = dict['BK1_cf']

        total_prob = 1 / ggbet_cf + 1 / pinnacle_cf

        if self.limit_type == 1:
            ggbet_sum_bet = math.ceil(1 / ggbet_cf / total_prob * float(self.limit_sum))
            pinnacle_sum_bet = math.ceil(1 / pinnacle_cf / total_prob * float(self.limit_sum))
            dict['ggbet_sum_bet'] = ggbet_sum_bet
            dict['pinnacle_sum_bet'] = pinnacle_sum_bet
        elif self.limit_type == 2: # макс ставка на ggbet
            ggbet_sum_bet = float(self.limit_sum)
            pinnacle_sum_bet = (ggbet_sum_bet * ggbet_cf) / pinnacle_cf
            dict['ggbet_sum_bet'] = math.ceil(ggbet_sum_bet)
            dict['pinnacle_sum_bet'] = math.ceil(pinnacle_sum_bet)
        elif self.limit_type == 3: # макс ставка на pinnacle
            pinnacle_sum_bet = float(self.limit_sum)
            ggbet_sum_bet = (pinnacle_sum_bet * pinnacle_cf) / ggbet_cf
            dict['ggbet_sum_bet'] = math.ceil(ggbet_sum_bet)
            dict['pinnacle_sum_bet'] = math.ceil(pinnacle_sum_bet)
        return dict



    

    def test_fu(self):
        print('Go')
        print(self.pinnacle_cf, self.pinnacle_limit_sum)
        print(self.ggbet_cf, self.ggbet_limit_sum)


        profit = 1/self.ggbet_cf + 1 / self.pinnacle_cf
        print(profit)
        if profit < 1:
            ggbet_sum_bet = math.ceil(1 / self.ggbet_cf / profit * float(self.limit_sum))
            pinnacle_sum_bet = math.ceil(1 / self.pinnacle_cf / profit * float(self.limit_sum))
            if ggbet_sum_bet > self.ggbet_limit_sum:
                ggbet_sum_bet = self.ggbet_limit_sum
                pinnacle_sum_bet = (ggbet_sum_bet * self.ggbet_cf) / self.pinnacle_cf
                if pinnacle_sum_bet > self.pinnacle_limit_sum:
                    pinnacle_sum_bet = self.pinnacle_limit_sum
                    ggbet_sum_bet = (pinnacle_sum_bet * self.pinnacle_cf) / self.ggbet_cf

            if pinnacle_sum_bet > self.pinnacle_limit_sum:
                pinnacle_sum_bet = self.pinnacle_limit_sum
                ggbet_sum_bet = (pinnacle_sum_bet * self.pinnacle_cf) / self.ggbet_cf

            print('GGbet ', math.ceil(ggbet_sum_bet))
            print('Pinnacle ', math.ceil(pinnacle_sum_bet))
            self.signal_do_bet_pinnacle(int(math.ceil(pinnacle_sum_bet)))
            #self.signal_do_bet_ggbet(math.ceil(ggbet_sum_bet))

        else:
            print('В этих ставках вилки не обнаружено')



    



    
    

    




    




"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())