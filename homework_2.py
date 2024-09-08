import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, \
    QFormLayout, QComboBox


class LoginPage(QWidget):
    def __init__(self, switch_to_exchange):
        super().__init__()
        self.switch_to_exchange = switch_to_exchange
        self.init_ui()

    def init_ui(self):
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.check_credentials)

        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "admin":
            self.switch_to_exchange()
        else:
            self.username_input.hide()
            self.password_input.hide()
            self.login_button.hide()
            label = QLabel("Incorrect password or username!", self)

            label.setAlignment(Qt.AlignCenter)
            self.layout().addWidget(label)



class ExchangePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Amount")
        self.from_currency = QComboBox(self)
        self.to_currency = QComboBox(self)

        self.from_currency.addItems(["USD", "EUR", "GEL"])
        self.to_currency.addItems(["USD", "EUR", "GEL"])

        self.convert_button = QPushButton("Convert", self)
        self.result_label = QLabel("Result:", self)

        layout = QFormLayout()
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("From Currency:", self.from_currency)
        layout.addRow("To Currency:", self.to_currency)
        layout.addRow("", self.convert_button)
        layout.addRow("", self.result_label)
        self.setLayout(layout)

        self.convert_button.clicked.connect(self.convert_currency)

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()

            rates = {
                ('USD', 'EUR'): 0.90,
                ('EUR', 'USD'): 1.11,
                ('GEL', 'USD'): 0.37,
                ('USD', 'GEL'): 2.69,
                ('EUR', 'GEL'): 2.98,
                ('GEL', 'EUR'): 0.34

            }

            if from_currency == to_currency:
                result = amount
            else:
                rate = rates.get((from_currency, to_currency), 1)
                result = amount * rate

            self.result_label.setText(f"Result: {result:.2f} {to_currency}")

        except ValueError:
            self.result_label.setText("Invalid amount")


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.login_page = LoginPage(self.show_exchange_page)
        self.exchange_page = ExchangePage()

        self.addWidget(self.login_page)
        self.addWidget(self.exchange_page)

        self.setWindowTitle("Currency exchange app")
        self.setGeometry(100, 100, 300, 200)
        self.setCurrentWidget(self.login_page)

    def show_exchange_page(self):
        self.setCurrentWidget(self.exchange_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
