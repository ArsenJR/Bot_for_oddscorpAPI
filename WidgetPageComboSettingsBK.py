from AllLibraries import *
from WidgetBkSettings import WidgetSettingBK

PINNACLE_PORT = None
FONBET_PORT = None
GGBET_PORT = None

PINNACLE_LINK = None
FONBET_LINK = None
GGBET_LINK = None

class PagesSettingsBK(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настроки букмекеров")

        self.is_settings_saved = False
        self.main_window = parent

        # Create a top-level layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        helpToolBar = QToolBar("Help")

        self.check_fonbet = QCheckBox('Fonbet')
        # self.bot_btn.clicked.connect(self.open_bot_widget)
        helpToolBar.addWidget(self.check_fonbet)
        helpToolBar.addSeparator()
        self.check_ggbet = QCheckBox('GGBet')
        # self.bot_btn.clicked.connect(self.open_bot_widget)
        helpToolBar.addWidget(self.check_ggbet)
        helpToolBar.addSeparator()
        self.check_pinnacle = QCheckBox('Pinnacle')
        # self.bot_btn.clicked.connect(self.open_bot_widget)
        helpToolBar.addWidget(self.check_pinnacle)
        helpToolBar.addSeparator()
        helpToolBar.setMovable(False)
        helpToolBar.setOrientation(Qt.Vertical)
        main_layout.addWidget(helpToolBar)

        layout = QVBoxLayout()
        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Pinnacle", "GGBet", "Fonbet"])
        self.pageCombo.activated.connect(self.switchPage)

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        # Create the first page
        self.pinnacle_settings = WidgetSettingBK()
        self.stackedLayout.addWidget(self.pinnacle_settings)
        # Create the second page
        self.ggbet_settings = WidgetSettingBK()
        self.stackedLayout.addWidget(self.ggbet_settings)

        self.fonbet_settings = WidgetSettingBK()
        self.stackedLayout.addWidget(self.fonbet_settings)

        # Add the combo box and the stacked layout to the top-level layout
        layout.addWidget(self.pageCombo)
        layout.addLayout(self.stackedLayout)

        # кнопка сохраняющая настройки букмекеров
        self.btn_save_bk_settings = QPushButton('Соранить')
        self.btn_save_bk_settings.clicked.connect(self.save_bk_settings)
        layout.addWidget(self.btn_save_bk_settings)

        main_layout.addLayout(layout)

    def save_bk_settings(self):
        self.is_settings_saved = False
        self.ggbet_uuid = None
        self.pinnacle_uuid = None
        self.fonbet_uuid = None
        self.wich_bk_list = []

        global PINNACLE_PORT, FONBET_PORT, GGBET_PORT, PINNACLE_LINK, FONBET_LINK, GGBET_LINK
        PINNACLE_PORT = None
        FONBET_PORT = None
        GGBET_PORT = None

        PINNACLE_LINK = None
        FONBET_LINK = None
        GGBET_LINK = None

        if self.check_ggbet.isChecked():
            self.wich_bk_list.append('ggbet')
        if self.check_pinnacle.isChecked():
            self.wich_bk_list.append('pinnacle')
        if self.check_fonbet.isChecked():
            self.wich_bk_list.append('fonbet')

        if len(self.wich_bk_list) < 2:
            self.error = QMessageBox.critical(self, "Ошибка!", 'Необходимо выбрать минимум двух букмекеров')
            return

        if "ggbet" in self.wich_bk_list:
            self.ggbet_settings.save_settings('GGBet')
            if self.ggbet_settings.is_settings_saved:
                self.ggbet_link = self.ggbet_settings.link
                self.ggbet_login = self.ggbet_settings.login
                self.ggbet_password = self.ggbet_settings.password
                self.ggbet_min_balance = self.ggbet_settings.min_balabce
                self.ggbet_exchange_rate = self.ggbet_settings.rate
                self.ggbet_is_first = self.ggbet_settings.is_betting_first
                self.ggbet_fix_bet = self.ggbet_settings.bet_sum
                self.ggbet_uuid = self.ggbet_settings.uuid
                GGBET_PORT = self.ggbet_uuid
                GGBET_LINK = self.ggbet_link

            else:
                return

        if "pinnacle" in self.wich_bk_list:
            self.pinnacle_settings.save_settings('Pinnacle')
            if self.pinnacle_settings.is_settings_saved:
                self.pinnacle_link = self.pinnacle_settings.link
                self.pinnacle_login = self.pinnacle_settings.login
                self.pinnacle_password = self.pinnacle_settings.password
                self.pinnacle_min_balance = self.pinnacle_settings.min_balabce
                self.pinnacle_exchange_rate = self.pinnacle_settings.rate
                self.pinnacle_is_first = self.pinnacle_settings.is_betting_first
                self.pinnacle_fix_bet = self.pinnacle_settings.bet_sum
                self.pinnacle_uuid = self.pinnacle_settings.uuid
                PINNACLE_PORT = self.pinnacle_uuid
                PINNACLE_LINK = self.pinnacle_link

                print('pinnacle: ', self.pinnacle_uuid)

                if self.pinnacle_uuid == self.ggbet_uuid:
                    self.error = QMessageBox.critical(self, "Ошибка!", 'Выбрали один профиль в окто для двух букмекеров')
                    return
            else:
                return

        if "fonbet" in self.wich_bk_list:
            self.fonbet_settings.save_settings('Fonbet')
            if self.fonbet_settings.is_settings_saved:
                self.fonbet_link = self.fonbet_settings.link
                self.fonbet_login = self.fonbet_settings.login
                self.fonbet_password = self.fonbet_settings.password
                self.fonbet_min_balance = self.fonbet_settings.min_balabce
                self.fonbet_exchange_rate = self.fonbet_settings.rate
                self.fonbet_is_first = self.fonbet_settings.is_betting_first
                self.fonbet_fix_bet = self.fonbet_settings.bet_sum
                self.fonbet_uuid = self.fonbet_settings.uuid
                FONBET_PORT = self.fonbet_uuid
                FONBET_LINK = self.fonbet_link

                print('Fonbet: ', self.fonbet_uuid)
                if self.fonbet_uuid == self.ggbet_uuid or self.fonbet_uuid == self.pinnacle_uuid:
                    self.error = QMessageBox.critical(self, "Ошибка!", 'Выбрали один профиль в окто для двух букмекеров')
                    return
            else:
                return
        # Открываем порты
        self.report = QMessageBox.information(self, "Успех", "Данные успешно сохранены")
        self.is_settings_saved = True
        self.main_window.save_bk_settings()

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PagesSettingsBK()
    window.show()
    sys.exit(app.exec())