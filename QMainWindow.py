from ForkScanerClass import *
import ForkScanerClass


class Window(QMainWindow, QObject, object):

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