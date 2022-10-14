import math
import time

from AllLibraries import *

GGBET_PORT = ''
GGBET_LINK = ''

class ggbetDriver(QObject):
    signal_with_cf_and_bet_limit = pyqtSignal(list)
    signal_error_in_getting_data = pyqtSignal()
    signal_first_bet_is_done = pyqtSignal(list)

    def doWebDriver(self):

        self.update_count = 0
        self.profile_id = GGBET_PORT
        # self.profile_id = 'ef7feae4c45943c9b9285ddc3a152be0'
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

        self.driver.maximize_window()
        self.driver.get(self.bk_link)

        # self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="GG.BET"]')))

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
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@data-label="Все"]')))
        except:
            print('GGBet:  Не нашел кнопки "Все"')
            self.signal_error_in_getting_data.emit()
            return

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
                self.signal_error_in_getting_data.emit()
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
            self.signal_error_in_getting_data.emit()
            return
        # заключаем пари

        key_coupons_class = 'sidebarToggler__btn___2wIhe'

        # открываем купон
        try:
            button_open_cupon = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_coupons_class))
            button_open_cupon.click()
        except:
            pass
        time.sleep(1)

        key_input_sum_class = 'input__input___tstQL'
        try:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class = "{}"]'.format(key_input_sum_class))
            input_sum_lable.clear()
            input_sum_lable.send_keys(10000000)

            key_max_bet_value = 'totalRow__value___1Ygme'
            print('Получаю лимит')
            self.bet_limit = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_max_bet_value))[0].text
        except:
            print('Не получил лимит')
            self.signal_error_in_getting_data.emit()
            return

        print('GGBET:   ', self.cf, self.bet_limit.split("\n")[0])
        self.signal_with_cf_and_bet_limit.emit([self.cf, self.bet_limit.split("\n")[0]])

    def get_cf(self):
        print('Ищем кнопку')
        button_with_our_bet = self.fields_with_our_bet.find_element(By.XPATH,
                                                                    './/button[contains(@title, "{}")]'.format(
                                                                        self.bet_name))

        if button_with_our_bet:
            cf_now = float(button_with_our_bet.text)
            print(cf_now)
            print('Нашел коэф')
            return cf_now
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
            #input_sum_lable.send_keys(50)

            # ключ кнопки "Сделать ставку"
            key_button_do_bet = '__app-PlaceBet-container placeBet__container___ejcC8'

            button_do_bet = self.driver.find_element(By.XPATH, '//div[@class = "{}"]'.format(key_button_do_bet))
            button_do_bet.click()
            return True
        except:
            return False




    def first_betting(self, bet_sum_bet_cf):
        print('GGBet: ', bet_sum_bet_cf)
        bet_sum = bet_sum_bet_cf[0]
        bet_kf = bet_sum_bet_cf[1]
        another_bet_kf = bet_sum_bet_cf[2]
        cf_now = self.get_cf()
        if not cf_now:
            print('GGBet:  Не получается получить кф')
            self.signal_error_in_getting_data.emit()
            return

        new_total_prob = (1 / cf_now) + (1 / another_bet_kf)

        if new_total_prob < 1:
            print('GGBet: Ставлю ставку)')
            print(bet_sum)
            is_bet_done = self.do_bet_by_sum(bet_sum)
            if is_bet_done:
                try:
                    betting_report_data = self.betting_report()
                    print(betting_report_data)
                    const_cf = float(betting_report_data[0])
                    const_bet_sum = float(betting_report_data[1].split(' ')[0].replace(',', '.'))

                    print(const_cf, const_bet_sum)

                    self.signal_first_bet_is_done.emit([const_cf, const_bet_sum])
                except:
                    print('Не удалось получить отчет')
        else:
            print('GGBet: Вилка пропала, ставка не сделана')
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

    def betting(self, bet_sum_bet_cf):
        print('GGBet: ', bet_sum_bet_cf)
        bet_sum = bet_sum_bet_cf[0]
        bet_kf = bet_sum_bet_cf[1]
        exchange_rate = bet_sum_bet_cf[2]
        another_bet_sum = bet_sum_bet_cf[3]
        another_bet_kf = bet_sum_bet_cf[4]
        another_exchange_rate = bet_sum_bet_cf[5]
        seconds_do_bet = bet_sum_bet_cf[6]
        loose_max = bet_sum_bet_cf[7]

        # проверяем не упал ли коэффициент
        print('Ищем кнопку')
        cf_now = self.get_cf()

        is_bet_done = False

        if cf_now:
            print('ggbet Now:  ', cf_now)
            print('ggbet', bet_sum)
            if bet_kf <= cf_now:
                is_bet_done = self.do_bet_by_sum(bet_sum)
                if is_bet_done:
                    print('GGBET: Ставка сделана')
                    print('GGBET: ', cf_now, bet_sum, cf_now * bet_sum)
                else:
                    print('GGBet:  Не получилось ввести')
            else:
                print('GGBet:   КФ изменился')
                print(cf_now)
                new_total_prob = (1 / cf_now) + (1 / another_bet_kf)
                win_sum = cf_now * bet_sum * exchange_rate
                totals_bets_sum = (bet_sum * exchange_rate) + (another_bet_sum * another_exchange_rate)
                if win_sum >= totals_bets_sum:
                    is_bet_done = self.do_bet_by_sum(bet_sum)
                    if is_bet_done:
                        print('GGBET: Ставка сделана')
                        print('GGBET: ', cf_now, bet_sum, cf_now * bet_sum)
                    else:
                        print('GGBet:  Не получилось ввести')
                elif new_total_prob <= 1:
                    bet_sum = math.ceil(((another_bet_sum * another_bet_kf * another_exchange_rate) / bet_kf) / exchange_rate)

                    is_bet_done = self.do_bet_by_sum(bet_sum)
                    if is_bet_done:
                        print('GGBET: Ставка сделана')
                        print('GGBET: ', cf_now, bet_sum, cf_now * bet_sum)
                    else:
                        print('GGBet:  Не получилось ввести')
        if not is_bet_done:
            for i in range(seconds_do_bet):
                print('GGBet: пытаюсь переставить, попытка №', i)
                time.sleep(1)
                cf_now_i = self.get_cf()
                total_prob_now = (1 / cf_now_i) + (1 / another_bet_kf)
                if total_prob_now <= 1:
                    bet_sum = math.ceil(
                        ((another_bet_sum * another_bet_kf * another_exchange_rate) / cf_now_i) / exchange_rate)
                    is_bet_done = self.do_bet_by_sum(bet_sum)
                    if is_bet_done:
                        print('Pinnacle:  cтавка сделана')
                        print('Pinnacle: ', cf_now_i, bet_sum, cf_now_i * bet_sum)
        if not is_bet_done:
            print('Пытаюсь поставить в минус', loose_max, '%')
            cf_now = self.get_cf()
            income_now = ((cf_now * another_bet_kf) / (cf_now + another_bet_kf)) * 100
            if income_now >= (100 - loose_max):
                bet_sum = math.ceil(
                    ((another_bet_sum * another_bet_kf * another_exchange_rate) / cf_now_i) / exchange_rate)
                is_bet_done = self.do_bet_by_sum(bet_sum)
                if is_bet_done:
                    print('Pinnacle:  cтавка сделана')
                    print('Pinnacle: ', cf_now_i, bet_sum, cf_now_i * bet_sum)

        if is_bet_done:
            self.betting_report()
        else:
            print('GGBet: Попробовалв се, не получилось сделать ставку(')


    def go_to_start_page(self):
        # пробую закрыть купон
        try:
            button_with_our_bet = self.fields_with_our_bet.find_element(By.XPATH,
                                                                        './/button[contains(@title, "{}")]'.format(
                                                                            self.bet_name))
            button_with_our_bet.click()
        except:
            pass
        time.sleep(2)
        self.driver.get(self.bk_link)

    def betting_report(self):
        print('GGBet: получаю отчет')

        try:
            print('GGBet: Жду открытия поля с инфо о сделанной ставке')
            key_field_bets_info = 'betListHeader__item___6VoUc betListHeader__is-active___1NzU8'
            key_bet_container = 'bet__container___2geIr'
            #self.wait.until(EC.visibility_of_element_located(By.XPATH, '//div[@class="{}"]'.format(key_bet_container)))
            #time.sleep(20)
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

            return [constant_cf, bet_sum]

            time.sleep(2)
            self.driver.get(self.bk_link)
        except:
            print('GGBet: Что-то пошло не так...')

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