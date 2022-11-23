from AllLibraries import *

class BettingSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Параметры ставок")
        self.is_settings_saved = False
        self.main_window = parent

        # общий слой
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Зона с ползунками (доходность, коэффициенты, время жизни)
        groupbox_rules = QtWidgets.QGroupBox()
        groupbox_rules.setTitle('Правила')
        rules_layout = QGridLayout()

        # Минимальная доходность
        self.min_profit_label = QLabel('Минимальная доходность (в %):')
        self.min_profit_slider = QSlider(Qt.Horizontal)
        self.min_profit_slider.setMaximum(100)
        #self.min_profit_slider.setFixedWidth(400)
        self.min_profit_slider.setSingleStep(1)
        self.min_profit_slider.setValue(0)
        self.min_profit_slider.valueChanged.connect(
            lambda: self.slider_profit_changed(self.min_profit_txt, self.min_profit_slider)
        )
        self.min_profit_txt = QLineEdit()
        self.min_profit_txt.setFixedWidth(70)
        self.min_profit_txt.setText('0')
        self.min_profit_txt.editingFinished.connect(
            lambda: self.txt_profit_changed(self.min_profit_txt, self.min_profit_slider)
        )

        # Максимальная доходность по вилке
        self.max_profit_label = QLabel('Максимальная доходность (в %):')
        self.max_profit_slider = QSlider(Qt.Horizontal)
        self.max_profit_slider.setMaximum(100)
        #self.max_profit_slider.setFixedWidth(400)
        self.max_profit_slider.setSingleStep(1)
        self.max_profit_slider.setValue(100)
        self.max_profit_slider.valueChanged.connect(
            lambda: self.slider_profit_changed(self.max_profit_txt, self.max_profit_slider)
        )
        self.max_profit_txt = QLineEdit()
        self.max_profit_txt.setFixedWidth(70)
        self.max_profit_txt.setText('100')
        self.max_profit_txt.editingFinished.connect(
            lambda: self.txt_profit_changed(self.max_profit_txt, self.max_profit_slider)
        )

        # минимальный коэффициент
        self.min_cf_label = QLabel('Минимальный коэффициент:')
        self.min_cf_slider = QSlider(Qt.Horizontal)
        self.min_cf_slider.setMaximum(291)
        #self.min_cf_slider.setFixedWidth(400)
        self.min_cf_slider.setSingleStep(1)
        self.min_cf_slider.setValue(1)
        self.min_cf_slider.valueChanged.connect(
            lambda: self.slider_cf_changed(self.min_cf_slider, self.min_cf_txt)
        )
        self.min_cf_txt = QLineEdit()
        self.min_cf_txt.setFixedWidth(70)
        self.min_cf_txt.setText('1.1')
        self.min_cf_txt.editingFinished.connect(
            lambda: self.txt_cf_changed(self.min_cf_txt, self.min_cf_slider)
        )

        # максимальный коэффициент
        self.max_cf_label = QLabel('Максимальный коэффициент:')
        self.max_cf_slider = QSlider(Qt.Horizontal)
        self.max_cf_slider.setMaximum(300)
        #self.max_cf_slider.setFixedWidth(400)
        self.max_cf_slider.setSingleStep(1)
        self.max_cf_slider.setValue(75)
        self.max_cf_slider.valueChanged.connect(
            lambda: self.slider_cf_changed(self.max_cf_slider, self.max_cf_txt)
        )
        self.max_cf_txt = QLineEdit()
        self.max_cf_txt.setFixedWidth(70)
        self.max_cf_txt.setText('8.5')
        self.max_cf_txt.editingFinished.connect(
            lambda: self.txt_cf_changed(self.max_cf_txt, self.max_cf_slider)
        )

        # Минимальное время жизни вилки
        self.min_lifetime_label = QLabel('Минимальное время жизни вилки (сек.):')
        self.min_lifetime_slider = QSlider(Qt.Horizontal)
        self.min_lifetime_slider.setMaximum(181)
        #self.min_lifetime_slider.setFixedWidth(400)
        self.min_lifetime_slider.setSingleStep(1)
        self.min_lifetime_slider.setValue(1)
        self.min_lifetime_slider.valueChanged.connect(
            lambda: self.slider_lifetime_changed(self.min_lifetime_txt ,self.min_lifetime_slider)
        )
        self.min_lifetime_txt = QLineEdit()
        self.min_lifetime_txt.setFixedWidth(70)
        self.min_lifetime_txt.setText('1')
        self.min_lifetime_txt.editingFinished.connect(
            lambda: self.txt_lifetime_changed(self.min_lifetime_txt, self.min_lifetime_slider)
        )

        # Максимальное время жизни вилки
        self.max_lifetime_label = QLabel('Максимальное время жизни (сек.):')
        self.max_lifetime_slider = QSlider(Qt.Horizontal)
        self.max_lifetime_slider.setMaximum(181)
        #self.max_lifetime_slider.setFixedWidth(400)
        self.max_lifetime_slider.setSingleStep(1)
        self.max_lifetime_slider.setValue(180)
        self.max_lifetime_slider.valueChanged.connect(
            lambda: self.slider_lifetime_changed(self.max_lifetime_txt, self.max_lifetime_slider)
        )
        self.max_lifetime_txt = QLineEdit()
        self.max_lifetime_txt.setFixedWidth(70)
        self.max_lifetime_txt.setText('180')
        self.max_lifetime_txt.editingFinished.connect(
            lambda: self.txt_lifetime_changed(self.max_lifetime_txt, self.max_lifetime_slider)
        )


        rules_layout.addWidget(self.min_profit_label, 0, 0)
        rules_layout.addWidget(self.min_profit_slider, 0, 1)
        rules_layout.addWidget(self.min_profit_txt, 0, 2)

        rules_layout.addWidget(self.max_profit_label, 1, 0)
        rules_layout.addWidget(self.max_profit_slider, 1, 1)
        rules_layout.addWidget(self.max_profit_txt, 1, 2)

        rules_layout.addWidget(self.min_cf_label, 2, 0)
        rules_layout.addWidget(self.min_cf_slider, 2, 1)
        rules_layout.addWidget(self.min_cf_txt, 2, 2)

        rules_layout.addWidget(self.max_cf_label, 3, 0)
        rules_layout.addWidget(self.max_cf_slider, 3, 1)
        rules_layout.addWidget(self.max_cf_txt, 3, 2)

        rules_layout.addWidget(self.min_lifetime_label, 4, 0)
        rules_layout.addWidget(self.min_lifetime_slider, 4, 1)
        rules_layout.addWidget(self.min_lifetime_txt, 4, 2)

        rules_layout.addWidget(self.max_lifetime_label, 5, 0)
        rules_layout.addWidget(self.max_lifetime_slider, 5, 1)
        rules_layout.addWidget(self.max_lifetime_txt, 5, 2)
        groupbox_rules.setLayout(rules_layout)
        layout.addWidget(groupbox_rules)

        # Ограничения
        groupbox_terms = QtWidgets.QGroupBox()
        groupbox_terms.setTitle('Ограничения')
        terms_layout = QGridLayout()

        # Максимальное время перекрытия 2ого плеча
        self.second_bet_spin = QSpinBox(self)
        self.second_bet_spin.setSuffix("  сек")
        self.second_bet_spin.setValue(10)
        self.second_bet_spin.setValue(600)
        self.second_bet_spin.setFixedWidth(200)


        # Пауза после успешной вилки
        self.pause_spin = QSpinBox(self)
        self.pause_spin.setSuffix("  сек")
        self.pause_spin.setValue(60)
        self.pause_spin.setMaximum(10000)
        self.pause_spin.setFixedWidth(200)

        # Максимальный процент потерь, с которым разрешено ставить
        self.procent_spin = QSpinBox(self)
        self.procent_spin.setSuffix("  %")
        self.procent_spin.setValue(5)
        self.procent_spin.setMaximum(99)
        self.procent_spin.setFixedWidth(200)

        # Максимальное кол-во вилок в матче
        self.forks_max_spin = QSpinBox(self)
        self.forks_max_spin.setSuffix("  шт")
        self.forks_max_spin.setValue(5)
        self.forks_max_spin.setMaximum(100)
        self.forks_max_spin.setFixedWidth(200)

        terms_layout.addWidget(QLabel('Макс. перекрытие 2ого плеча: '),0,0)
        terms_layout.addWidget(self.second_bet_spin, 1, 0)
        terms_layout.addWidget(QLabel('Пауза после  успешной ставки: '), 0, 1)
        terms_layout.addWidget(self.pause_spin, 1, 1)
        terms_layout.addWidget(QLabel('Макс. разрешенные потери: '), 0, 2)
        terms_layout.addWidget(self.procent_spin, 1, 2)
        terms_layout.addWidget(QLabel('Макс вилок в матче: '), 2, 0)
        terms_layout.addWidget(self.forks_max_spin, 3, 0)

        groupbox_terms.setLayout(terms_layout)
        layout.addWidget(groupbox_terms)

        self.btn_save_settings = QPushButton('Сохранить настройки')
        self.btn_save_settings.clicked.connect(self.save_settings)
        layout.addWidget(self.btn_save_settings)

    def save_settings(self):

        self.min_profit = int(float(self.min_profit_txt.text()))
        self.max_profit = int(float(self.max_profit_txt.text()))
        self.min_cf = self.transform_max_value(self.min_cf_txt.text())
        self.max_cf = self.transform_max_value(self.max_cf_txt.text())
        self.min_lifetime = int(self.transform_max_value(self.min_lifetime_txt.text()))
        self.max_lifetime = int(self.transform_max_value(self.max_lifetime_txt.text()))
        self.time_second_bet = self.second_bet_spin.value()
        self.pause_time = self.pause_spin.value()
        self.procent_loose = self.procent_spin.value()
        self.count_forks_in_match = self.forks_max_spin.value()

        self.is_settings_saved = True
        self.report = QMessageBox.information(self, "Успех", "Данные успешно сохранены")

        self.main_window.save_bet_settings()


    def transform_max_value(self, value):

        if value == 'MAX':
            return 100000
        else:
            return float(value)

    def txt_profit_changed(self, txt_line, slider):
        txt_value = txt_line.text()
        slider_value = slider.value()
        try:
            txt_value = float(txt_value)
        except:
            txt_line.setText(str(slider_value))
            return

        if txt_value > 100:
            txt_value = 100
            txt_line.setText(str(100))
        if txt_value != slider_value:
            slider.setValue(int(txt_value))
            return
        else:
            return

    def slider_profit_changed(self, txt_line, slider):
        slider_value = slider.value()
        txt_line.setText(str(slider_value))


    def txt_cf_changed(self, txt_line, slider):
        txt_value = txt_line.text()
        slider_value = slider.value()
        if not txt_value:
            if slider_value > 290:
                txt_line.setText('MAX')
            else:
                txt_line.setText(str(slider_value / 10 + 1))
            return
        if txt_value == 'MAX':
            if slider_value != 291:
                slider.setValue(291)
            return
        try:
            txt_value = int((float(txt_value) - 1) * 10)
        except:
            if slider_value > 291:
                txt_line.setText('MAX')
            else:
                txt_line.setText(str(slider_value / 10 + 1))
            return

        if txt_value == slider_value:
            return

        if txt_value > 291:
            slider.setValue(291)
            txt_line.setText('MAX')
        else:
            slider.setValue(txt_value)


    def slider_cf_changed(self, slider, txt_line):
        value_now = slider.value()
        if value_now > 290:
            txt_line.setText('MAX')
            return
        value_now = (value_now) / 10 + 1
        txt_line.setText(str(value_now))

    def txt_lifetime_changed(self, txt_line, slider):
        txt_value = txt_line.text()
        slider_value = slider.value()
        try:
            txt_value = int(float(txt_value))
        except:
            txt_line.setText(str(slider_value))
            return

        if txt_value > 180:
            txt_value = 180
            txt_line.setText('Max')
        if txt_value != slider_value:
            slider.setValue(int(txt_value))
            return
        else:
            return

    def slider_lifetime_changed(self, txt_line, slider):
        value_now = slider.value()
        if value_now > 180:
            txt_line.setText('MAX')
            return
        else:
            txt_line.setText(str(value_now))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BettingSettings()
    window.show()
    sys.exit(app.exec())
