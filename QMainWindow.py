from ForkScanerClass import *
import ForkScanerClass
from QDialodToLogin import *
import QDialodToLogin
from SetParamToBetting import *
import SetParamToBetting
from GGBetDriver import *
from PinnacleDriver import *
from GetToOddscorp import *


class Window(QMainWindow, QObject, object):

    signal_to_logIn_ggbet = pyqtSignal(list)
    signal_to_logIn_pinnacle = pyqtSignal(list)
    signal_to_send_bet_parameter_to_ggbet = pyqtSignal(dict)
    signal_to_send_bet_parameter_to_pinnacle = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Forks scaner")
        self.resize(1200, 700)
        # создаем для обращение к окну приложения
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Создаем listView для вывода информации о ставках
        self.listView = QtWidgets.QListView(self.centralWidget)
        self.listView.setGeometry(QtCore.QRect(300, 20, 830, 600))
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

        # кнопка открывабщая окно с настройками
        self.btn_set_settings = QtWidgets.QPushButton('Настройки', self)
        self.btn_set_settings.setGeometry(QtCore.QRect(70, 210, 200, 30))
        self.btn_set_settings.setObjectName("btn_set_settings")
        self.btn_set_settings.clicked.connect(self.open_settings_dialog)

        # кнопка открывабщая новое окно (для Log in)
        self.btn_bk_logIn = QtWidgets.QPushButton('Авторизоваться', self)
        self.btn_bk_logIn.setGeometry(QtCore.QRect(70, 310, 200, 30))
        self.btn_bk_logIn.setObjectName("btn_bk_logIn")
        self.btn_bk_logIn.clicked.connect(self.open_logIn_dialog)

        # создаем кнопку окончания работы сканера
        self.btn_scaner_end = QtWidgets.QPushButton('Закончить сканирование', self)
        self.btn_scaner_end.setGeometry((QtCore.QRect(70, 410, 200, 30)))
        self.btn_scaner_end.setObjectName('btn_scaner_end')
        self.btn_scaner_end.clicked.connect(self.scanerEnd)
        self.btn_scaner_end.setEnabled(False)

        # создаем кнопку начало сканирования
        self.btn_scaner_start = QtWidgets.QPushButton('Начать сканирование', self)
        self.btn_scaner_start.setGeometry(QtCore.QRect(70, 510, 200, 30))
        self.btn_scaner_start.setObjectName("btn_start_scan")
        self.btn_scaner_start.clicked.connect(self.scanerStartInThread)

        # кнопка открывабщая новое окно (для Log in)
        self.btn_do_bet = QtWidgets.QPushButton('Сделать ставку', self)
        self.btn_do_bet.setGeometry(QtCore.QRect(70, 610, 200, 30))
        self.btn_do_bet.setObjectName("btn_do_bet")
        #self.btn_do_bet.setEnabled(False)
        self.btn_do_bet.clicked.connect(self.do_bet)

        # открываем автоматизированные вкладки с бк
        self.open_ggbet_driver()
        self.open_pinnacle_driver()

    def open_settings_dialog(self):
        self.scanerEnd()
        dialog = DialogSettings(self)
        if dialog.exec():
            print('Данные получены!')
        else:
            print('Cansel!')


    def do_bet(self):
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
            except:
                print("Вилка пропала")


    def open_pinnacle_driver(self):
        self.pinnacle_thread = QThread()
        self.pinnacle_driver = pinnacleDriver()
        self.pinnacle_driver.moveToThread(self.pinnacle_thread)
        self.pinnacle_thread.started.connect(self.pinnacle_driver.doWebDriver)
        self.signal_to_logIn_pinnacle.connect(self.pinnacle_driver.log_in)
        self.signal_to_send_bet_parameter_to_pinnacle.connect(self.pinnacle_driver.do_bet)


        self.pinnacle_thread.start()


    def open_ggbet_driver(self):
        self.ggbet_thread = QThread()
        self.ggbet_driver = ggbetDriver()
        self.ggbet_driver.moveToThread(self.ggbet_thread)
        self.ggbet_thread.started.connect(self.ggbet_driver.doWebDriver)
        self.signal_to_logIn_ggbet.connect(self.ggbet_driver.log_in)
        self.signal_to_send_bet_parameter_to_ggbet.connect(self.ggbet_driver.do_bet)

        self.ggbet_thread.start()

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




    def reportProgress(self, n):
        fork_now, fork_alive_now  = n

        #получаем выбранный эллемент
        indef_of_selected_item = self.listView.selectionModel().selectedIndexes()
        # получаем текст выбранного эллемента
        name = None
        if indef_of_selected_item:
            text_selected_items = self.model.itemFromIndex(indef_of_selected_item[0]).text()
            text_selected_items = " | ".join(text_selected_items.split(' | ')[:-1])
            name = text_selected_items

        self.model.removeRows(0,self.model.rowCount())
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
            lambda: self.model.removeRows(0, self.model.rowCount())
        )





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())