from AllLibraries import *

class pinnacleDriver(QObject):

    def doWebDriver(self):
        self.driver = webdriver.Chrome()
        self.bk_link = 'https://www.betonproxy.shop/ru/'
        self.driver.get(self.bk_link)
        self.driver.maximize_window()
        time.sleep(3)
        try:
            # не нажимает, разобраться почему
            key_button_accept_cookie = 'style_button__2cht5 style_fullWidth__tyxzD ellipsis style_medium__1Uf0e dead-center style_tertiary__1XC1Z style_button__3eTui'
            button_accept_cookie = self.driver.find_element(By.XPATH,
                                                            '//button[@class="{}"]'.format(key_button_accept_cookie))
            button_accept_cookie.click()
        except:
            pass


    def log_in(self, login_password):
        login = login_password[0]
        password = login_password[1]

        # раскрываем бк на полный экран
        self.log_in_link = self.bk_link + 'account/login'
        self.driver.get(self.log_in_link)

        # ключ кноки "Вход"
        key_button_input = 'style_button__2cht5 style_fullWidth__tyxzD ellipsis style_large__2GNuq dead-center style_secondary__Cc5kq'

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
