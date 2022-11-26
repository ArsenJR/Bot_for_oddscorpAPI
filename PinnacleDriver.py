import time

from AllLibraries import *
import WidgetPageComboSettingsBK

PINNACLE_PORT = ''
PINNACLE_LINK = ''


class pinnacleDriver(QObject):
        # сигнал с полученными кф и лимитам
    signal_with_cf_and_bet_limit = pyqtSignal(list)
        # сигнал с ошибкой открытия купона
    signal_error_in_getting_data = pyqtSignal()

        # сигнал с инфо о ставке (при проставлении второго плеча)
    signal_second_bet_is_done = pyqtSignal(list)


    #signal_error_in_getting_data = pyqtSignal()
    #signal_first_bet_is_done = pyqtSignal(list)

    #signal_error_in_betting = pyqtSignal()
    #signal_stop_scaner = pyqtSignal()

    def doWebDriver(self):

        self.update_list = 0
        #### ИЗМЕНИТЬ ПРИ РАБОТЕ ПРОГРАММЫ ####
        #self.profile_id = PINNACLE_PORT
        self.profile_id = '423ab8dbaa7547f0b97ef35ac72457e1'
        self.profile_id = WidgetPageComboSettingsBK.PINNACLE_PORT
        print('Fonbet: Заданная ссылка -', WidgetPageComboSettingsBK.PINNACLE_LINK)
        # self.bk_link = PINNACLE_LINK
        self.bk_link = 'https://www.skynotes.bond/ru/'
        self.port = get_debug_port(self.profile_id)
        self.driver = get_webdriver(self.port)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                const newProto = navigator.__proto__
                delete newProto.webdriver
                navigator.__proto__ = newProto
                """
        })
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.wait_error_webpage = WebDriverWait(self.driver, 20)
        self.driver.get(self.bk_link)


        key_element = 'style_selected__FPAJz undefined style_selected__FPAJz'
        # self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="{}"]'.format(key_element))))





    def log_in(self, login_password):
        login = login_password[0]
        password = login_password[1]

        # раскрываем бк на полный экран
        self.log_in_link = self.bk_link + 'account/login'
        self.driver.get(self.log_in_link)

        # находим поля для ввода логина и пороля
        username_lable = self.driver.find_element(By.XPATH, '//input[@name="username"]')
        password_lable = self.driver.find_element(By.XPATH, '//input[@name="password"]')

        # вводим логин и пороль
        username_lable.clear()
        username_lable.send_keys(login)

        password_lable.clear()
        password_lable.send_keys(password)
        time.sleep(1)
        password_lable.send_keys(Keys.ENTER)
        self.wait.until(EC.visibility_of_element_located((By.ID, "all")))


    def do_bet(self, dict):

        self.update_count = 0
        self.bet_parameter = dict

        self.bet_parameter = {
            'fork_id': '52bf84d9c1ed1d62a3',
            'income': 1.51,
            'ow_income': 0,
            'sport': 'esports.cs',
            'bet_type': 'WIN',
            'event_id': '16093728',
            'is_middles': '0',
            'is_cyber': '1',
            'BK1_bet': 'WIN__P1',
            'BK1_bet_type': 'WIN',
            'BK1_alt_bet': '',
            'BK1_cf': 1.31,
            'BK1_event_id': 'GGGEC83DB3B892AE',
            'BK1_event_native_id': '5:f0c05042-4b0f-4052-bce5-4c4a220ab4cc',
            'BK1_game': 'Team Finest vs MASONIC',
            'BK1_href': 'https://gg.bet/ru/esports/match/natus-vincere-vs-bad-news-eagles-07-11-1',
            'BK1_league': 'Elisa Invitational Fall 2022',
            'BK1_name': 'gg_bet',
            'BK1_score': '1:0',
            'BK1_event_meta': '{"start_at":1663848000}',
            'BK1_market_meta': '{"title_name":"Победитель","bet_name":"Natus Vincere"}',
            'BK2_bet': 'SET_01__WIN__P1',
            'BK2_bet_type': 'SET_WIN',
            'BK2_alt_bet': '',
            'BK2_cf': 4.51,
            'BK2_event_id': 'PINECA347B908FF3',
            'BK2_event_native_id': '1559705902',
            'BK2_game': 'Finest vs MASONIC',
            'BK2_href': 'https://www.skynotes.bond/ru/esports/csgo-intel-extreme-masters-rio-major/outsiders-vs-heroic/1563129926',
            'BK2_league': 'CS:GO - Elisa Invitational',
            'BK2_name': 'pinnacle',
            'BK2_score': '',
            'BK2_event_meta': '{"league_id":208956,"start_at":1663847880}',
            'BK2_market_meta': '{"key":"s;0;m","market_name":"moneyline","dest":"away","matchup_id":1559708853,"league_id":208956,"parent_id":1559705902,"participant_id":null,"is_special":false}',
            'alive_sec': 0
        }

        self.bet_parameter = dict

        if self.bet_parameter['BK1_name'] == 'pinnacle':
            bet_href = self.bet_parameter['BK1_href']
            bet_type = self.bet_parameter['BK1_bet_type']
            bet_name = self.bet_parameter['BK1_bet']
        elif self.bet_parameter['BK2_name'] == 'pinnacle':
            bet_href = self.bet_parameter['BK2_href']
            bet_type = self.bet_parameter['BK2_bet_type']
            bet_name = self.bet_parameter['BK2_bet']

        sport_type = self.bet_parameter['sport']

        print('Pinnacle:   Получил вилку')
        bet_link = self.get_match_link(self.bk_link, bet_href)

        #bet_type = 'MAP__HANDICAP'
        #bet_name = 'MAP_1__HANDICAP__P2(2.5)'
        #bet_link = 'https://www.betonproxy.shop/ru/esports/csgo-esl-pro-league/liquid-vs-movistar-riders/1557069066'

        try:
            self.driver.minimize_window()
            self.driver.maximize_window()

            self.driver.get(bet_link)
        except:
            self.driver.get(bet_link)
            self.driver.minimize_window()
            self.driver.maximize_window()



        # дожидаемся прогрузки страницы
        key_loading = 'style_button__3llZm'
        try:
            WebDriverWait(self.driver, 4).until(
                EC.visibility_of_element_located((By.XPATH, '//button[@class="{}"]'.format(key_loading))))
        except:
            print('Pinnacle:  Не дождался кнопки "Все"')
            #self.signal_error_in_getting_data.emit()
            #return

        #### нажимаем кнопку "ВСЕ"
        page_btns = self.driver.find_elements(By.XPATH, '//button[@class="{}"]'.format(key_loading))
        our_btn = None
        for page in page_btns:
            try:
                print(page.text)
                if page.text == 'Все' or page.text == 'ВСЕ':
                    our_btn = page
                    print('Pinnacle - Нашли вкладку "ВСЕ"')
                    break
            except:
                pass
        if our_btn:
            our_btn.click()
            print('Pinnacle - Открыл вкладку "ВСЕ"')
        else:
            print('Pinnacle - Не удалось открыть все ставки')
            return
        ####

        try:
            print("Ищем поле")
            self.bets_field = self.get_field_by_name(bet_type, bet_name, sport_type)
            print('Pinnacle:   Поле найдено')
        except:
            print('Pinnacle:   Не удалось найти поле со ставкой')
            self.signal_error_in_getting_data.emit()
            return
        try:
            print('Пытаюсь закрыть купон')
            self.try_close_cupons()
            print(bet_type)
            if bet_type == 'SET_WIN' or bet_type == 'WIN':
                self.do_win_bet(bet_name, self.bets_field, sport_type)
                print('Pinnacle:   Открыл купон')
            if bet_type == 'SETS_TOTALS' or bet_type == 'TOTALS' or bet_type == 'SET_TOTALS':
                print('Делаю тотал')
                self.do_total_bet(bet_name, self.bets_field, sport_type)
                print('Pinnacle:   Открыл купон')
            if bet_type == 'HANDICAP' or bet_type == 'SETS_HANDICAP' or bet_type == 'SET_HANDICAP':
                print('Делаю ставку фора')
                self.do_handicap_bet(bet_name, self.bets_field)
                print('Pinnacle:   Открыл купон')

            self.get_cf_and_bet_sum()

            self.cf = float(self.cf)
            print(f'Pinnacle:   {self.cf}, {self.bet_limit}')
            self.bet_limit = float(self.bet_limit.replace('USD', ' ').replace('RUB', ' ').replace(' ', '').replace(',', '.'))
            print(self.bet_limit)
            self.signal_with_cf_and_bet_limit.emit(['pinnacle', self.cf, self.bet_limit])
        except:
            print('Pinnacle:   Не получилось поставить!(((')
            self.signal_error_in_getting_data.emit()




    def try_close_cupons(self):
        key_btn_delete_all = 'icon-trash-bin'
        key_accept_delete_all = 'style_yes__2hRbu'

        try:
            btn_delete_all = self.driver.find_element(By.XPATH, '//i[@class="{}"]'.format(key_btn_delete_all))
        except:
            btn_delete_all = None
        if btn_delete_all:
            btn_delete_all.click()

            btn_accept_delete_all = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_accept_delete_all))
            btn_accept_delete_all.click()
        return

    def get_cf_and_bet_sum(self):

        key_max_bet_sum = 'Betslip-StakeWinInput-MaxWagerLimit'
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-test-id="{}"]'.format(key_max_bet_sum))))
        except:
            '''  Переделать на отправку сигнала об ошибке в сборе данных '''
            self.signal_error_in_getting_data.emit()
            return

        self.bet_limit = self.driver.find_element(By.XPATH, '//a[@data-test-id="{}"]'.format(key_max_bet_sum)).text

        key_cf_value = 'style_price__1pYJK betslipCardPrice'

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="{}"]'.format(key_cf_value))))
        self.cf = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_cf_value)).text



    def get_match_link(self, url_bk, url_match):
        return url_bk + "/".join(url_match.split('/')[4:])

    def get_field_by_name(self, bet_type, bet, sport_type):

        # ключ области каждого вида ставок
        field_class_name = 'style_primary__1bqk9 style_marketGroup__1z6ED'
        # ключи названия типа ставки
        key_bet_type = 'style_titleText__1NKyr'

        # открываем все виды ставок
        self.open_all_bets()

        # находим области каждого вида ставок
        bet_fields = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(field_class_name))

        # получаем нужное название поля со ставкой
        our_bet_type_name = self.pinnacle_get_field_name(bet_type, bet, sport_type)
        print(f'Pinnacle: ищем  {our_bet_type_name}')

        # находим название (тип ставки) каждого поля и получаем нужное поле
        for bet_field in bet_fields:
            bet_type_name = bet_field.find_element(By.XPATH, './/span[@class="{}"]'.format(key_bet_type)).text
            if bet_type_name == str(our_bet_type_name):
                fields_with_our_bet = bet_field
                break
        return fields_with_our_bet

    def pinnacle_get_field_name(self, bet_type, bet_name, sport_type):
        print('Начинаю подбирать имя поля')
        fields_name_dict = {
            'WIN':'Денежная линия – Матч',
            'SET_01_WIN':'Денежная линия – Карта 1',
            'SET_02_WIN':'Денежная линия – Карта 2',
            'SET_03_WIN':'Денежная линия – Карта 3',
            'SET_04_WIN':'Денежная линия – Карта 4',
            'SET_05_WIN':'Денежная линия – Карта 5',
            'SETS_TOTALS':'Тотал – Матч',
            'TOTALS': 'Тотал',  # ЕЩЁ НЕ ВСТРЕЧАЛ
            'SET_01_TOTALS':'Тотал – Карта 1',
            'SET_02_TOTALS':'Тотал – Карта 2',
            'SET_03_TOTALS':'Тотал – Карта 3',
            'SET_04_TOTALS':'Тотал – Карта 4',
            'SET_05_TOTALS':'Тотал – Карта 5',
            'SETS_HANDICAP':'Гандикап – Матч',
            'SET_01_HANDICAP':'Гандикап – Карта 1',
            'SET_02_HANDICAP':'Гандикап – Карта 2',
            'SET_03_HANDICAP':'Гандикап – Карта 3',
            'SET_04_HANDICAP':'Гандикап – Карта 4',
            'SET_05_HANDICAP':'Гандикап – Карта 5',
        }
        if sport_type == 'soccer':
            fields_name_dict = {
                'WIN' : 'Денежная линия – Матч',
                'TOTALS' : 'Тотал – Матч',
            }
        if sport_type == 'tennis':
            fields_name_dict = {
                'WIN' : 'Денежная линия (Сеты) – Матч',
                'TOTALS' : 'Тотал (геймы) – Матч',
            }

            # Разбиваем строку на массив слов (роль разделителя - подчеркивание)
            # и соединяем массив в строку без последнего эллемента
        bet_field = '_'.join(bet_name.replace('__', ' ').replace('_', ' ').replace('  ', ' ').split(' ')[:-1])
        print('Pinnacle - получаю имя поля:', bet_field)
        try:
            field_name = fields_name_dict[bet_field]
            print('Pinnacle возвращаю: ', field_name)
        except:
            field_name = None
            print(bet_field)

        return field_name

    def open_all_bets(self):
        # ключ кнопки "посмотреть все рынки"
        #key_to_open_all_bets = 'style_button__2cht5 style_fullWidth__tyxzD ellipsis style_medium__1Uf0e dead-center style_tertiary__1XC1Z all-markets-btn style_button__2Wms9'
        key_to_open_all_bets = 'style_button__27Bgy style_fullWidth__INYTu ellipsis style_medium__2kpGi dead-center style_tertiary__3tFWt all-markets-btn style_button__2mnbC'

        # нажимаем кнопку посмотреть все рынки
        try:
            button_open_all_bets = self.driver.find_element(By.XPATH,
                                                            '//button[@class="{}"]'.format(key_to_open_all_bets))
            button_open_all_bets.click()
        except:
            pass

    def do_win_bet(self, BK_bet, fields_with_our_bet, sport):

        # имя класса элемента с названием команд
        class_name = 'style_participantName__3pj60'  # lable

        bet = ('__').join(BK_bet.replace('__', " ").replace("_", " ").split(' ')[-2:])

        # если это победа 1ого или 2ого (или весь матч, или за часть)
        # если за часть, то поле fields_with_our_bet будет со ставками на победу в выбранном периоде
        # получаем имя команды, на которую будем ставить

        if bet == 'WIN__P1':
            command_name = self.driver.find_elements(By.CLASS_NAME, class_name)[0].text
        elif bet == 'WIN__P2':
            command_name = self.driver.find_elements(By.CLASS_NAME, class_name)[1].text
        if sport == 'tennis':
            command_name += ' (Сеты)'
        # в поле с нашей ставкой ищем кнопку со свойством title = command_name
        self.button_with_our_bet = fields_with_our_bet.find_element(By.XPATH, './/button[@title="{}"]'.format(command_name))
        self.button_with_our_bet.click()

    def do_total_bet(self, BK_bet, fields_with_our_bet, sport):
        # ключ копки 'отображать больше'
        key_button_image_more = 'style_toggleMarkets__2pyyw'

        try:
            button_image_more = fields_with_our_bet.find_element(By.XPATH, './/button[@class="{}"]'.format(
                key_button_image_more))
            button_image_more.click()
        except:
            pass
        if BK_bet[0] == 'S':
            BK_bet_name = self.transform_total_bet(BK_bet)
        elif BK_bet[0] == 'T':
            BK_bet_name = self.transform_total_bet2(BK_bet)
        if sport == 'tennis':
            BK_bet_name += ' геймы'

        self.button_with_our_bet = fields_with_our_bet.find_element(By.XPATH,
                                                               './/button[@title="{}"]'.format(BK_bet_name))

        self.button_with_our_bet.click()

    def transform_total_bet(self, bet):
        # делаем список слов
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')',
                                                                                                           '').split(
            ' ')
        print('Transform total:', bet_to_transform)
        if bet_to_transform[0] == 'SETS':
            if bet_to_transform[2] == 'UNDER':
                bet_name = 'Меньше {}'.format(bet_to_transform[3])
            if bet_to_transform[2] == 'OVER':
                bet_name = 'Больше {}'.format(bet_to_transform[3])
        if bet_to_transform[0] == 'SET':
            if bet_to_transform[3] == 'UNDER':
                bet_name = 'Меньше {}'.format(bet_to_transform[4])
            if bet_to_transform[3] == 'OVER':
                bet_name = 'Больше {}'.format(bet_to_transform[4])
        print(bet_name)
        return bet_name

    def transform_total_bet2(self, bet):
        # делаем список слов
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')',
                                                                                                           '').split(
            ' ')
        if bet_to_transform[1] == 'UNDER':
            bet_name = 'Меньше {}'.format(bet_to_transform[2])
        if bet_to_transform[1] == 'OVER':
            bet_name = 'Больше {}'.format(bet_to_transform[2])
        return bet_name

    def do_handicap_bet(self, BK_bet, fields_with_our_bet):
        # ключ строки с двумя кнопка (фора)
        key_div_two_fora_bet = 'style_buttonRow__kJ_WC'
        # ключ класса кнопок ставок форы
        key_button_fora_bet = 'market-btn style_button__2DGnQ style_pill__I9z83 style_horizontal__2ylXg'
        # ключ копки 'отображать больше'
        key_button_image_more = 'style_toggleMarkets__2pyyw'
        try:
            self.button_image_more = fields_with_our_bet.find_element(By.XPATH,
                                                                 './/button[@class="{}"]'.format(key_button_image_more))
            self.button_image_more.click()
        except:
            pass
        # получаем значение свойства title кнопки с нужной ставкой
        if BK_bet[0] == 'H':
            BK_bet_name = self.transform_handicap_bet(BK_bet)
        elif BK_bet[0] == 'S':
            BK_bet_name = self.transform_map_handicap_bet(BK_bet)

        print('pinnacle transform фора:', BK_bet_name)


        command = self.get_command_number_in_handicap(BK_bet)
        print('com numb:', command)
        all_fora_div = fields_with_our_bet.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_div_two_fora_bet))

        # если P1
        if command == 0:
            for fora_div in all_fora_div:
                buttons_with_fora = fora_div.find_elements(By.XPATH,
                                                           './/button[@class="{}"]'.format(key_button_fora_bet))
                button_with_fora = buttons_with_fora[0]
                bet_text = button_with_fora.text.split('\n')[0]

                if bet_text == BK_bet_name:
                    self.button_with_our_bet = button_with_fora
                    self.button_with_our_bet.click()
        # если P2
        if command == 1:
            for fora_div in all_fora_div:
                buttons_with_fora = fora_div.find_elements(By.XPATH,
                                                           './/button[@class="{}"]'.format(key_button_fora_bet))
                button_with_fora = buttons_with_fora[1]
                bet_text = button_with_fora.text.split('\n')[0]

                if bet_text == BK_bet_name:
                    self.button_with_our_bet = button_with_fora
                    self.button_with_our_bet.click()

    def get_command_number_in_handicap(self, bet):
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')', '').split(' ')
        print('Трансформ фора:', bet_to_transform)
        if bet_to_transform[0] == 'SET':
            if bet_to_transform[3] == 'P1':
                command_number = 0
            if bet_to_transform[3] == 'P2':
                command_number = 1
        elif bet_to_transform[0] == 'SETS':
            if bet_to_transform[2] == 'P1':
                command_number = 0
            if bet_to_transform[2] == 'P2':
                command_number = 1
        return command_number

    def transform_map_handicap_bet(self, bet):
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')', '').split(' ')
        bet_name = bet_to_transform[len(bet_to_transform) - 1]
        if bet_name[0] != '-':
            bet_name = '+' + bet_name
        return bet_name

    def transform_handicap_bet(self, bet):
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')', '').split(' ')
        bet_name = bet_to_transform[len(bet_to_transform) - 1]
        if bet_name[0] != '-':
            bet_name = '+' + bet_name
        return bet_name

    def get_cf(self):
        key_max_bet_sum = 'Betslip-StakeWinInput-MaxWagerLimit'
        key_cf_value = 'style_price__1pYJK betslipCardPrice'
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-test-id="{}"]'.format(key_max_bet_sum))))
        except:
            print('Pinnacle - Ставка закрыта')
            сf = 1.0
            return сf

        print('Дождался limit')

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="{}"]'.format(key_cf_value))))
            cf = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_cf_value)).text
            cf = float(cf)
            return cf
        except:
            print('Ставка закрыта')
            сf = 1.0
            return сf

    def do_bet_by_sum(self, bet_value):

        try:
            self.button_with_our_bet.click()
            time.sleep(1)
            self.button_with_our_bet.click()
        except:
            pass

        # находим поле и вводим туда сумму ставки
        input_sum_lable = self.driver.find_element(By.XPATH, '//input[@placeholder = "Сумма ставки"]')
        input_sum_lable.clear()
        print(bet_value)
        input_sum_lable.send_keys(bet_value)
        #input_sum_lable.send_keys(1.50)



        time.sleep(1)
        # нажимаем кнопку Поставить
        key_btn_do_bet = 'style_button__27Bgy style_fullWidth__INYTu break-word style_medium__2kpGi dead-center style_primary__28DOG style_button__3MB85'
        btn_do_bet = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_do_bet))
        time.sleep(1)
        btn_do_bet.click()
        try:
            #btn_do_bet.click()
            print()
        except:
            pass
        #time.sleep(5)

    def go_to_start_page(self):
        # пробую закрыть купон
        try:
            self.driver.minimize_window()
            self.driver.maximize_window()
        except:
            try:
                self.driver.minimize_window()
                self.driver.maximize_window()
            except:
                pass

        try:
            key_btn_close_kupon = 'betslip-close-button style_close__3bdcI'
            btn_close_kupon = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_close_kupon))
            btn_close_kupon.click()
        except:
            pass

        try:
            key_btn_close_bet_info = 'betslip-close-button style_close__3bdcI style_close__U1ZAq'
            btn_close_bet_info = self.driver.find_element(By.XPATH,
                                                          '//button[@class="{}"]'.format(key_btn_close_bet_info))
            btn_close_bet_info.click()
        except:
            pass
        try:
            balance_now = self.check_balance()
            print("Pinnacle: balance now -", balance_now)
        except:
            pass

        time.sleep(2)
        self.driver.get(self.bk_link)

        #if balance_now < self.balance_limit:
            #self.signal_stop_scaner.emit()



    def first_betting(self,bet_sum_bet_cf):
        print('Pinnacle: ', bet_sum_bet_cf)
        bet_sum = bet_sum_bet_cf[0]
        bet_kf = bet_sum_bet_cf[1]
        another_bet_kf = bet_sum_bet_cf[2]
        cf_now = self.get_cf()

        new_total_prob = (1 / cf_now) + (1 / another_bet_kf)
        if new_total_prob < 1:
            print('Pinnacle: Ставлю ставку)')
            print(bet_sum)
            self.do_bet_by_sum(bet_sum)
            betting_report_data = self.betting_report()
            print(betting_report_data)
            if betting_report_data:
                const_cf = float(betting_report_data[0])
                const_bet_sum = float(betting_report_data[1].split(' ')[0].replace(',', '.'))

                self.signal_first_bet_is_done.emit([const_cf, const_bet_sum])
                return
            else:
                print('Pinnacle: Ставка не сделана (первое плечо)')
                self.signal_error_in_getting_data.emit()
                return
        else:
            print('Pinnacle: Ставка не сделана (первое плечо)')
            self.signal_error_in_getting_data.emit()

    def second_betting(self, first_bet_data):
        ggbet_cf = float(first_bet_data[0])
        ggbet_sum = float(first_bet_data[1])
        ggbet_exchange_rate = first_bet_data[2]
        exchange_rate = first_bet_data[3]
        seconds_do_bet = first_bet_data[4]
        loose_max = first_bet_data[5]

        self.driver.minimize_window()
        self.driver.maximize_window()

        print('Pinnacle: Получаю коэффициент')
        cf_now = float(self.get_cf())
        try:
            print(cf_now)
        except:
            print('Pinnacle: Не получил кф')

        if cf_now != 1.0:
            new_total_prob = (1 / cf_now) + (1 / ggbet_cf)
        else:
            new_total_prob = 2

        if new_total_prob <= 1:
            print('Pinnacle: Считаю сумму ставки для второго плеча')
            bet_sum = round(((ggbet_sum * ggbet_cf) / cf_now) / exchange_rate)
            print('Pinnacle: Сумма ставки -', bet_sum)
            self.do_bet_by_sum(bet_sum)
            ##### ТЕТСОВАЯ ЗОНА #####
            time.sleep(1)
            try:
                key_btn_do_bet = 'style_button__2cht5 style_fullWidth__tyxzD break-word style_medium__1Uf0e dead-center style_primary__3OVhQ style_button__1TVoo'
                test_btn_do_bet = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_do_bet))

                if test_btn_do_bet:
                    print('Pinnacle: Вижу кнопку поставить')
            except:
                pass
            ##### ------------ #####
            print('Pinnacle:  cтавка сделана')
            betting_params = self.betting_report()
            if betting_params:
                print('Pinnacle: Посылаю результат')
                self.signal_second_bet_is_done.emit(betting_params)
                return
            else:
                #self.signal_error_in_betting.emit()
                print('Pinnacle: Поставил, но купон не прогрузился')
                return
        else:
            print('Pinnacle: Пытаюсь поставить (попытка №2)')
            for i in range(seconds_do_bet):
                time.sleep(1)

                cf_now = float(self.get_cf())
                try:
                    print(cf_now)
                except:
                    print('Pinnacle: Не получил кф')

                if not cf_now:
                    continue
                if cf_now != 1.0:
                    new_total_prob = (1 / cf_now) + (1 / ggbet_cf)
                else:
                    new_total_prob = 2
                if new_total_prob <= 1:
                    print('Pinnacle: Считаю сумму ставки для второго плеча')
                    bet_sum = round(((ggbet_sum * ggbet_cf) / cf_now) / exchange_rate)
                    print('Pinnacle: Сумма ставки -', bet_sum)
                    self.do_bet_by_sum(bet_sum)
                    ##### ТЕТСОВАЯ ЗОНА #####
                    time.sleep(1)
                    try:
                        key_btn_do_bet = 'style_button__2cht5 style_fullWidth__tyxzD break-word style_medium__1Uf0e dead-center style_primary__3OVhQ style_button__1TVoo'
                        test_btn_do_bet = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_do_bet))
                        if test_btn_do_bet:
                            print('Pinnacle: Вижу кнопку поставить')
                    except:
                        pass
                    ##### ------------ #####
                    print('Pinnacle:  cтавка сделана')
                    betting_params = self.betting_report()
                    if betting_params:
                        print('Pinnacle: Посылаю результат')
                        self.signal_second_bet_is_done.emit(betting_params)
                    else:
                        #self.signal_error_in_betting.emit()
                        print('Pinnacle: Поставил, но купон не прогрузился')
                        return
                        ################3# отправить отчет в mainwindow  #####################
                    return
        print('Pinnacle: Пытаюсь поставить в минус', loose_max, '%')
        cf_now = self.get_cf()
        if cf_now == 1.0:
            print('Pinnacle: Ставка закрыта')
            #self.signal_error_in_betting.emit()
            print('Pinnacle: Не удалось перекрыть плечо')
            # не получилось поставить второе плечо
            # отправить отчет об этом
            # restart_bots
        else:
            income_now = ((cf_now * ggbet_cf) / (cf_now + ggbet_cf)) * 100
            if income_now >= (100 - loose_max):
                bet_sum = round(((ggbet_sum * ggbet_cf) / cf_now) / exchange_rate)
                self.do_bet_by_sum(bet_sum)
                ##### ТЕТСОВАЯ ЗОНА #####
                time.sleep(1)
                try:
                    key_btn_do_bet = 'style_button__2cht5 style_fullWidth__tyxzD break-word style_medium__1Uf0e dead-center style_primary__3OVhQ style_button__1TVoo'
                    test_btn_do_bet = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_do_bet))

                    if test_btn_do_bet:
                        print('Pinnacle: Вижу кнопку поставить')
                except:
                    pass
                ##### ------------ #####
                print('Pinnacle:  cтавка сделана')
                betting_params = self.betting_report()
                if betting_params:
                    print('Pinnacle: Посылаю результат')
                    self.signal_second_bet_is_done.emit(betting_params)
                else:
                    #self.signal_error_in_betting.emit()
                    print('Pinnacle: Поставил, но не прогрузился купон')
                    return

                ########## отправить отчет в mainwindow  #############
                return


    def betting(self,bet_sum_bet_cf):
        print('Pinnacle: ', bet_sum_bet_cf)
        bet_sum = bet_sum_bet_cf[0]
        bet_kf = bet_sum_bet_cf[1]
        exchange_rate = bet_sum_bet_cf[2]
        another_bet_sum = bet_sum_bet_cf[3]
        another_bet_kf = bet_sum_bet_cf[4]
        another_exchange_rate = bet_sum_bet_cf[5]
        seconds_do_bet = bet_sum_bet_cf[6]
        loose_max = bet_sum_bet_cf[7]

        print('Pinnacle: сек пытается поставить -', seconds_do_bet, type(seconds_do_bet))

        cf_now = self.get_cf()
        print('pinca Now:  ', cf_now)
        print('pinca', bet_sum)
        if cf_now >= bet_kf:
            self.do_bet_by_sum(bet_sum)
            print('Pinnacle:  cтавка сделана')
            self.betting_report()
            print('Pinnacle: ', cf_now, bet_sum, cf_now * bet_sum)
        else:
            print('Pinnacle: кф изменился в меньшую сторону')
            new_total_prob = (1 / cf_now) + (1 / another_bet_kf)
            win_sum = cf_now * bet_sum * exchange_rate
            totals_bets_sum = (bet_sum * exchange_rate) + (another_bet_sum * another_exchange_rate)
            if win_sum >= totals_bets_sum:
                self.do_bet_by_sum(bet_sum)
                print('Pinnacle:  cтавка сделана')
                self.betting_report()
                print('Pinnacle: ', cf_now, bet_sum, cf_now * bet_sum)
            elif new_total_prob <= 1:
                bet_sum = math.ceil(((another_bet_sum * another_bet_kf * another_exchange_rate) / cf_now) / exchange_rate)
                self.do_bet_by_sum(bet_sum)
                print('Pinnacle:  cтавка сделана')
                self.betting_report()
                print('Pinnacle: ', cf_now, bet_sum, cf_now * bet_sum)
                return
            else:
                print('Вилка пропала, пытаюсь переставить')
                for i in range(seconds_do_bet):
                    print('Pinnacle: пытаюсь переставить, попытка №', i)
                    time.sleep(1)
                    cf_now_i = self.get_cf()
                    total_prob_now = (1 / cf_now_i) + (1 / another_bet_kf)
                    if total_prob_now <= 1:
                        bet_sum = math.ceil(
                            ((another_bet_sum * another_bet_kf * another_exchange_rate) / cf_now_i) / exchange_rate)
                        self.do_bet_by_sum(bet_sum)
                        print('Pinnacle:  cтавка сделана')
                        self.betting_report()
                        print('Pinnacle: ', cf_now_i, bet_sum, cf_now_i * bet_sum)
                        # отправить отчет в mainwindow
                        return

                # пытаемся поставить в минус (заданный параметр)
                print('Пытаюсь поставить в минус', loose_max, '%')
                cf_now = self.get_cf()
                if cf_now == 1.0:
                    print('Pinnacle: Ставка закрыта, не полуилось закрыть плечо')
                    return
                income_now = ((cf_now * another_bet_kf) / (cf_now + another_bet_kf)) * 100

                if income_now >= (100-loose_max):
                    bet_sum = math.ceil(
                        ((another_bet_sum * another_bet_kf * another_exchange_rate) / cf_now_i) / exchange_rate)
                    self.do_bet_by_sum(bet_sum)
                    print('Pinnacle:  cтавка сделана')
                    self.betting_report()
                    print('Pinnacle: ', cf_now_i, bet_sum, cf_now_i * bet_sum)
                    # отправить отчет в mainwindow
                    return

                print('Pinnacle: Не получилось перекрыть, вилка исчезла')
                # не получилось поставить второе плечо
                # restart_bots
                #self.betting_report(False)


    def test_funct_do_bet_report(self):
        print('Проставляю')
        self.do_bet_by_sum(1)
        print('Pinnacle:  cтавка сделана')
        self.betting_report()

    def betting_report(self):

        print('Pinnacle: получаю отчет')
        try:
            print('Pinnacle:  Ставка поставлена')

            print('Pinnacle:  Жду прогрузки купона с инфо о поставленной ставке')
            key_bet_success = 'style_acceptedBet__1CnBu'
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="{}"]'.format(key_bet_success))))

            time.sleep(1)

            print('Pinnacle:  Считываю итог ставки')
            label_success = self.driver.find_element(By.XPATH, '//span[@class="{}"]'.format(key_bet_success)).text

            print('Pinnacle:  Получаю поставленный кф')
            #key_cf_label = 'SelectionDetails-Odds'
            key_cf_label = 'style_price__1pYJK betslipCardPrice'

            lablel_cf = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_cf_label)).text

            print('Pinnacle:  Получаю название команд')
            key_match_name ='style_matchupName__7ANi_ selectionDetailsMatchupName'
            match_name = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_match_name)).text

            print('Pinnacle:  Сумму ставки и выигрыш')
            key_win_bet_sum = 'style_subLabel__3pji-'
            win_bet_sum = self.driver.find_elements(By.XPATH, '//span[@class="{}"]'.format(key_win_bet_sum))
            bet_sum = win_bet_sum[0].text
            win_sum = win_bet_sum[1].text

            print('Pinnacle:  cf', lablel_cf)
            print('Pinnacle:  bet sum/win sum - ', bet_sum, ' | ', win_sum)

            return [match_name, lablel_cf, bet_sum]

            print('Pinnacle:  Закрываю купон')
            key_btn_close_bet_info = 'betslip-close-button style_close__NU41W style_close__3iLVm'
            btn_close_bet_info = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_btn_close_bet_info))
            btn_close_bet_info.click()

            time.sleep(2)

            #print('Pinnacle: Перехожу на главную страницу')
            #self.driver.get(self.bk_link)
        except:
            print('Pinnacle: что-то пошло не так в обработке инфо о ставке')
            return None

    def check_balance(self):
        key_label_balance = "style_bankroll__1aDDE"
        balance = self.driver.find_element(By.XPATH, '//span[@class="{}"]'.format(key_label_balance)).text
        try:
            balance = float(balance.split(' ')[0].replace(',', '.'))
        except:
            print('Something went wrong')
            return 0
        print('Pinnacle: balance =', balance)
        return balance

    def save_balance_limit(self, limit):
        self.balance_limit = limit





def get_webdriver(port):
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
    # Change chrome driver path accordingly
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def get_debug_port(profile_id):
    LOCAL_API = 'http://localhost:58888/api/profiles'
    data = requests.post(
        f'{LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
    ).json()
    return data['debug_port']




'''driver = pinnacleDriver()
driver.doWebDriver()
driver.log_in(['KH1553462', '34DFdfg3'])

dict = {
    'sport' : 'soccer',
    'BK1_name' : 'pinnacle',
    'BK1_href' : 'https://www.skynotes.bond/ru/soccer/spain-la-liga/girona-vs-real-sociedad/1559266140',
    'BK1_bet_type' : 'TOTALS',
    'BK1_bet' : 'TOTALS__OVER(2.5)',
    'BK1_cf': '1.358',
    'BK2_name' : 'gg_bet',
    'BK2_href' : 'https://gg209.bet/ru/esports/match/fnatic-vs-loud-01-10',
    'BK2_bet_type' : 'WIN',
    'BK2_bet' : 'WIN__P2',
    'BK2_cf': '4.94',
    'BK2_market_meta' : '{"title_name":"Победитель","bet_name":"LOUD"}',
    'pinnacle_sum_bet' : '100',
}

driver.do_bet(dict)'''