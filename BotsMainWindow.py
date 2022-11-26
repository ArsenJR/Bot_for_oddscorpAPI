from AllLibraries import *

from WidgetPageComboSettingsBK import PagesSettingsBK
from WidgetBettingSettings import BettingSettings
from GeneralSettings import GeneralSettings
from BotWidget import BotWindow

from ChooseOctoPorts import ChoosePortOcto
from GGBetDriver import *
from PinnacleDriver import *
from FonbetDriver import *
from ForkScanerClass import *
import ForkScanerClass
from WidgetBkSettings import WidgetSettingBK
from ForkCalculator import is_fork_fit, order_of_betting


class MainWindow(QMainWindow, QObject, object):

    # сигналы
            # сигнал открытия купона в конторах
    signal_to_send_bet_parameter_to_ggbet = pyqtSignal(dict)
    signal_to_send_bet_parameter_to_pinnacle = pyqtSignal(dict)
    signal_to_send_bet_parameter_to_fonbet = pyqtSignal(dict)

            # сигнал проставления первого плеча
    signal_do_first_bet_fonbet = pyqtSignal(list)

            # сигнал проставления второго плеча
    signal_do_second_bet_pinnacle = pyqtSignal(list)

            # сигнал переход на стартовую страницу
    signal_start_page_pinnacle = pyqtSignal()
    signal_start_page_fonbet = pyqtSignal()

            # тествые сигналы (потом убрать)
    signal_test_report_fonbet = pyqtSignal()
    signal_test_do_bet_pinnacle = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

        #self.page_bk_settings = PagesSettingsBK()
        #self.betting_settings = BettingSettings()
        #self.general_settings_widget = GeneralSettings()
        self.bet_bk_settings_is_saved = False
        self.bet_filter_settings_is_saved = False
        self.bet_settings_is_saved = False

        self.auto_betting = True

        self.black_list = []
        self.white_list = []

        self.first_data_is_ready = False

    def setupUi(self):
        self.setWindowTitle("Сканер вилок с автоматизированным проставлением")
        self.setFixedSize(1600, 800)

        ##########  Панель на левой кройке программы ###############
        helpToolBar = QToolBar("Help", self)
        helpToolBar.setFixedWidth(120)

        self.bot_btn = QPushButton('Бот')
        self.bot_btn.clicked.connect(self.open_bot_widget)
        helpToolBar.addWidget(self.bot_btn)
        helpToolBar.addSeparator()

        self.bookmakers_settings_btn = QPushButton('Букмекеры')
        self.bookmakers_settings_btn.clicked.connect(self.open_bookmakers_settings)
        helpToolBar.addWidget(self.bookmakers_settings_btn)
        helpToolBar.addSeparator()

        self.bet_settings_btn = QPushButton('Ставки')
        self.bet_settings_btn.clicked.connect(self.open_set)
        helpToolBar.addWidget(self.bet_settings_btn)
        helpToolBar.addSeparator()

        self.general_settings_btn = QPushButton('Общие \nнастройки')
        self.general_settings_btn.clicked.connect(self.open_general_settings)
        helpToolBar.addWidget(self.general_settings_btn)

        helpToolBar.setMovable(False)

        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

        # test zone
        self.btn_check_all_settings = QPushButton('Проверить \n настройки')
        #self.btn_check_all_settings.clicked.connect(self.start_octo_brawser)
        #self.btn_check_all_settings.clicked.connect(self.get_all_settings)
        helpToolBar.addSeparator()
        helpToolBar.addWidget(self.btn_check_all_settings)

        ##########  Верхний menubar ###############
        # создаем menubar
        self.menu = self.menuBar()
        self.start_menu = self.menu.addMenu("&Начало")
        self.settings_menu = self.menu.addMenu("&Настройки")
        self.help_menu = self.menu.addMenu("&Помощь")

        ########## Основное окно ###############
        # создаем widget который помещаем на главное окно
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # добавляем слой к виджету
        layout = QVBoxLayout()
        self.centralWidget.setLayout(layout)
        # создаем слой, в который будем помещать оазные виджеты
        self.stackedLayout = QStackedLayout()

        # Создаем виджет со сканером вилок (и управлением проставления)
        self.bot_widget = BotWindow(self)
        self.stackedLayout.addWidget(self.bot_widget)
        # Создаем виджет с настройками букмекеров
        self.bk_settings = PagesSettingsBK(self)
        self.stackedLayout.addWidget(self.bk_settings)
        # Создаем виджет со сканером вилок (и управлением проставления)
        self.betting_settings = BettingSettings(self)
        self.stackedLayout.addWidget(self.betting_settings)
        # Создаем виджет с общими настройками
        self.general_settings_widget = GeneralSettings(self)
        self.stackedLayout.addWidget(self.general_settings_widget)

        layout.addLayout(self.stackedLayout)

        # таймер окончания паузы после успешной ставки
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_start_scanner)


    def do_first_bet(self):

        first_bet_name = self.bot_widget.fork_now['BK1_bet']
        second_bet_name = self.bot_widget.fork_now['BK2_bet']
        bet_type = self.bot_widget.fork_now['bet_type']

        # определяем первую контору
        self.first_bk, self.first_cf, self.first_limit, \
        self.second_bk, self.second_cf, self.second_limit = order_of_betting(first_bk=self.first_bk,
                                                                             first_cf=self.first_cf,
                                                                             first_limit=self.first_limit,
                                                                             second_bk=self.second_bk,
                                                                             second_cf=self.second_cf,
                                                                             second_limit=self.second_limit,
                                                                             first_bet_name=first_bet_name,
                                                                             second_bet_name=second_bet_name,
                                                                             bet_type=bet_type,
                                                                             how_do_total=self.how_betting_total,
                                                                             how_do_handicap=self.how_betting_handicap)
        #bet_sum = self.get_first_bet_sum() ПОЛУЧАЕМ СУММУ ПО СЛОВАРЮ ИЛИ КАК_ТО ПРИДУМАТЬ
        bet_sum = self.fonbet_fix_bet
        exchange_rate = self.fonbet_exchange_rate
        another_exchange_rate = self.pinnacle_exchange_rate
        #####
        #bet_sum = 1000
        #exchange_rate = 1
        #another_exchange_rate = 60


        # проверяем подходит ли нам вилка
        self.is_fork_fit = is_fork_fit(bet_sum=bet_sum, bet_limit=self.first_limit, bet_cf=self.first_cf,
                                       exchange_rate=exchange_rate, another_limit=self.second_limit,
                                       another_cf=self.second_cf, another_exchange_rate=another_exchange_rate,
                                       min_profit=self.min_profit, max_profit=self.max_profit,
                                       min_cf=self.min_cf, max_cf=self.max_cf)
        if not self.is_fork_fit:
            print('Вилка не подходит')
            self.error_in_getting_data()
            return      # сброс ботов, начало сканера

        # начинаем проставлять первое плечо
        # потом добавить if name == "контора"

        print('Начинаем проставлять плечо')

        data_to_betting = [bet_sum, exchange_rate, self.second_limit, self.second_cf,
                           another_exchange_rate, self.min_profit, self.max_profit,
                           self.min_cf, self.max_cf]

        print('Данные для проставления фонбет:', data_to_betting)

        if self.first_bk == 'fonbet':
            print('Ставим фонбет. Отправка сигнала')
            self.signal_do_first_bet_fonbet.emit(data_to_betting)
        if self.first_bk == 'ggbet':
            print('Ставим ггбет, доработать.')
        if self.first_bk == 'pinnacle':
            print('Ставим пинку, доработать.')

        #data_to_betting = [bet_sum, exchange_rate, self.second_limit, self.second_cf,
        #                   another_exchange_rate, self.min_profit, self.max_profit,
        #                   self.min_cf, self.max_cf]
        #print('Данные для проставления фонбет:', data_to_betting)
        #self.signal_do_first_bet_fonbet.emit(data_to_betting)



    def do_second_bet(self, data):
        first_bet_sum = data[0]
        first_cf = data[1]
        first_exchange_rate = self.fonbet_exchange_rate
        exchange_rate = self.pinnacle_exchange_rate
        seconds_do_bet = self.time_second_bet
        loose_max = self.procent_loose
        """first_exchange_rate = 1
        exchange_rate = 60
        seconds_do_bet = 10
        loose_max = 10"""

        print('Посылаю сигнал во вторую контору')
        data_to_betting = [first_cf, first_bet_sum, first_exchange_rate, exchange_rate, seconds_do_bet, loose_max]
        print('Данные для проставления пинакл:', data_to_betting)

        if self.second_bk == 'pinnacle':
            print('Проставляю второе плечо на пинке. Посылаю сигнал.')
            self.signal_do_second_bet_pinnacle.emit(data_to_betting)

        if self.second_bk == 'fonbet':
            print('Проставляю второе плечо на фонбете. Доработать...')

        if self.second_bk == 'ggbet':
            print('Проставляю второе плечо на ггбет. Доработать...')

        #print('Посылаю сигнал во вторую контору')
        #data_to_betting = [first_cf, first_bet_sum, first_exchange_rate, exchange_rate, seconds_do_bet, loose_max]
        #print('Данные для проставления пинакл:', data_to_betting)
        #self.signal_do_second_bet_pinnacle.emit(data_to_betting)

    def error_in_getting_data(self):
        print('ошибка в получении данных')
        #################### signal_start_page_pinnacle
        #first_bk = self.bot_widget.fork_now['BK1_name']
        #second_bk = self.bot_widget.fork_now['BK2_name']
        first_bk = 'fonbet'
        second_bk = 'pinnacle'
        if first_bk == 'fonbet' or second_bk == 'fonbet':
            print('Рестарт фонбет')
            # time.sleep(2)
        if first_bk == 'ggbet' or second_bk == 'ggbet':
            print('Рестарт ггбет')
            # time.sleep(2)
        if first_bk == 'pinnacle' or second_bk == 'pinnacle':
            print('Рестарт пиннакле')
            #time.sleep(2)
        self.signal_start_page_pinnacle.emit()
        time.sleep(2)
        self.signal_start_page_fonbet.emit()

        print('Заданное время: ', self.pause_time)
        time_to_scanner = 30 * 1000         # В последствии после 30 сек меняем на вводимые параметры
        print('Пауза после проставления')
        self.timer.start(time_to_scanner)
        return

    def fork_is_done(self):
        print('Главное окно, ставки сделаны, перехожу в режим ожидания')
        first_bk = self.bot_widget.fork_now['BK1_name']
        second_bk = self.bot_widget.fork_now['BK2_name']
        if first_bk == 'fonbet' or second_bk == 'fonbet':
            print('Рестарт фонбет')
            # time.sleep(2)
        if first_bk == 'ggbet' or second_bk == 'ggbet':
            print('Рестарт ггбет')
            # time.sleep(2)
        if first_bk == 'pinnacle' or second_bk == 'pinnacle':
            print('Рестарт пиннакле')
            # time.sleep(2)
        self.signal_start_page_pinnacle.emit()
        time.sleep(2)
        self.signal_start_page_fonbet.emit()

        print('Заданное время: ', self.pause_time)
        time_to_scanner = self.pause_time * 1000
        print('Пауза после проставления')
        self.timer.start(time_to_scanner)
        return

    def timer_start_scanner(self):
        print('Пауза окончена')
        self.bot_widget.btn_scaner_start.click()
        self.timer.stop()

    def cf_and_limit_is_get(self, data):
        # пришли коэффициенты с бк
        if self.first_data_is_ready:
            self.second_bk = data[0]
            self.second_cf = data[1]
            self.second_limit = data[2]
            print('Получил данные от второй конторы:', self.second_bk)
            print(self.second_cf, '  ', self.second_limit)
            print(type(self.second_cf), '  ', type(self.second_limit))

            # проверка вилки и проставление
            self.do_first_bet()

            self.first_data_is_ready = False
        else:
            self.first_data_is_ready = True
            self.first_bk = data[0]
            self.first_cf = data[1]
            self.first_limit = data[2]
            print('Получил данные от первой конторы:', self.first_bk)
            print(self.first_cf, '  ', self.first_limit)
            print(type(self.first_cf), '  ', type(self.first_limit))

    # Запуск браузеров в потоке
    def open_ggbet_driver(self):
        self.ggbet_thread = QThread()
        self.ggbet_driver = ggbetDriver()
        self.ggbet_driver.moveToThread(self.ggbet_thread)
        self.ggbet_thread.started.connect(self.ggbet_driver.doWebDriver)
        # сигнал начала функции открытия купона
        self.signal_to_send_bet_parameter_to_ggbet.connect(self.ggbet_driver.do_bet)

        self.ggbet_thread.start()


    def open_pinnacle_driver(self):
        self.pinnacle_thread = QThread()
        self.pinnacle_driver = pinnacleDriver()
        self.pinnacle_driver.moveToThread(self.pinnacle_thread)
        self.pinnacle_thread.started.connect(self.pinnacle_driver.doWebDriver)
        # сигнал начала функции открытия купона
        self.signal_to_send_bet_parameter_to_pinnacle.connect(self.pinnacle_driver.do_bet)
        # сигнал с кф и лимитом ставки (посылается в main window)
        self.pinnacle_driver.signal_with_cf_and_bet_limit.connect(self.cf_and_limit_is_get)
        # сигнал проставления второго плеча
        self.signal_do_second_bet_pinnacle.connect(self.pinnacle_driver.second_betting)
        # сигнал о ошибке в получении данных
        self.pinnacle_driver.signal_error_in_getting_data.connect(self.error_in_getting_data)
        # сигнал перехода на главный экран
        self.signal_start_page_pinnacle.connect(self.pinnacle_driver.go_to_start_page)
        # сигнал о удачном проставлении второго плеча
        self.pinnacle_driver.signal_second_bet_is_done.connect(self.fork_is_done)

        # тестовые сигналы проверить betting report и проставление
        self.signal_test_do_bet_pinnacle.connect(self.pinnacle_driver.test_funct_do_bet_report)

        self.pinnacle_thread.start()

    def open_fonbet_driver(self):
        self.fonbet_thread = QThread()
        self.fonbet_driver = fonbetDriver()
        self.fonbet_driver.moveToThread(self.fonbet_thread)
        self.fonbet_thread.started.connect(self.fonbet_driver.doWebDriver)
        # сигнал начала функции открытия купона
        self.signal_to_send_bet_parameter_to_fonbet.connect(self.fonbet_driver.do_bet)
        # сигнал с кф и лимитом ставки (посылается в main window)
        self.fonbet_driver.signal_with_cf_and_bet_limit.connect(self.cf_and_limit_is_get)
        # сигнал проставления первого плеча
        self.signal_do_first_bet_fonbet.connect(self.fonbet_driver.betting_first)
        # сигнал при завершении проставления первого плеча
        self.fonbet_driver.signal_first_bet_is_done.connect(self.do_second_bet)
        # сигнал о ошибке в получении данных
        self.fonbet_driver.signal_error_in_getting_data.connect(self.error_in_getting_data)
        # сигнал перехода на главный экран
        self.signal_start_page_fonbet.connect(self.fonbet_driver.go_to_start_page)

        # тестовые сигналы проверить betting report
        self.signal_test_report_fonbet.connect(self.fonbet_driver.get_betting_report)


        self.fonbet_thread.start()

    def save_black_white_list(self):
        self.black_list = self.general_settings_widget.black_white_list_settings.black_list_words
        self.white_list = self.general_settings_widget.black_white_list_settings.white_list_words

    def save_filter_settings(self):
        self.list_sport_name = self.general_settings_widget.bet_filter_settings.list_sport_name
        self.list_bet_type = self.general_settings_widget.bet_filter_settings.list_bet_type
        self.how_betting_total = self.general_settings_widget.bet_filter_settings.how_betting_total
        self.how_betting_handicap = self.general_settings_widget.bet_filter_settings.how_betting_handicap

        self.bet_filter_settings_is_saved = True

    def save_bet_settings(self):
        self.min_profit = self.betting_settings.min_profit
        self.max_profit = self.betting_settings.max_profit
        self.min_cf = self.betting_settings.min_cf
        self.max_cf = self.betting_settings.max_cf
        self.min_lifetime = self.betting_settings.min_lifetime
        self.max_lifetime = self.betting_settings.max_lifetime
        self.time_second_bet = self.betting_settings.time_second_bet
        self.pause_time = self.betting_settings.pause_time
        self.procent_loose = self.betting_settings.procent_loose
        self.count_forks_in_match = self.betting_settings.count_forks_in_match

        self.bet_settings_is_saved = True

    def save_bk_settings(self):
        # получаем какие бк ставить
        self.wich_bk_list = self.bk_settings.wich_bk_list

        # считываем данные по кноторам
        if "ggbet" in self.wich_bk_list:
            self.ggbet_link = self.bk_settings.ggbet_link
            self.ggbet_login = self.bk_settings.ggbet_login
            self.ggbet_password = self.bk_settings.ggbet_password
            self.ggbet_min_balance = self.bk_settings.ggbet_min_balance
            self.ggbet_exchange_rate = self.bk_settings.ggbet_exchange_rate
            self.ggbet_is_first = self.bk_settings.ggbet_is_first
            self.ggbet_fix_bet = self.bk_settings.ggbet_fix_bet
            self.ggbet_uuid = self.bk_settings.ggbet_uuid

        if "pinnacle" in self.wich_bk_list:
            self.pinnacle_link = self.bk_settings.pinnacle_link
            self.pinnacle_login = self.bk_settings.pinnacle_login
            self.pinnacle_password = self.bk_settings.pinnacle_password
            self.pinnacle_min_balance = self.bk_settings.pinnacle_min_balance
            self.pinnacle_exchange_rate = self.bk_settings.pinnacle_exchange_rate
            self.pinnacle_is_first = self.bk_settings.pinnacle_is_first
            self.pinnacle_fix_bet = self.bk_settings.pinnacle_fix_bet
            self.pinnacle_uuid = self.bk_settings.pinnacle_uuid

        if "fonbet" in self.wich_bk_list:
            self.fonbet_link = self.bk_settings.fonbet_link
            self.fonbet_login = self.bk_settings.fonbet_login
            self.fonbet_password = self.bk_settings.fonbet_password
            self.fonbet_min_balance = self.bk_settings.fonbet_min_balance
            self.fonbet_exchange_rate = self.bk_settings.fonbet_exchange_rate
            self.fonbet_is_first = self.bk_settings.fonbet_is_first
            self.fonbet_fix_bet = self.bk_settings.fonbet_fix_bet
            self.fonbet_uuid = self.bk_settings.fonbet_uuid

        self.start_octo_brawser()
        self.bet_bk_settings_is_saved = True

    def start_octo_brawser(self):
        print('Список выбранных контор:', self.wich_bk_list)
        if 'fonbet' in self.wich_bk_list:
            print('открываю Фонбет')
            self.open_fonbet_driver()
            time.sleep(2)

        if 'ggbet' in self.wich_bk_list:
            print('открываю ГГБЕТ')
            self.open_ggbet_driver()
            time.sleep(2)

        if 'pinnacle' in self.wich_bk_list:
            print('открываю Пинку')
            self.open_pinnacle_driver()
            time.sleep(2)


    def open_bot_widget(self, checked):
        self.stackedLayout.setCurrentIndex(0)

    def open_bookmakers_settings(self, checked):
        self.stackedLayout.setCurrentIndex(1)

    def open_set(self, checked):
        self.stackedLayout.setCurrentIndex(2)

    def open_general_settings(self, checked):
        self.stackedLayout.setCurrentIndex(3)

    def closeEvent(self, event):
        print('Выхожу')
        event.accept()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())