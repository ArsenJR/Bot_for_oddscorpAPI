from AllLibraries import *

Login = ''
Password = ''

class DialogToLogIn(QDialog):
    def __init__(self, bk_name,parent=None):
        super().__init__(parent)


        self.setWindowTitle("Log in")
        self.resize(600,400)

        self.lable = QtWidgets.QLabel(f'Введите логин и пароль для {bk_name}:', self)
        self.lable.setGeometry((QtCore.QRect(70, 70, 300, 30)))
        self.lable.setObjectName('lable')

        self.txt_Login = QtWidgets.QLineEdit('', self)
        self.txt_Login.setGeometry((QtCore.QRect(70, 100, 250, 30)))
        self.txt_Login.setPlaceholderText('Логин')
        self.txt_Login.setObjectName('txt_Login')

        self.txt_password = QtWidgets.QLineEdit('', self)
        self.txt_password.setGeometry((QtCore.QRect(70, 150, 250, 30)))
        self.txt_password.setPlaceholderText('Пароль')
        self.txt_password.setObjectName('txt_password')

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn, self)
        self.buttonBox.setGeometry((QtCore.QRect(350, 270, 240, 200)))
        self.buttonBox.accepted.connect(self.save_login_password)
        self.buttonBox.rejected.connect(self.reject)

    def save_login_password(self):
        login = self.txt_Login.text()
        password = self.txt_password.text()
        if login and password:
            global Login, Password
            Login = login
            Password = password
            self.accept()
        else:
            self.lable.setStyleSheet("color: red")