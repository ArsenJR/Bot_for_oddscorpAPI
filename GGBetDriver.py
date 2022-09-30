from AllLibraries import *

GGBET_PORT = ''
GGBET_LINK = ''

class ggbetDriver(QObject):

    def doWebDriver(self):

        self.profile_id = GGBET_PORT
        self.bk_link = GGBET_LINK
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
        self.driver.get(self.bk_link)

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
        self.driver.get('https://gg209.bet/ru/live#!/auth/signin')

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
        print('Получил')
        print(self.bet_parameter['ggbet_sum_bet'])
        self.bet_link = self.get_match_link(self.bk_link, self.bet_href)
        self.bet_title = self.bet_markers['title_name']
        self.bet_name = self.bet_markers['bet_name']

        # открыли ссылку с матчем
        self.driver.get(self.bet_link)
        time.sleep(2)

        # открываем все ставки
        self.driver.execute_script(f"window.scrollTo(0, 0)")
        self.driver.find_element(By.XPATH, '//div[@data-label="Все"]').click()

        # прогружаем всю страничку
        self.driver.execute_script(f"window.scrollTo(0, 3000)")
        time.sleep(1)
        self.driver.execute_script(f"window.scrollTo(0, 0)")

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
                    print('Поле найдено')
            except:
                print("Не удалось обработать поле")
        # находим ставку по bet_name и нажимаем на неё
        for n in range(0, 5000, 300):
            try:
                button_with_our_bet = self.fields_with_our_bet.find_element(By.XPATH,
                                                                       './/button[contains(@title, "{}")]'.format(
                                                                           self.bet_name))
                button_with_our_bet.click()
                print("Ставка сделана")
                break
            except:
                self.driver.execute_script(f"window.scrollTo(0, {n})")

        # заключаем пари
        time.sleep(1)

        key_coupons_class = 'sidebarToggler__btn___2wIhe'

        # открываем купон
        try:
            button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
            button_open_cupon.click()
        except:
            pass

        # ключ строки для ввода суммы ставки
        key_input_sum_class = 'input__input___tstQL'

        # вводим сумму
        try:
            bet_sum = int(self.bet_parameter['ggbet_sum_bet'])
            print(bet_sum)
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class = "{}"]'.format(key_input_sum_class))
            input_sum_lable.clear()
            input_sum_lable.send_keys(bet_sum)

            # ключ кнопки "Сделать ставку"
            key_button_do_bet = '__app-PlaceBet-container placeBet__container___ejcC8'


            button_do_bet = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_button_do_bet))
            button_do_bet.click()
        except:
            pass

        print(self.bet_link)
        print(self.bet_markers['title_name'], " | ", self.bet_markers['bet_name'])



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