from AllLibraries import *
from BetFilterSettings import BetFilter
from BlackWhiteListSettings import BlackWhiteList

class GeneralSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Общие настроки")
        self.main_window = parent

        # ВЕРХНИЙ СЛОЙ
        layout = QVBoxLayout()
        self.setLayout(layout)
        # переход между страницами
        self.pageCombo = QComboBox()
        self.pageCombo.addItems(["Фильтр", "Ключевые слова"])
        self.pageCombo.activated.connect(self.switchPage)
        # Create the stacked layout
        self.stackedLayout = QStackedLayout()
        # первая страница
        self.bet_filter_settings = BetFilter(self)
        self.stackedLayout.addWidget(self.bet_filter_settings)

        # Вторая страница
        self.black_white_list_settings = BlackWhiteList(self)
        self.stackedLayout.addWidget(self.black_white_list_settings)

        layout.addWidget(self.pageCombo)
        layout.addLayout(self.stackedLayout)

    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())

    def save_filter_settings(self):
        self.main_window.save_filter_settings()
    def save_black_white_list(self):
        self.main_window.save_black_white_list()

    def get_data(self):
        if self.bet_filter_settings.is_settings_saved:
            return self.bet_filter_settings.list_sport_name,\
                   self.bet_filter_settings.list_bet_type,\
                   self.bet_filter_settings.how_betting_total,\
                   self.bet_filter_settings.how_betting_handicap, \
                   self.black_white_list_settings.black_list_words, \
                   self.black_white_list_settings.white_list_words
        else:
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GeneralSettings()
    win.show()
    sys.exit(app.exec())