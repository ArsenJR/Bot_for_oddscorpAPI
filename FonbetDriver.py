from AllLibraries import *
from ForkCalculator import is_fork_fit
import WidgetPageComboSettingsBK




class fonbetDriver(QObject):
    # сигнал с полученными кф и лимитам
    signal_with_cf_and_bet_limit = pyqtSignal(list)
    # сигнал при проставленном первом плече
    signal_first_bet_is_done = pyqtSignal(list)
    # сигнал с ошибкой открытия купона
    signal_error_in_getting_data = pyqtSignal()
    # сигнал с инфо о ставке (при проставлении второго плеча)
    signal_second_bet_is_done = pyqtSignal(list)

    def doWebDriver(self):

        self.update_list = 0

        self.profile_id = 'fd9dad5d82c44a0b9855e35f89c5cb63'
        self.profile_id = 'b983527da61e4a2c86f9c11d5fac5dd8'
        self.profile_id = WidgetPageComboSettingsBK.FONBET_PORT
        #print('Fonbet: Заданная ссылка -', WidgetPageComboSettingsBK.FONBET_LINK)

        # self.bk_link = PINNACLE_LINK
        self.bk_link = 'https://www.fon.bet/'
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

        self.wait = WebDriverWait(self.driver, 30)
        self.wait_error_webpage = WebDriverWait(self.driver, 4)

        self.driver.get(self.bk_link)

    def do_bet(self, dict):

        print('Fonbet: Данные получены!')
        self.update_count = 0
        self.bet_parameter = dict
        self.bet_parameter = {
            "fork_id": "24c69551b6a2dc8d3c",
            "income": 0.66,
            "ow_income": 0,
            "sport": "esports.cs",
            "bet_type": "SET_HANDICAP",
            "event_id": "2711419",
            "is_middles": "0",
            "is_cyber": "1",
            "BK1_bet": "SET_01__TOTALS__UNDER(23.5)",
            "BK1_bet_type": "SET_TOTALS",
            "BK1_alt_bet": "",
            "BK1_cf": 3.45,
            "BK1_event_id": "FONECC062548F092",
            "BK1_event_native_id": "37171745",
            "BK1_game": "corinthians academy vs Yawara Esports",
            "BK1_href": "https://www.fon.bet/sports/esports/84068/37347274/",
            "BK1_league": "Counter-Strike. Logitech G Challenge. Бразилия. Из 3-х карт",
            "BK1_name": "fonbet",
            "BK1_score": "",
            "BK1_event_meta": "{\"start_at\":1667588400,\"raw_start_at\":\"04.11 22:00\",\"eng_team1\":\"corinthians academy\",\"eng_team2\":\"Yawara Esports\",\"tv\":0}",
            "BK1_market_meta": "{\"group_name\":\"МАТЧ\",\"market_name\":\"Форы\",\"outcome_name\":\"2\",\"subevent_id\":37171746,\"market_type\":0,\"market_num\":503,\"factor_id\":1572,\"p\":\"+3.5\"}",
            "BK2_bet": "SET_01__HANDICAP__P1(-3.5)",
            "BK2_bet_type": "SET_HANDICAP",
            "BK2_alt_bet": "",
            "BK2_cf": 1.79,
            "BK2_event_id": "BCYECEFB8C55190F",
            "BK2_event_native_id": "12053614",
            "BK2_game": "Corinthians Academy vs Yawara Esports",
            "BK2_href": "https://betcity.by/ru/line/cybersport/119595/12053614",
            "BK2_league": "Киберспорт. CSGO. Logitech G Challenge (матчи из 3-х карт).",
            "BK2_name": "betcity_by",
            "BK2_score": "",
            "BK2_event_meta": "{\"start_at\":1667588100,\"str_start_at\":\"2022-11-04 21:55\"}",
            "BK2_market_meta": "{\"selector\":\"540249442_F1_Kf_F1\",\"marketName\":\"Исходы по картам\",\"blockName\":\"F1\",\"selection_name\":\"Kf_F1\",\"row_name\":\"1-я карта\"}"
        }

        self.bet_parameter = dict

        if self.bet_parameter['BK1_name'] == 'fonbet':
            bet_href = self.bet_parameter['BK1_href']
            bet_type = self.bet_parameter['BK1_bet_type']
            bet_name = self.bet_parameter['BK1_bet']
        elif self.bet_parameter['BK2_name'] == 'fonbet':
            bet_href = self.bet_parameter['BK2_href']
            bet_type = self.bet_parameter['BK2_bet_type']
            bet_name = self.bet_parameter['BK2_bet']

        bet_link = self.get_match_link(self.bk_link, bet_href)
        print('ССылка на матч: ', bet_link)

        sport_type = self.bet_parameter['sport']

        print('Fonbet:   Получил вилку')
        bet_link = bet_href

        time.sleep(1)       # Возможно убрать (ЗАЧЕМ ОНА? <3)
        self.driver.minimize_window()
        try:
            self.driver.maximize_window()
        except:
            time.sleep(1)
            self.driver.maximize_window()
        self.driver.get(bet_link)

        # активная вкладка раздела ставок
        key_active_game_part = 'tab--4RNtV _state_selected--408s1'
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="{}"]'.format(key_active_game_part))))
        except:
            print('Не прогрузилась страница')
            self.signal_error_in_getting_data.emit()
            return  # сброс бота в последствии

        print('Страница загружена!')

        # ОТКРЫВАЕМ РАЗДЕЛ СО СТАВКАМИ
        is_part_open =self.open_bet_part(bet_name)
        if not is_part_open:
            print('Конец, не загрузились ставки на необходимый период')
            self.signal_error_in_getting_data.emit()
            return  # сброс бота в последствии

        # ДАЛЬШЕ ИЩЕМ ОБЛАСТЬ С НАШЕЙ СТАВКОЙ
        field_with_our_bet = self.get_bet_field(bet_name)
        if field_with_our_bet:
            print('Поле со ставкой найдено')
        else:
            print('Нет поля со ставкой')
            self.signal_error_in_getting_data.emit()
            return

        print('Пытаюсь закрыть купон')
        self.try_close_cupons()


        if bet_type == 'SET_WIN' or bet_type == 'WIN':
            self.do_win_bet(bet_name, field_with_our_bet)
            print('Fonbet:   Открыл купон')

        if bet_type == 'SETS_TOTALS' or bet_type == 'TOTALS' or bet_type == 'SET_TOTALS':
            self.do_total_bet(bet_name, field_with_our_bet)
            print('Fonbet:   Открыл купон')

        if bet_type == 'HANDICAP' or bet_type == 'SET_HANDICAP' or bet_type == 'SETS_HANDICAP':
            self.do_handicap_bet(bet_name, field_with_our_bet)
            print('Fonbet:   Открыл купон')

        try:
            cf_now, limit_now = self.get_cf_and_bet_limit()
            print(cf_now, limit_now)
            self.signal_with_cf_and_bet_limit.emit(['fonbet', cf_now, limit_now])
        except:
            self.signal_error_in_getting_data.emit()
            print('Fonbet: Не получил кф и лимит')


    def betting_first(self, data):

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
        try:
            self.driver.maximize_window()
        except:
            time.sleep(1)
            self.driver.maximize_window()

        cf_now, limit_now = self.get_cf_and_bet_limit()

        self.is_fork_fit = is_fork_fit(bet_sum, limit_now, cf_now, exchange_rate,
                        another_limit, another_cf, another_exchange_rate,
                        min_profit, max_profit, min_cf, max_cf)

        if not self.is_fork_fit:
            print('Fonbet - вилка не подходит')
            return

        self.do_bet_by_sum(bet_sum)
        # пробуем кф
        cf, bet_sum = self.get_betting_report()
        if cf and bet_sum:
            self.signal_first_bet_is_done.emit([bet_sum, cf])
        else:
            print('Не получил отчет по Fonbet')


    def second_betting(self, first_bet_data):
        print('Fonbet - данные для закрытия второго плеча: ', first_bet_data)
        first_cf = float(first_bet_data[0])
        first_bet_sum = float(first_bet_data[1])
        first_exchange_rate = first_bet_data[2]
        exchange_rate = first_bet_data[3]
        seconds_do_bet = first_bet_data[4]
        loose_max = first_bet_data[5]

        try:
            self.driver.minimize_window()
            self.driver.maximize_window()
        except:
            time.sleep(1)
            self.driver.minimize_window()
            self.driver.maximize_window()

        cf_now, limit_now = self.get_cf_and_bet_limit()

        if cf_now:
            new_total_prob = (1 / cf_now) + (1 / first_cf)
        else:
            new_total_prob = 2

        if new_total_prob <= 1:
            print('Fonbet: Считаю сумму ставки для второго плеча')
            bet_sum = round(((first_bet_sum * first_cf * first_exchange_rate) / cf_now) / exchange_rate)
            print('Fonbet: Сумма ставки -', bet_sum)
            # ставим
            self.do_bet_by_sum(bet_sum)
            # пробуем кф
            cf, bet_sum = self.get_betting_report()
            if cf and bet_sum:
                self.signal_second_bet_is_done.emit([bet_sum, cf])
                print('Сделал ставку, добавить сигнал с результатом. ДОРАБОТАТЬ (вроде сделал). ')
                return
            else:
                print('Не получил отчет по Fonbet')

        # Поставить не удалось, пробую снова (макс. время перекрытия плеча)
        for i in range(seconds_do_bet):
            time.sleep(1)
            cf_now = self.get_cf()

            if cf_now:
                new_total_prob = (1 / cf_now) + (1 / first_cf)
            else:
                new_total_prob = 2

            if new_total_prob <= 1:
                break

        print('Финальная попытка проставления. Макс. разрешенные потери - ', loose_max)

        cf_now, limit_now = self.get_cf_and_bet_limit()

        income_now = ((cf_now * first_cf) / (cf_now + first_cf)) * 100
        print('Прибыль сейчас = ', income_now)
        if income_now >= (100 - loose_max):
            print('Fonbet: Считаю сумму ставки для второго плеча')
            bet_sum = round(((first_bet_sum * first_cf * first_exchange_rate) / cf_now) / exchange_rate)
            print('Fonbet: Сумма ставки -', bet_sum)
            # ставим
            self.do_bet_by_sum(bet_sum)
            # пробуем кф
            cf, bet_sum = self.get_betting_report()
            if cf and bet_sum:
                print('Fonbet - удалось закрыть плечо')
                self.signal_second_bet_is_done.emit([bet_sum, cf])
                return
            else:
                print('Не получил отчет по Fonbet')
                return
        print('Плечо не удалось закрыть')
        return

    def get_betting_report(self):
        try:
            print('Жду принятия ставки')
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="caption--4yIjj"]')))
        except:
            print('Не полчается получить отчет')
            return None, None

        key_betting_data = 'coupon__info-text--1McvP'
        betting_data = self.driver.find_elements(By.XPATH, '//i[@class="{}"]'.format(key_betting_data))

        try:
            cf = float(betting_data[1].text)
            bet_sum_label = betting_data[2].text
            bet_sum = float(bet_sum_label.split(' ')[0])
            print('КФ:', cf)
            print('Сумма ставки:', bet_sum)
            return cf, bet_sum
        except:
            print('Не получилось кф и сумму')
            return None, None

    def do_bet_by_sum(self, sum):
        key_label_bet_v1 = 'sum-panel__input--5a9Sq _state_error--5LXOR'
        key_label_bet_v2 = 'sum-panel__input--5a9Sq'

        try:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class="{}"]'.format(key_label_bet_v1))
        except:
            input_sum_lable = self.driver.find_element(By.XPATH, '//input[@class="{}"]'.format(key_label_bet_v2))

        input_sum_lable.clear()
        input_sum_lable.send_keys(str(sum))

        time.sleep(2)
        key_btn_betting = 'button--9z8aU normal-bet--6H68z _use_color_settings--2h94A _spec1--1haRL _spec2--2pfTB'
        try:
            btn_do_bet = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_btn_betting))
            print('Fonbet -  нашел кнопку поставить')
            btn_do_bet.click()
            time.sleep(3)
            print('Отправляю сигнал, получилось поставить.')
        except:
            print('Fonbet - не получилось поставить ')

    def try_close_cupons(self):
        # ищем кнопку закрыть купон перед ставкой
        print('Test zone 0')
        try:
            print('start')
            self.driver.find_element(By.XPATH, '//div[@class="stakes-head__clear--1ESbd _use_color_settings--2h94A"]').click()
            print('end')
        except:
            print('Fonbet - купон был пуст')
            return
        print('Fonbet - удалил старый купон')
        return

        """try:
            print('Fonbet - Ищу купон')
            btn_close_cupon = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_btn_close_cupon))
            print('Fonbet - Нашел купон')
            time.sleep(1)
            print(btn_close_cupon)
            btn_close_cupon.click()
            print('Закрыли купон')
        except:
            btn_close_cupon = None
            print('Купон был пуст')"""




    def get_cf_and_bet_limit(self):
        # получаем кф и лимит
        key_btn_close_cupon = 'stakes-head__clear--1ESbd _use_color_settings--2h94A'
        try:
            btn_close_cupon = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="{}"]'.format(key_btn_close_cupon))))
        except:
            btn_close_cupon = None
            print('Купон не открылся')
        if btn_close_cupon:
            cf_now = self.get_cf()
            limit_now = self.get_bet_limit()

            print('Лимит =', limit_now)
            print('Коэффициент =', cf_now)
            return cf_now, limit_now
        else:
            return None, None

    def get_cf(self):

        # изменился ли коэф
        key_span_new_cf = 'v-current--6su1Q _active--6faLR'

        try:
            new_cf_btn = self.driver.find_element(By.XPATH, '//span[@class="{}"]'.format(key_span_new_cf))
        except:
            new_cf_btn = None

        if new_cf_btn:
            new_cf_btn.click()

        key_cf_span = 'v-current--6su1Q'
        try:
            cf_span = self.driver.find_element(By.XPATH, '//span[@class="{}"]'.format(key_cf_span))
        except:
            cf_span = 1
            print('Fonbet - что-то не так с получением кф')
        return float(cf_span.text)

    def get_bet_limit(self):

        key_btn_max_bet = 'info-block__value--7qWjd _active--6faLR'
        el = self.driver.find_elements(By.XPATH, '//span[@class="{}"]'.format(key_btn_max_bet))
        text = el[1].text
        print(text)

        return float(text.replace('\u2009', '').replace('₽', ''))

    def get_match_link(self, url_bk, url_match):
        return url_bk + "/".join(url_match.split('/')[3:])

    def do_win_bet(self, bet_name, bet_field):

        # ключ кнопки
        key_btn_bet = 'cell-wrap--LHnTw'

        btn_indx = int(float(bet_name.replace('_', ' ').replace('  ', ' ')[-1]) - 1)
        win_btns = bet_field.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_btn_bet))

        win_btns[btn_indx].click()

    def do_total_bet(self, bet_name, bets_field):

        # связка кнопка - название ставики
        key_bet_row = 'row-common--33mLE'
        # название ставки-тотал
        key_name_total_bet = 'cell-wrap--LHnTw'
        # ключ к кнопке тотал
        key_btn_total_bet = 'cell-wrap--LHnTw _width-fixed--dhzsT'

        total_value = bet_name.replace('_', ' ').replace('  ', ' ').split(' ')[-1]
        total_value = total_value.replace('(', ' ').replace(')', '').split()

        total_name = 'Тотал ' + total_value[1]
        total_type = total_value[0]
        print(total_name, total_type)

        is_first = False
        true_row = None

        rows = bets_field.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_bet_row))
        for row in rows:
            names = row.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_name_total_bet))
            j = 0
            for name in names:
                j += 1
                print(name.text)
                if name.text == total_name:  # СРАВНЕНИЕ С ДАННЫМИ ИЗ ВИЛКИ
                    print('Найдена строка с нужным тоталом')
                    true_row = row
                    if j == 1:
                        is_first = True
                        break

        if not true_row:
            print('Нет заданного тотала')
            return

        btns_with_total = true_row.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_btn_total_bet))
        if is_first:
            if total_type == 'OVER':
                btns_with_total[0].click()
            else:
                btns_with_total[1].click()
        else:
            if total_type == 'OVER':
                btns_with_total[2].click()
            else:
                btns_with_total[3].click()

    def do_handicap_bet(self, bet_name, bet_field):

        # связка кнопка - название ставики
        key_bet_row = 'row-common--33mLE'
        # класс  отдела с форой на определенную команду.
        key_command_handicap_zone = 'grid--6A7cH'
        # ключ к кнопке тотал
        key_btn_total_bet = 'cell-wrap--LHnTw _width-fixed--dhzsT'

        command_index = int(float(bet_name.replace('_', ' ').replace('  ', ' ').split(' ')[-1][1]) - 1)
        if bet_name.split('(')[1][0] == '-':
            handicap_name = 'Фора (' + bet_name.split('(')[1]
        else:
            handicap_name = 'Фора (+' + bet_name.split('(')[1]
        print(command_index)

        command_zone = bet_field.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_command_handicap_zone))[
            command_index]

        rows = command_zone.find_elements(By.XPATH, './/div[@class="{}"]'.format(key_bet_row))

        true_row = None
        for row in rows:
            bet_name = row.text.split('\n')[0].replace('‑', '-')
            print(bet_name)
            # print(row.text)
            if bet_name == handicap_name:  # Сравниваем с данными из вилки
                true_row = row
                print('Получил')
                # break

        if true_row:
            btn_handicap_bet = true_row.find_element(By.XPATH, './/div[@class="{}"]'.format(key_btn_total_bet))
            if btn_handicap_bet:
                btn_handicap_bet.click()
            else:
                print('Нет такой ставки')
        else:
            print('Нет такой ставки')

    def get_bet_field(self, bet_name):

        key_fields_with_bet = 'market-group-box--z23Vv'
        key_fields_name = 'text-new--2WAqa'

        time.sleep(1)
        needful_field = self.get_field_name(bet_name)
        field_with_our_bet = None

        fields = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_fields_with_bet))

        if not fields:
            print('Не найдено ни одно поле со ставкой')
            return None

        for field in fields:
            try:
                field_name = field.find_element(By.XPATH, './/div[@class="{}"]'.format(key_fields_name)).text
            except:
                continue

            print(field_name)
            if field_name == needful_field:
                field_with_our_bet = field
                break

        return field_with_our_bet

    def get_field_name(self, bet_name):

        dict_fields_names = {
            'WIN': 'Исход',
            'SET_01_WIN': 'Исход 1‑й карты',
            'SET_02_WIN': 'Исход 2‑й карты',
            'SET_03_WIN': 'Исход 3‑й карты',
            'SET_04_WIN': 'Исход 4‑й карты',
            'SET_05_WIN': 'Исход 5‑й карты',
            # total
            'SETS_TOTALS': 'Количество карт',
            'TOTALS': 'Тотал',  # ЕЩЁ НЕ ВСТРЕЧАЛ
            'SET_01_TOTALS': 'Тотал на 1‑й карте',
            'SET_02_TOTALS': 'Тотал на 2‑й карте',
            'SET_03_TOTALS': 'Тотал на 3‑й карте',
            'SET_04_TOTALS': 'Тотал на 4‑й карте',
            'SET_05_TOTALS': 'Тотал на 5‑й карте',
            # handicap
            'HANDICAP': 'Фора по картам',  ### ВОЗМОЖНО НАДО ИЗМЕНИТЬ
            'SETS_HANDICAP': 'Фора по картам',
            'SET_01_HANDICAP': 'Исход 1‑й карты с учетом форы',
            'SET_02_HANDICAP': 'Исход 2‑й карты с учетом форы',
            'SET_03_HANDICAP': 'Исход 3‑й карты с учетом форы',
            'SET_04_HANDICAP': 'Исход 4‑й карты с учетом форы',
            'SET_05_HANDICAP': 'Исход 5‑й карты с учетом форы',
            '': '',
        }
        # Разбиваем строку на массив слов (роль разделителя - подчеркивание)
        # и соединяем массив в строку без последнего эллемента
        bet_field = '_'.join(bet_name.replace('__', ' ').replace('_', ' ').replace('  ', ' ').split(' ')[:-1])
        try:
            field_name = dict_fields_names[bet_field]
            print('Поле имя: ', field_name)
        except:
            field_name = None
            print(bet_field)
        return field_name

    def open_bet_part(self, bet):

        # активная вкладка раздела ставок
        key_active_game_part = 'tab--4RNtV _state_selected--408s1'
        # осталные вкладки радела ставок
        key_game_part = 'tab--4RNtV'

        page_is_clicked = False

        game_part = self.get_page_name(bet)
        active_page = self.driver.find_element(By.XPATH, '//div[@class="{}"]'.format(key_active_game_part)).text

        if not active_page == game_part:
            another_pages = self.driver.find_elements(By.XPATH, '//div[@class="{}"]'.format(key_game_part))
            for page in another_pages:
                page_name = page.text
                if page_name == game_part:
                    page.click()
                    page_is_clicked = True
                    break
        else:
            page_is_clicked = True

        if page_is_clicked:
            print('Нашли нужную страницу')
            return True
        else:
            print('Не удалось найти необходимый раздел')
            print('Активная страница -', active_page)
            print('Необходимая страница - ', game_part)
            return False

    def get_page_name(self, bet):

        transform_bet = bet.replace('_', ' ').replace('  ', ' ').split(' ')
        if transform_bet[0] == 'SET':
            i = (int(float(transform_bet[1][1])))
        else:
            i = 0

        if i == 0:
            print(bet, ":", 'МАТЧ')
            return 'МАТЧ'
        else:
            print(bet, ":", f'{i}-Я КАРТА')
            return f'{i}-Я КАРТА'

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