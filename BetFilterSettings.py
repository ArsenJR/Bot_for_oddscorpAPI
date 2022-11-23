from AllLibraries import *

class BetFilter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтр настроек")

        self.is_settings_saved = False
        self.main_window = parent

        # общий слой
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Фильтр (выбор видов спорта)
        groupbox_filter = QtWidgets.QGroupBox()
        groupbox_filter.setTitle('Фильтр')
        filter_layout = QGridLayout()

        # Check box с видами спорта
        self.check_csgo = QtWidgets.QCheckBox('CS GO')
        self.check_dota = QtWidgets.QCheckBox('DOTA 2')
        self.check_lol = QtWidgets.QCheckBox('LOL')

        filter_layout.addWidget(QLabel('Виды спорта:'), 0, 0)
        filter_layout.addWidget(self.check_csgo, 1, 0)
        filter_layout.addWidget(self.check_dota, 1, 1)
        filter_layout.addWidget(self.check_lol, 1, 2)

        # Check box с вдами ставок
        self.check_win = QtWidgets.QCheckBox('WIN')
        self.check_totals = QtWidgets.QCheckBox('TOTALS')
        self.check_handicap = QtWidgets.QCheckBox('HANDICAP')

        filter_layout.addWidget(QLabel('Типы ставок:'), 2, 0)
        filter_layout.addWidget(self.check_win, 3, 0)
        filter_layout.addWidget(self.check_totals, 3, 1)
        filter_layout.addWidget(self.check_handicap, 3, 2)

        groupbox_filter.setLayout(filter_layout)
        layout.addWidget(groupbox_filter)

        # Правила очередности
        groupbox_priority = QtWidgets.QGroupBox()
        groupbox_priority.setTitle('Правила очередности')
        priority_layout = QGridLayout()

        # Правило проставления ТОТАЛ
        priority_layout.addWidget(QLabel('Тотал: '), 0, 0)
        self.total_btn_more = QRadioButton('Больше')
        self.total_btn_less = QRadioButton('Меньше')
        self.total_btn_default = QRadioButton('По умолчанию')
        self.total_btn_default.setChecked(True)
        self.total_group = QButtonGroup(self)
        self.total_group.addButton(self.total_btn_more)
        self.total_group.addButton(self.total_btn_less)
        self.total_group.addButton(self.total_btn_default)

        priority_layout.addWidget(self.total_btn_more, 0, 2)
        priority_layout.addWidget(self.total_btn_less, 0, 3)
        priority_layout.addWidget(self.total_btn_default, 0, 4)

        #priority_layout.addWidget(QLabel(' '), 1, 0)
        # Правило проставления фора
        priority_layout.addWidget(QLabel('Фора: '), 1, 0)
        self.handicap_btn_positive = QRadioButton('Положительная')
        self.handicap_btn_negative = QRadioButton('Отрицательная')
        self.handicap_btn_default = QRadioButton('По умолчанию')
        self.handicap_btn_default.setChecked(True)
        self.handicap_group = QButtonGroup(self)
        self.handicap_group.addButton(self.handicap_btn_positive)
        self.handicap_group.addButton(self.handicap_btn_negative)
        self.handicap_group.addButton(self.handicap_btn_default)

        priority_layout.addWidget(self.handicap_btn_positive, 1, 2)
        priority_layout.addWidget(self.handicap_btn_negative, 1, 3)
        priority_layout.addWidget(self.handicap_btn_default, 1, 4)

        groupbox_priority.setLayout(priority_layout)
        layout.addWidget(groupbox_priority)

        self.btn_save_settings = QPushButton('Сохранить настройки')
        self.btn_save_settings.clicked.connect(self.save_settings)
        layout.addWidget(self.btn_save_settings)

    def save_settings(self):
        print('Saved')

        self.is_settings_saved = False

        self.list_sport_name = []
        self.list_bet_type = []

        # считываем данные по выбранным вида спорта
        if self.check_csgo.isChecked():
            self.list_sport_name.append('esports.cs')
        if self.check_dota.isChecked():
            self.list_sport_name.append('esports.dota2')
        if self.check_lol.isChecked():
            self.list_sport_name.append('esports.lol')

        if not self.list_sport_name:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите вид спорта.')
            return

        # считываем данные по выбранным типам ставок
        if self.check_win.isChecked():
            self.list_bet_type.append('WIN')
            self.list_bet_type.append('SET_WIN')
        if self.check_totals.isChecked():
            self.list_bet_type.append('SETS_TOTALS')
            self.list_bet_type.append('SET_TOTALS')
            self.list_bet_type.append('TOTALS')
        if self.check_handicap.isChecked():
            self.list_bet_type.append('HANDICAP')
            self.list_bet_type.append('SETS_HANDICAP')
            self.list_bet_type.append('SET_HANDICAP')


        if not self.list_bet_type:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Выберите тип ставки.')
            return

        # порядок проставления тотала
        if self.total_btn_more.isChecked():     # первым ставить тотал больше
            self.how_betting_total = 2
        elif self.total_btn_less.isChecked():   # первым ставить тотал меньше
            self.how_betting_total = 1
        else:
            self.how_betting_total = 0               # согласно начальным настройкам

        # порядок проставления форы
        if self.handicap_btn_positive.isChecked():
            self.how_betting_handicap = 2
        elif self.handicap_btn_negative.isChecked():
            self.how_betting_handicap = 1
        else:
            self.how_betting_handicap = 0

        self.is_settings_saved = True
        self.report = QMessageBox.information(self, "Успех", "Данные успешно сохранены")

        self.main_window.save_filter_settings()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BetFilter()
    window.show()
    sys.exit(app.exec())
