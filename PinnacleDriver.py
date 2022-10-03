from AllLibraries import *

PINNACLE_PORT = ''
PINNACLE_LINK = ''


class pinnacleDriver(QObject):
    signal_with_cf_and_bet_limit = pyqtSignal(list)
    def doWebDriver(self):

        #### ИЗМЕНИТЬ ПРИ РАБОТЕ ПРОГРАММЫ ####
        #self.profile_id = PINNACLE_PORT
        self.profile_id = '83772dc46c3e4caba2a0902455dd422c'
        #self.bk_link = PINNACLE_LINK
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
        self.wait = WebDriverWait(self.driver, 500)
        self.driver.get(self.bk_link)

        key_element = 'style_selected__FPAJz undefined style_selected__FPAJz'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="{}"]'.format(key_element))))





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

        self.bet_parameter = dict
        """self.bet_parameter = {
            "fork_id": "caf709ede191ef38f3",
            "income": 1.14,
            "ow_income": 0,
            "sport": "esports.cs",
            "bet_type": "WIN",
            "event_id": "16366171",
            "is_middles": "0",
            "is_cyber": "0",
            "BK1_bet": "WIN__P1",
            "BK1_bet_type": "WIN",
            "BK1_alt_bet": "",
            "BK1_cf": 2.16,
            "BK1_event_id": "GGGTN060ED2572B4",
            "BK1_event_native_id": "5:7bd12e59-4ffb-4938-84d1-347c6d2cbea0",
            "BK1_game": "Билли Харрис vs Dali Blanch",
            "BK1_href": "https://ggbet.name/ru/esports/match/bad-news-eagles-vs-eternal-fire-04-10",
            "BK1_league": "АТР Челленджер. Аликанте",
            "BK1_name": "gg_bet",
            "BK1_score": "0:0",
            "BK1_event_meta": "{'start_at': 1664799900}",
            "BK1_market_meta": "{\"title_name\":\"Победитель\",\"bet_name\":\"Bad News Eagles\"}",
            "BK2_bet": "WIN__P2",
            "BK2_bet_type": "WIN",
            "BK2_cf": 1.769,
            "BK2_href": "https://www.skynotes.one/ru/esports/csgo-iem-road-to-rio-eu-rmr-a/bad-news-eagles-vs-eternal-fire/1559739529#all",
            "BK2_name": "pinnacle",
            "BK2_event_meta": "AAA",
            "BK2_market_meta": "AAA",
            "alive_sec": 57
        }"""
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

        self.driver.get(bet_link)

        # дожидаемся прогрузки страницы
        self.wait.until(EC.visibility_of_element_located((By.ID, "all")))

        try:
            self.bets_field = self.get_field_by_name(bet_type, bet_name, sport_type)
            print('Pinnacle:   Поле найдено')
        except:
            print('Pinnacle:   Не удалось найти поле со ставкой')
            return
        try:
            if bet_type == 'SET_WIN' or bet_type == 'WIN':
                self.do_win_bet(bet_name, self.bets_field, sport_type)
                print('Pinnacle:   Открыл купон')
            if bet_type == 'SETS_TOTALS' or bet_type == 'TOTALS':
                self.do_total_bet(bet_name, self.bets_field, sport_type)
                print('Pinnacle:   Открыл купон')

            if bet_type == 'HANDICAP' or bet_type == 'MAP__HANDICAP':
                self.do_handicap_bet(bet_name, self.bets_field)
                print('Pinnacle:   Открыл купон')


            self.get_cf_and_bet_sum()

            print(f'Pinnacle:   {self.cf}, {self.bet_limit}')
            self.bet_limit = self.bet_limit.replace('RUB', ' ').replace(' ', '')
            print(self.bet_limit)
            #print('Отправляю')
            self.signal_with_cf_and_bet_limit.emit([self.cf, self.bet_limit])
        except:
            print('Pinnacle:   Не получилось поставить!(((')





    def get_cf_and_bet_sum(self):

        key_max_bet_sum = 'Betslip-StakeWinInput-MaxWagerLimit'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-test-id="{}"]'.format(key_max_bet_sum))))
        self.bet_limit = self.driver.find_element(By.XPATH, '//a[@data-test-id="{}"]'.format(key_max_bet_sum)).text

        key_cf_value = 'style_price__2KUeC betslipCardPrice'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="{}"]'.format(key_cf_value))))
        self.cf = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_cf_value)).text



    def get_match_link(self, url_bk, url_match):
        return url_bk + "/".join(url_match.split('/')[4:])

    def get_field_by_name(self, bet_type, bet, sport_type):

        # ключ области каждого вида ставок
        field_class_name = 'style_primary__3IwKt style_marketGroup__1-qlF'
        # ключи названия типа ставки
        key_bet_type = 'style_titleText__35WhH'

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

    def pinnacle_get_field_name(self, bet_type, bet, sport_type):
        fields_name_dict ={
            'WIN':'Денежная линия – Матч',
            'SET_01__WIN':'Денежная линия – Карта 1',
            'SET_02__WIN':'Денежная линия – Карта 2',
            'SET_03__WIN':'Денежная линия – Карта 3',
            'SET_04__WIN':'Денежная линия – Карта 4',
            'SET_05__WIN':'Денежная линия – Карта 5',
            'SETS_TOTALS':'Тотал – Матч',
            'MAP_1__TOTALS':'Тотал – Карта 1',
            'MAP_2__TOTALS':'Тотал – Карта 2',
            'MAP_3__TOTALS':'Тотал – Карта 3',
            'MAP_4__TOTALS':'Тотал – Карта 4',
            'MAP_5__TOTALS':'Тотал – Карта 5',
            'TEAM_TOTALS':'Тотал команды – Матч',
            'MAP_1__TEAM_TOTALS':'Тотал команды – Карта 1',
            'MAP_2__TEAM_TOTALS':'Тотал команды – Карта 2',
            'MAP_3__TEAM_TOTALS':'Тотал команды – Карта 3',
            'MAP_4__TEAM_TOTALS':'Тотал команды – Карта 4',
            'MAP_5__TEAM_TOTALS':'Тотал команды – Карта 5',
            'HANDICAP':'Гандикап – Матч',
            'MAP_1__HANDICAP':'Гандикап – Карта 1',
            'MAP_2__HANDICAP':'Гандикап – Карта 2',
            'MAP_3__HANDICAP':'Гандикап – Карта 3',
            'MAP_4__HANDICAP':'Гандикап – Карта 4',
            'MAP_5__HANDICAP':'Гандикап – Карта 5'
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


        transform_bet_type = bet_type.replace('__', ' ').replace('_', ' ').split(' ')
        transform_bet = bet.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')', '').split(' ')
        if transform_bet_type[0] == 'SET':
            bet_key = transform_bet_type[0]+ '_' +transform_bet[1]+ '__' + ('_'.join(transform_bet_type[1:]))
        else:
            bet_key = bet_type

        return fields_name_dict[bet_key]

    def open_all_bets(self):
        # ключ кнопки "посмотреть все рынки"
        key_to_open_all_bets = 'style_button__2cht5 style_fullWidth__tyxzD ellipsis style_medium__1Uf0e dead-center style_tertiary__1XC1Z all-markets-btn style_button__2Wms9'

        # нажимаем кнопку посмотреть все рынки
        try:
            button_open_all_bets = self.driver.find_element(By.XPATH,
                                                            '//button[@class="{}"]'.format(key_to_open_all_bets))
            button_open_all_bets.click()
        except:
            pass

    def do_win_bet(self, BK_bet, fields_with_our_bet, sport):

        # имя класса элемента с названием команд
        class_name = 'style_participantName__gdIKf'  # lable

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
        button_with_our_bet = fields_with_our_bet.find_element(By.XPATH, './/button[@title="{}"]'.format(command_name))
        button_with_our_bet.click()

    def do_total_bet(self, BK_bet, fields_with_our_bet, sport):
        # ключ копки 'отображать больше'
        key_button_image_more = 'style_toggleMarkets__18eR0'
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

        button_with_our_bet = fields_with_our_bet.find_element(By.XPATH,
                                                               './/button[@title="{}"]'.format(BK_bet_name))

        button_with_our_bet.click()

    def transform_total_bet(self, bet):
        # делаем список слов
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')',
                                                                                                           '').split(
            ' ')
        if bet_to_transform[2] == 'UNDER':
            bet_name = 'Меньше {}'.format(bet_to_transform[3])
        if bet_to_transform[2] == 'OVER':
            bet_name = 'Больше {}'.format(bet_to_transform[3])
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
        key_div_two_fora_bet = 'style_buttonRow__1eO34'
        # ключ класса кнопок ставок форы
        key_button_fora_bet = 'market-btn style_button__34Zqv style_pill__1NXWo style_horizontal__10PLW'
        # ключ копки 'отображать больше'
        key_button_image_more = 'style_toggleMarkets__18eR0'
        try:
            button_image_more = fields_with_our_bet.find_element(By.XPATH,
                                                                 './/button[@class="{}"]'.format(key_button_image_more))
            button_image_more.click()
        except:
            pass
        # получаем значение свойства title кнопки с нужной ставкой
        if BK_bet[0] == 'H':
            BK_bet_name = self.transform_handicap_bet(BK_bet)
        elif BK_bet[0] == 'M':
            BK_bet_name = self.transform_map_handicap_bet(BK_bet)

        command = self.get_command_number_in_handicap(BK_bet)
        all_fora_div = fields_with_our_bet.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_div_two_fora_bet))
        # если P1
        if command == 0:
            for fora_div in all_fora_div:
                buttons_with_fora = fora_div.find_elements(By.XPATH,
                                                           './/button[@class="{}"]'.format(key_button_fora_bet))
                button_with_fora = buttons_with_fora[0]
                bet_text = button_with_fora.text.split('\n')[0]

                if bet_text == BK_bet_name:
                    button_with_our_bet = button_with_fora
                    button_with_our_bet.click()
        # если P2
        if command == 1:
            for fora_div in all_fora_div:
                buttons_with_fora = fora_div.find_elements(By.XPATH,
                                                           './/button[@class="{}"]'.format(key_button_fora_bet))
                button_with_fora = buttons_with_fora[1]
                bet_text = button_with_fora.text.split('\n')[0]

                if bet_text == BK_bet_name:
                    button_with_our_bet = button_with_fora
                    button_with_our_bet.click()

    def get_command_number_in_handicap(self, bet):
        bet_to_transform = bet
        bet_to_transform = bet_to_transform.replace('__', ' ').replace('_', ' ').replace('(', ' ').replace(')', '').split(' ')
        if bet[0] == 'M':
            if bet_to_transform[3] == 'P1':
                command_number = 0
            if bet_to_transform[3] == 'P2':
                command_number = 1
        elif bet[0] == 'H':
            if bet_to_transform[1] == 'P1':
                command_number = 0
            if bet_to_transform[1] == 'P2':
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

    def betting(self,bet_sum):

        # находим поле и вводим туда сумму ставки
        input_sum_lable = self.driver.find_element(By.XPATH, '//input[@placeholder = "Сумма ставки"]')
        input_sum_lable.clear()
        input_sum_lable.send_keys(bet_sum)


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