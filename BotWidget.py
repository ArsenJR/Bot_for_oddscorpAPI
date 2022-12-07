from AllLibraries import *
from ForkScanerClass import *
import ForkScanerClass
from GetToOddscorp import *

class BotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bot")

        self.main_window = parent
        self.auto_betting = True
        #self.auto_betting = False
        self.count_successful_in_match = {}
        self.list_done_fork_id = []

        self.listView = QtWidgets.QListView(self)
        self.listView.setGeometry(QtCore.QRect(350, 50, 1050, 670))
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

        self.btn_open_octo = QtWidgets.QPushButton('Кнопка для тестов', self)
        self.btn_open_octo.setGeometry(QtCore.QRect(80, 400, 200, 30))
        self.btn_open_octo.setObjectName("btn_clear_list")
        self.btn_open_octo.setEnabled(True)
        self.btn_open_octo.clicked.connect(self.test_func)

        self.btn_open_octo2 = QtWidgets.QPushButton('Кнопка для тестов 2', self)
        self.btn_open_octo2.setGeometry(QtCore.QRect(80, 300, 200, 30))
        self.btn_open_octo2.setEnabled(True)
        self.btn_open_octo2.clicked.connect(self.test_func2)

        # создаем кнопку окончания работы сканера
        self.btn_scaner_end = QtWidgets.QPushButton('Закончить сканирование', self)
        self.btn_scaner_end.setGeometry((QtCore.QRect(80, 500, 200, 30)))
        self.btn_scaner_end.setObjectName('btn_scaner_end')
        self.btn_scaner_end.clicked.connect(self.scanerEnd)
        #self.btn_scaner_end.setEnabled(False)

        # создаем кнопку начало сканирования
        self.btn_scaner_start = QtWidgets.QPushButton('Начать сканирование', self)
        self.btn_scaner_start.setGeometry(QtCore.QRect(80, 600, 200, 30))
        self.btn_scaner_start.setObjectName("btn_start_scan")
        self.btn_scaner_start.clicked.connect(self.start_scaner)
        #self.btn_scaner_start.clicked.connect(self.scanerStartInThread)
        #self.btn_scaner_start.setEnabled(False)


        # кнопка "Сделать ставку"
        self.btn_do_bet = QtWidgets.QPushButton('Сделать ставку', self)
        self.btn_do_bet.setGeometry(QtCore.QRect(80, 700, 200, 30))
        self.btn_do_bet.setObjectName("btn_do_bet")
        #self.btn_do_bet.setEnabled(False)
        self.btn_do_bet.clicked.connect(self.do_bet)


    def test_func(self):
        #self.main_window.open_fonbet_driver()
        #self.main_window.open_pinnacle_driver()
        self.main_window.open_ggbet_driver()
        #self.btn_open_octo.setEnabled(False)

        #self.main_window.get_bet_sum_and_ex_rate('gg_bet', 'pinnacle')



    def test_func2(self):
        print('Second')

        #self.main_window.signal_test_do_bet_pinnacle.emit()
        #self.main_window.signal_do_first_bet_ggbet.emit([500, 1, 100, 5.1, 60, 1, 300, 1.1, 8.5])
        self.main_window.signal_test_do_bet_ggbet.emit(50)


    def start_scaner(self):
        #           Добавит проверку на кол-во вилок в матче

        if not self.main_window.bet_bk_settings_is_saved:
            self.error = QMessageBox.critical(self, "Ошибка", "Заполните настройки Букмекеров")
            return
        if not self.main_window.bet_filter_settings_is_saved:
            self.error = QMessageBox.critical(self, "Ошибка", "Заполните Общие настройки")
            return
        if not self.main_window.bet_settings_is_saved:
            self.error = QMessageBox.critical(self, "Ошибка", "Заполните настройки 'Ставки'")
            return
        if not self.main_window.order_ruels_is_saved:
            self.error = QMessageBox.critical(self, "Ошибка", "Заполните настройки 'Правила проставления'")
            return
        self.wich_bk_list = ['pinnacle', 'fonbet', 'gg_bet']       # в последствии считывать
        #self.wich_bk_list = self.main_window.wich_bk_list

        print(f'Диапазон прибыли: {self.main_window.min_profit} - {self.main_window.max_profit}')
        print(f'Диапазон коэффициентов: {self.main_window.min_cf} - {self.main_window.max_cf}')
        print(f'Диапазон прибыли: {self.main_window.min_lifetime} - {self.main_window.max_lifetime}')
        print(f'Заданные виды спорта: {self.main_window.list_sport_name}')
        print(f'Заданные типы ставок: {self.main_window.list_bet_type}')
        print(f'черный лист: {self.main_window.black_list}')
        print(f'Белый лист: {self.main_window.white_list}')
        print('Список контор: ', self.wich_bk_list)


        self.main_windowfirst_data_is_ready = False
        # Дальше запускаем сканерz
        self.scanerStartInThread()

    def do_bet(self):

        fork = self.get_fork_data()
        if not fork:
            print('Выберите ставку')
            return False
        self.scanerEnd()
        self.main_window.first_data_is_ready = False
        print('Отправляю сигнал')
        self.main_window.signal_to_send_bet_parameter_to_ggbet.emit(fork)
        #self.main_window.signal_to_send_bet_parameter_to_pinnacle.emit(fork)
        #time.sleep(2)
        #self.test_func2()
        #self.main_window.signal_to_send_bet_parameter_to_fonbet.emit(fork)


    def get_fork_data(self):
        print()
        name = None
        indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
        if indef_of_selected_item:
            text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
            text_selected_items = " | ".join(text_selected_items.split(' | ')[:-1])
            name = text_selected_items
            print(name)
        else:
            name = None
            return False

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
                            return fork_for_bet
            except:
                return None

    def scanerEnd(self):
        ForkScanerClass.CHEK = False

    def scanerStartInThread(self):

        self.main_window.first_data_is_ready = False
        self.fork_now = None

        if self.auto_betting:
            self.is_auto_work = True
        else:
            self.is_auto_work = False

        ForkScanerClass.CHEK = True

        # добавить автомтатический перебор вилок (из Юпитера)

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
            lambda: self.model.removeRows(0, self.model.rowCount())
        )


    def reportProgress(self, n):
        fork_now, fork_alive_now, forks_data = n

        # автоматическое проставление
        if self.is_auto_work:
            self.auto_scan_forks(forks_data)

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

    def get_fork_for_bet(self):
        name = None
        indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
        if indef_of_selected_item:
            text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
            #text_selected_items = " | ".join(text_selected_items.split(' | ')[:-1])
            name = text_selected_items
            print(name)
        else:
            print('Выберите ставку')

        return ''

        # далее добавить вторую часть ф-кции

    def auto_scan_forks(self, fork_list):

        for fork in fork_list:

            if not self.is_auto_work:
                return
            if not self.is_fork_in_white_list(fork):
                print('Не прошел по белому листу')
                continue

            if self.is_fork_in_black_list(fork):
                print('Не прошел по черному листу')
                continue

            """if self.is_bk_fit(fork['BK1_name'], fork['BK2_name']):
                #print('Не ставим!')
                continue"""

            if fork['sport'] not in self.main_window.list_sport_name:
                #print('Тип спорта не входит в заданные значения')
                continue
            #### wich_bk_list
            if fork['BK1_name'] not in self.wich_bk_list:
                print('Не подходит  первая бк', fork['BK1_name'])
                continue

            if fork['BK2_name'] not in self.wich_bk_list:
                print('Не подходит вторая бк', fork['BK2_name'])
                continue

            if fork['bet_type'] not in self.main_window.list_bet_type:
                print('Не подходит тип ставки', fork['bet_type'])
                continue

            if fork['alive_sec'] < self.main_window.min_lifetime or fork['alive_sec'] > self.main_window.max_lifetime:
                print('Время вилки не подходит')
                continue

            if fork['BK1_cf'] < self.main_window.min_cf or fork['BK1_cf'] > self.main_window.max_cf or fork['BK2_cf'] < self.main_window.min_cf or fork['BK2_cf'] > self.main_window.max_cf:
                print('Коэффициент не подходит')
                continue

            if fork['income'] < self.main_window.min_profit or fork['income'] > self.main_window.max_profit:
                print('Прибыль не подходит')
                continue

            if self.is_bk_fit(fork['BK1_name'], fork['BK2_name']):
                print('Не ставим!')
                print(fork['BK1_name'], fork['BK2_name'])
                continue

            print('Начинаем проставлять вилку')
            print('return')
            print(fork)
            self.is_auto_work = False
            self.fork_now = fork
            #self.settings_info = QMessageBox.information(self, "Информация!", 'Нашел вилку')
            print('Нашел вилку')
            if fork['BK1_name'] == 'pinnacle' or fork['BK2_name'] == 'pinnacle':
                print('Отправляю сигнао в pinnacle driver для открытия купона')
                self.main_window.signal_to_send_bet_parameter_to_pinnacle.emit(fork)
                time.sleep(2)
            if fork['BK1_name'] == 'gg_bet' or fork['BK2_name'] == 'gg_bet':
                print('Отправляю сигнао в ggbet driver для открытия купона')
                self.main_window.signal_to_send_bet_parameter_to_ggbet.emit(fork)
                time.sleep(2)
            if fork['BK1_name'] == 'fonbet' or fork['BK2_name'] == 'fonbet':
                print('Отправляю сигнао в fonbet driver для открытия купона')
                self.main_window.signal_to_send_bet_parameter_to_fonbet.emit(fork)
                time.sleep(2)

            #self.main_window.signal_to_send_bet_parameter_to_pinnacle.emit(fork)
            #time.sleep(2)
            #self.main_window.signal_to_send_bet_parameter_to_fonbet.emit(fork)
            self.btn_scaner_end.click()
            return


    def is_bk_fit(self, first_bk, second_bk):
        #print('Проверка пары бк')
        all_pairs = self.main_window.dict_order_ruels.keys()
        bk_pair_01 = first_bk + ' - ' + second_bk
        bk_pair_02 = second_bk + ' - ' + first_bk

        if bk_pair_01 in all_pairs:
            if self.main_window.dict_order_ruels[bk_pair_01] != 'None':
                print('Пара проставляется(список)')
                return False
            else:
                #print('Пара не проставляется (список)')
                return True
        elif bk_pair_02 in all_pairs:
            if self.main_window.dict_order_ruels[bk_pair_02] != 'None':
                print('Пара проставляется (список)')
                return False
            else:
                #print('Пара не проставляется (список)')
                return True
        else:
            #print('Пара не найдена (в списоке)')
            return True

    def is_fork_in_black_list(self, fork):

        first_league_name = fork['BK1_league'].split(' ')
        second_league_name = fork['BK2_league'].split(' ')

        first_game_name = fork['BK1_game'].split(' ')
        second_game_name = fork['BK2_game'].split(' ')

        if not self.main_window.black_list:
            return False

        if self.is_word_in_list(self.main_window.black_list, first_league_name) or self.is_word_in_list(self.main_window.black_list, second_league_name):
            return True
        if self.is_word_in_list(self.main_window.black_list, first_game_name) or self.is_word_in_list(self.main_window.black_list, second_game_name):
            return True

        return False

    def is_fork_in_white_list(self, fork):

        first_league_name = fork['BK1_league'].split(' ')
        second_league_name = fork['BK2_league'].split(' ')

        first_game_name = fork['BK1_game'].split(' ')
        second_game_name = fork['BK2_game'].split(' ')

        if not self.main_window.white_list:
            return True

        if self.is_word_in_list(self.main_window.white_list, first_league_name) or self.is_word_in_list(self.main_window.white_list, second_league_name):
            return True
        if self.is_word_in_list(self.main_window.white_list, first_game_name) or self.is_word_in_list(self.main_window.white_list, second_game_name):
            return True

        return False

    def is_word_in_list(self, key_list, words):

        for word in words:
            if word in key_list:
                return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotWindow()
    window.show()
    sys.exit(app.exec())