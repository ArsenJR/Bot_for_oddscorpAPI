from AllLibraries import *

GGBET_PORT = ''
GGBET_LINK = ''

class ggbetDriver(QObject):
    signal_with_cf_and_bet_limit = pyqtSignal(list)
    def doWebDriver(self):

        #self.profile_id = GGBET_PORT
        self.profile_id = 'ef7feae4c45943c9b9285ddc3a152be0'
        #self.bk_link = GGBET_LINK
        self.bk_link = 'https://ggbet.name/ru/'
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

        self.driver.maximize_window()
        self.driver.get(self.bk_link)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))

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
        self.driver.get(self.bet_link)

        self.driver.execute_script(f"window.scrollTo(0, 0)")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@data-label="Все"]')))

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
        bet_fields = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(fields_class_name))
            # ключ для доступа к названию типа ставки
        key_bet_type_name = 'marketTable__header___mSHxT'

        for bet_field in bet_fields:
            try:
                bet_type_name = bet_field.find_element(By.XPATH, './/div[@class="{}"]'.format(key_bet_type_name)).text
                if bet_type_name == self.bet_title:
                    self.fields_with_our_bet = bet_field
                    print('GGBET:   Поле найдено')
            except:
                print("GGBET:   Не удалось найти поле со ставкой")

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
            return
        # заключаем пари
        time.sleep(1)

        key_coupons_class = 'sidebarToggler__btn___2wIhe'

        # открываем купон
        try:
            button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
            button_open_cupon.click()
        except:
            pass


        key_btns_sum = 'amount__stake___2tO04 amount__is-desktop___3tNIb'
        time.sleep(1)
        self.buttons_with_sum = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_btns_sum))
        for btn in self.buttons_with_sum:
            if btn.text == 'MAX':
                print('GGBET:   Нашли кнопку макс ставки ')
                btn.click()
                key_max_bet_value = 'totalRow__value___1Ygme'
                self.bet_limit = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_max_bet_value))[0].text

        print('GGBET:   ', self.cf, self.bet_limit.split("\n")[0])
        self.signal_with_cf_and_bet_limit.emit([self.cf, self.bet_limit.split("\n")[0]])


    def betting(self, bet_sum_bet_cf):
        print('GGBet: ', bet_sum_bet_cf)
        bet_sum = bet_sum_bet_cf[0]
        bet_kf = bet_sum_bet_cf[1]
        # ключ строки для ввода суммы ставки
        key_input_sum_class = 'input__input___tstQL'
        try:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class = "{}"]'.format(key_input_sum_class))
            input_sum_lable.clear()
            input_sum_lable.send_keys(bet_sum)

            # ключ кнопки "Сделать ставку"
            key_button_do_bet = '__app-PlaceBet-container placeBet__container___ejcC8'


            button_do_bet = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_button_do_bet))
            button_do_bet.click()
        except:
            pass


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