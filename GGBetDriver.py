import WidgetPageComboSettingsBK
from AllLibraries import *
from ForkCalculator import is_fork_fit

GGBET_PORT = ''
GGBET_LINK = ''

class ggbetDriver(QObject):
    # сигнал с полученными кф и лимитам
    signal_with_cf_and_bet_limit = pyqtSignal(list)
    # сигнал при проставленном первом плече
    signal_first_bet_is_done = pyqtSignal(list)
    # сигнал с ошибкой открытия купона
    signal_error_in_getting_data = pyqtSignal()


    #signal_first_bet_is_done = pyqtSignal(list)
    #signal_stop_scaner = pyqtSignal()

    def doWebDriver(self):

        self.update_count = 0
        #self.profile_id = GGBET_PORT
        self.profile_id = '92295e3dbbbb4028a6fdd32c5e4ff11f'
        self.profile_id = WidgetPageComboSettingsBK.GGBET_PORT
        print('ggbet port - ', self.profile_id)
        # self.bk_link = GGBET_LINK
        self.bk_link = 'https://ggbets.co/ru/'
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
        self.wait_error_webpage = WebDriverWait(self.driver, 4)

        self.driver.maximize_window()
        self.driver.get(self.bk_link)

        # self.wait_error_webpage.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))

        try:
            key_button_accept_cookie = 'cookie-agreement__button cookie-agreement__button--ok'
            button_accept_cookie = self.driver.find_element(By.XPATH,
                                                            '//button[@class="{}"]'.format(key_button_accept_cookie))
            button_accept_cookie.click()
        except:
            pass

    def log_in(self, login_password):

        login = login_password[0]
        password = login_password[1]

        # переходим по ссылке авторизации
        self.driver.get(self.bk_link + 'live#!/auth/signin')

        username_lable = self.driver.find_element(By.XPATH, '//input[@id="_username"]')
        password_lable = self.driver.find_element(By.XPATH, '//input[@id="_password"]')
        username_lable.clear()
        username_lable.send_keys(login)

        password_lable.clear()
        password_lable.send_keys(password)
        time.sleep(1)

        key_button_input = 'btn btn-success btn-lg'
        button_input = self.driver.find_element(By.XPATH, '//button[@class="{}"]'.format(key_button_input))
        button_input.click()

    def get_match_link(self, bk_link, bet_link):
        return bk_link + "/".join(bet_link.split('/')[4:])

    def do_bet(self, dict):
        self.update_count = 0
        self.bet_parameter = dict

        self.bet_parameter = {
            'fork_id': '52bf84d9c1ed1d62a3',
            'income': 1.51, 'ow_income': 0,
            'sport': 'esports.cs',
            'bet_type': 'WIN',
            'event_id': '16093728',
            'is_middles': '0',
            'is_cyber': '1',
            'BK1_bet': 'WIN__P2',
            'BK1_bet_type': 'WIN',
            'BK1_alt_bet': '',
            'BK1_cf': 1.31,
            'BK1_event_id': 'GGGEC83DB3B892AE',
            'BK1_event_native_id': '5:f0c05042-4b0f-4052-bce5-4c4a220ab4cc',
            'BK1_game': 'Team Finest vs MASONIC',
            'BK1_href': 'https://ggbets.co/ru/esports/match/ravens-vs-balrogs-e-sport-30-11',
            'BK1_league': 'Elisa Invitational Fall 2022',
            'BK1_name': 'gg_bet',
            'BK1_score': '1:0',
            'BK1_event_meta': '{"start_at":1663848000}',
            'BK1_market_meta': '{"title_name":"Победитель","bet_name":"Balrogs e-Sport"}',
            'BK2_bet': 'WIN__P2',
            'BK2_bet_type': 'WIN',
            'BK2_alt_bet': '',
            'BK2_cf': 4.51,
            'BK2_event_id': 'PINECA347B908FF3',
            'BK2_event_native_id': '1559705902',
            'BK2_game': 'Finest vs MASONIC',
            'BK2_href': 'https://www.pinnacle.com/ru/esports/csgo-intel-extreme-masters-rio-major/natus-vincere-vs-bad-news-eagles/1562790469',
            'BK2_league': 'CS:GO - Elisa Invitational',
            'BK2_name': 'pinnacle',
            'BK2_score': '',
            'BK2_event_meta': '{"league_id":208956,"start_at":1663847880}',
            'BK2_market_meta': '{"key":"s;0;m","market_name":"moneyline","dest":"away","matchup_id":1559708853,"league_id":208956,"parent_id":1559705902,"participant_id":null,"is_special":false}',
            'alive_sec': 0
        }
        self.bet_parameter = dict
        #print(self.bet_parameter)

        if self.bet_parameter['BK1_name'] == 'gg_bet':
            self.bet_href = self.bet_parameter['BK1_href']
            self.bet_type = self.bet_parameter['BK1_bet_type']
            self.bet_name = self.bet_parameter['BK1_bet']
            self.bet_markers = json.loads(self.bet_parameter['BK1_market_meta'])
        elif self.bet_parameter['BK2_name'] == 'gg_bet':
            self.bet_href = self.bet_parameter['BK2_href']
            self.bet_type = self.bet_parameter['BK2_bet_type']
            self.bet_name = self.bet_parameter['BK2_bet']
            self.bet_markers = json.loads(self.bet_parameter['BK2_market_meta'])
        print('GGBET:   Получил данные по вилке')

        self.bet_link = self.get_match_link(self.bk_link, self.bet_href)
        self.bet_title = self.bet_markers['title_name']
        self.bet_name = self.bet_markers['bet_name']

        # открыли ссылку с матчем
        self.driver.minimize_window()
        self.driver.maximize_window()
        self.driver.get(self.bet_link)

        self.driver.execute_script(f"window.scrollTo(0, 0)")

        # проверка: на страницу с ошибкой/ техническими работами
        try:
            self.wait_error_webpage.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))
        except:
            try:
                self.wait_error_webpage.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))
            except:
                self.driver.get(self.bet_link)

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@data-label="Все"]')))
        except:
            print('GGBet:  Не нашел кнопки "Все"')
            #self.signal_error_in_getting_data.emit()
            return

        # убираем открытый купон, если он остался после прошлой ставки
        print('GGBet - удаляем старый купон')
        self.try_close_cupons()

        # открываем все ставки
        self.driver.execute_script(f"window.scrollTo(0, 0)")
        self.driver.find_element(By.XPATH, '//div[@data-label="Все"]').click()

        # прогружаем всю страничку
        self.driver.execute_script(f"window.scrollTo(0, 3000)")
        time.sleep(1)
        self.driver.execute_script(f"window.scrollTo(0, 0)")
        time.sleep(1)

        # находим поле по title_name
        # ключ для поиска областей с каждым типом ставки
        fields_class_name = '__app-TableHeader-table tableHeader__container___2othd'
        # находим области каждого вида ставок
        print('Ищу поле')
        bet_fields = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(fields_class_name))
        print('Нашел поле')

        # ключ для доступа к названию типа ставки
        key_bet_type_name = 'marketTable__header___mSHxT'
        for bet_field in bet_fields:
            try:
                bet_type_name = bet_field.find_element(By.XPATH, './/div[@class="{}"]'.format(key_bet_type_name)).text
                if bet_type_name == self.bet_title:
                    self.fields_with_our_bet = bet_field
                    print('GGBET:   Поле найдено')
                    break
            except:
                print("GGBET:   Не удалось найти поле со ставкой")
                #self.signal_error_in_getting_data.emit()
                return

        # находим ставку по bet_name и нажимаем на неё
        print(self.bet_name)
        is_cupon_open = True
        for n in range(0, 5000, 300):
            try:
                button_with_our_bet = self.fields_with_our_bet.find_element(By.XPATH,
                                                                       './/button[contains(@title, "{}")]'.format(
                                                                           self.bet_name))
                self.cf = button_with_our_bet.text
                button_with_our_bet.click()
                print("GGBET:   Ставка сделана")
                is_cupon_open = False
                break
            except:
                self.driver.execute_script(f"window.scrollTo(0, {n})")

        if is_cupon_open:
            print("GGBet:     Ставка закрыта")
            #self.signal_error_in_getting_data.emit()
            return
        # заключаем пари

        key_coupons_class = '__app-MatchDetails-team matchDetails__team___1DUD-'
        # открываем купон
        key_coupons_class = 'sidebarToggler__btn___2wIhe'
        # открываем купон
        try:
            button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
            button_open_cupon.click()
        except:
            pass

        time.sleep(1)
        self.driver.minimize_window()
        self.driver.maximize_window()
        self.bet_limit = self.get_limit()
        if  not self.bet_limit:
            print('Не получил лимит')
            key_coupons_class = 'sidebarToggler__btn___2wIhe'
            # открываем купон
            try:
                button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
                button_open_cupon.click()
            except:
                pass
            self.bet_limit = self.get_limit()
            if not self.bet_limit:
                # self.signal_error_in_getting_data.emit()
                return

        print('GGBET:   ', float(self.cf), self.bet_limit)
        self.signal_with_cf_and_bet_limit.emit(['gg_bet', float(self.cf), self.bet_limit])

    def get_limit(self):
        print('Ищу лимит')
        key_input_sum_class = 'input__input___tstQL'
        try:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class = "{}"]'.format(key_input_sum_class))
            input_sum_lable.clear()
            input_sum_lable.send_keys(10000000)

            time.sleep(1)
            # key_max_bet_value = 'totalRow__value___1Ygme'
            key_max_bet_value = 'totalRow__value___ZoXb4'
            print('Получаю лимит')
            bet_limit = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_max_bet_value))[0].text
            bet_limit = bet_limit.split('\n')[0]
            return float(bet_limit)
        except:
            print('Не получил лимит')
            return False

    def get_cf(self):
        print('Ищем кнопку')
        print(self.bet_name)
        button_with_our_bet = self.fields_with_our_bet.find_element(By.XPATH,
                                                                    './/button[contains(@title, "{}")]'.format(
                                                                        self.bet_name))

        if button_with_our_bet:
            print('Нашел коэф')
            cf_now = float(button_with_our_bet.text)
            if cf_now:
                print(cf_now)
                return cf_now
            else:
                print('GGBet:  Нашел кнопку, но ставка закрыта')
                return None
        else:
            print('GGBet:    Не могу найти коэф')
            return None

    def do_bet_by_sum(self, bet_value):
        # ключ строки для ввода суммы ставки
        key_input_sum_class = 'input__input___tstQL'
        try:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class = "{}"]'.format(key_input_sum_class))
            input_sum_lable.clear()
            input_sum_lable.send_keys(bet_value)
            print('Постаивл', bet_value)
            #input_sum_lable.send_keys(50)

            time.sleep(1)
            # ключ кнопки "Сделать ставку"
            key_button_do_bet = '__app-PlaceBet-container placeBet__container___niUkt'

            button_do_bet = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_button_do_bet))
            button_do_bet.click()

            return True
        except:
            return False




    def first_betting(self, data):
        print('GGBet: ', data)
        bet_sum = data[0]
        exchange_rate = data[1]
        another_limit = data[2]
        another_cf = data[3]
        another_exchange_rate = data[4]
        min_profit = data[5]
        max_profit = data[6]
        min_cf = data[7]
        max_cf = data[8]

        self.driver.minimize_window()
        self.driver.maximize_window()

        # Проверяем все ли видно на странице
        try:
            self.wait_error_webpage.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))
        except:
            try:
                self.wait_error_webpage.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))
            except:
                self.driver.get(self.bet_link)

        limit_now = self.get_limit()
        cf_now = self.get_cf()
        if not cf_now:
            print('GGBet:  Не получается получить кф')
            #self.signal_error_in_getting_data.emit()
            return

        self.is_fork_fit = is_fork_fit(bet_sum, limit_now, cf_now, exchange_rate,
                                       another_limit, another_cf, another_exchange_rate,
                                       min_profit, max_profit, min_cf, max_cf)

        if not self.is_fork_fit:
            print('GGBet - вилка не подходит')
            return

        is_bet_done = self.do_bet_by_sum(bet_sum)
        print('Поставил,дальше получаю отчет')
        if is_bet_done:
            betting_report_data = self.betting_report()
            print(betting_report_data)
            const_cf = float(betting_report_data[0])
            const_bet_sum = float(betting_report_data[1].split(' ')[0].replace(',', '.'))

            print(const_cf, const_bet_sum)
            self.signal_first_bet_is_done.emit([const_bet_sum, const_cf, betting_report_data[2]])
        else:
            print('Не получилось поставить')

        ################################################

    def second_betting(self, first_bet_data):
        pinnacle_cf = float(first_bet_data[0])
        pinnacle_sum = float(first_bet_data[1])
        pinnacle_exchange_rate = first_bet_data[2]
        exchange_rate = first_bet_data[3]
        seconds_do_bet = first_bet_data[4]
        loose_max = first_bet_data[5]


        print('GGbet: Получаю коэффициент')
        cf_now = self.get_cf()
        is_bet_done = False

        if cf_now:
            new_total_prob = (1 / cf_now) + (1 / pinnacle_cf)
        else:
            new_total_prob = 2

        if new_total_prob <= 1:
            print('GGbet: Считаю сумму ставки для второго плеча')
            bet_sum = math.ceil((pinnacle_sum * pinnacle_cf * pinnacle_exchange_rate) / cf_now)
            print('GGbet: Сумма ставки -', bet_sum)
            is_bet_done = self.do_bet_by_sum(bet_sum)
        if not is_bet_done:
            print('GGBet: Пытаюсь поставить (попытка №2)')
            for i in range(seconds_do_bet):
                time.sleep(1)
                cf_now = self.get_cf()
                if cf_now:
                    new_total_prob = (1 / cf_now) + (1 / pinnacle_cf)
                else:
                    new_total_prob = 2
                if new_total_prob <= 1:
                    print('GGbet: Считаю сумму ставки для второго плеча')
                    bet_sum = math.ceil((pinnacle_sum * pinnacle_cf * pinnacle_exchange_rate) / cf_now)
                    print('GGbet: Сумма ставки -', bet_sum)
                    is_bet_done = self.do_bet_by_sum(bet_sum)
                    break
        if not is_bet_done:
            print('GGBet: Пытаюсь поставить в минус', loose_max, '%')
            cf_now = self.get_cf()
            income_now = ((cf_now * pinnacle_cf) / (cf_now + pinnacle_cf)) * 100
            if income_now >= (100 - loose_max):
                bet_sum = math.ceil(
                    ((pinnacle_sum * pinnacle_cf * pinnacle_exchange_rate) / cf_now) / exchange_rate)
                is_bet_done = self.do_bet_by_sum(bet_sum)

        if is_bet_done:
            self.betting_report()
        else:
            print('GGBet: Попробовал все, не получилось сделать ставку(')

    def try_close_cupons(self):
        key_label_cpon_count = '__app-BetCount-container' # div
        count_open_cupons = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_label_cpon_count))
        if count_open_cupons.text == '0':
            print('Текст на плагке с купоном: ', count_open_cupons.text)
            return

        key_coupons_class = 'sidebarToggler__btn___2wIhe'
        # открываем купон
        try:
            button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
            button_open_cupon.click()
        except:
            pass

        try:
            btn_delete_all = self.driver.find_element(By.XPATH, '//div[@title="Удалить все ставки"]')
        except:
            btn_delete_all = None

        if btn_delete_all:
            btn_delete_all.click()

    def go_to_start_page(self):
        try:
            self.driver.minimize_window()
            self.driver.maximize_window()
        except:
            self.driver.minimize_window()
            self.driver.maximize_window()

        self.try_close_cupons()
        # get_balance
        self.driver.get(self.bk_link)

    def betting_report(self):
        print('GGBet: получаю отчет')

        try:
            print('GGBet: Жду открытия поля с инфо о сделанной ставке')
            key_field_bets_info = 'betListHeader__item___6VoUc betListHeader__is-active___1NzU8'
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="bet__container___2geIr"]')))
            except:
                print('Не нашел это поле')

            time.sleep(1)

            # находим поле со ставкой
            print("GGBet:  Ищем поля с инфой о сделанных ставок")
            key_bet_container = 'bet__container___2geIr'

            containers = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_bet_container))

            print("GGBet:  Ищем наше поле")
            our_container = containers[0]

            print('GGBet: Получаю название команд')
            key_match_name = '__app-SmartLink-link'
            match_name = our_container.find_element(By.XPATH, './/a[@class="{}"]'.format(key_match_name)).text

            print('GGBet: Получаю ставку')
            key_bet_name = 'odd__odd___2d18G'
            bet = our_container.find_element(By.XPATH, './/div[@class="{}"]'.format(key_bet_name)).text

            print('GGBet: Получаю тип ставки')
            key_bet_type = 'odd__market___1nQc1'
            bet_type = our_container.find_element(By.XPATH, './/div[@class="{}"]'.format(key_bet_type)).text


            print('GGBet: Получаю сумму ставки и выигрыша')
            key_win_bet_sum = 'betFooter__value___1w0hb'
            elements_with_sum = our_container.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_win_bet_sum))
            bet_sum = elements_with_sum[0].text
            win_sum = elements_with_sum[1].text

            print('GGBet: Получаю кф')
            key_kf_value = 'odd__coef___13USE'
            constant_cf = our_container.find_element(By.XPATH, './/div[@class="{}"]'.format(key_kf_value)).text
            print('GGBet: КФ =', constant_cf)


            print('GGBet:  ', match_name, ' | ', bet_type, ' | ', bet)
            print('GGBet:  ', bet_sum, ' | ', win_sum)

            return [constant_cf, bet_sum, [match_name, constant_cf, bet_sum, bet_type, bet]]
        except:
            print('GGBet: Что-то пошло не так...')

    def check_balance(self):
        key_label_balance = "display-balance__text"
        balance = self.driver.find_element(By.XPATH, '//span[@class="{}"]'.format(key_label_balance)).text
        try:
            balance = float(balance.split(' ')[0].replace(',', ''))
        except:
            print('Something went werong')
            return 0
        print('GGBet: balance =', balance)
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



#driver = ggbetDriver()
#driver.doWebDriver()
#driver.log_in(['+79771000530', 'Arsen2000!'])

"""dict = {
    'BK1_name' : 'pinnacle',
    'BK1_href' : 'https://www.skynotes.one/ru/esports/csgo-iem-road-to-rio-eu-rmr-b/vitality-vs-fantasy/1560166295',
    'BK1_bet_type' : 'WIN',
    'BK1_bet' : 'WIN__P2',
    'BK1_cf': '9.14',
    'BK2_name' : 'gg_bet',
    'BK2_href' : 'https://ggbet.name/ru/esports/match/vitality-vs-fantasy-04-10',
    'BK2_bet_type' : 'WIN',
    'BK2_bet' : 'WIN__P1',
    'BK2_cf': '1.1',
    'BK2_market_meta' : '{"title_name":"Победитель","bet_name":"VITALITY"}',
    'pinnacle_sum_bet' : '100',
    'ggbet_sum_bet' : '100',
}"""

#driver.do_bet(dict)