import random
import sqlite3

account_number = ""
pin = 0
connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
customer = " "


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                        number TEXT UNIQUE, pin TEXT, balance INTEGER DEFAULT 0);''')
    connection.commit()


def create_new_account():
    # global accounts
    global pin
    pin = '{:04d}'.format(random.randrange(0000, 9999))
    mii = 400000
    account_id = '{:09d}'.format(random.randrange(000000000, 999999999))
    global account_number
    account_number = str(mii) + str(account_id)

    # Make the account number iterable:
    original_number = list(account_number)

    control_number = []
    # Luhn's Algorithm :
    for i in original_number[1::2]:
        control_number.append(int(i))
    for i in original_number[0::2]:
        i = int(i) * 2
        if i > 9:
            i = i - 9
            control_number.append(i)
        else:
            control_number.append(i)

    check_sum = sum(control_number)

    mod10 = check_sum % 10

    if mod10 == 0:
        check_digit = 0
    else:
        check_digit = 10 - int(str(check_sum)[-1])

    account_number = account_number + str(check_digit)
    save_account(account_number, pin)

    print("Your card has been created\nYour card number:")
    print(account_number, "\nYour card PIN:")
    print(pin)
    """print("\n")"""


def save_account(number, save_pin):
    cursor.execute("INSERT INTO card (number, pin) VALUES(?,?)", (number, save_pin))
    connection.commit()


class CustomerAccount:
    def __init__(self, number, customer_pin):
        cursor.execute("SELECT number, pin, balance FROM card WHERE number = ? AND pin =?;",
                       (number, customer_pin))
        try:
            self.user_retrieved_account = cursor.fetchone()
            self.account = self.user_retrieved_account[0]
            self.pin = self.user_retrieved_account[1]
            self.balance = self.user_retrieved_account[2]
        except TypeError:
            pass

    def show_balance(self):
        number = self.account
        pin_1 = self.pin  # changed pin to pin_1
        cursor.execute("SELECT number, pin, balance FROM card WHERE number = ? AND pin =?;",
                       (number, pin_1))
        self.user_retrieved_account = cursor.fetchone()
        self.balance = self.user_retrieved_account[2]
        connection.commit()
        print("Balance: ", self.balance)

    def add_income(self):
        income = int(input("Enter income:\n"))
        new_income = self.balance + income
        number = self.account
        pin_3 = self.pin
        cursor.execute("UPDATE card SET balance = ? WHERE number = ? AND pin =?;",
                       (new_income, number, pin_3))
        connection.commit()
        print("\n Income was added!\n")
        self.show_balance()

    def delete_account(self):
        number = self.account
        pin_2 = self.pin
        cursor.execute("DELETE FROM card WHERE number = ? AND pin =?;", (number, pin_2))
        connection.commit()
        print("The account has been closed!")


def transfer():
    class TransferAccount:
        def __init__(self, number):
            """Checks if transfer account is in database and transfer money"""

            try:
                cursor.execute("SELECT number, balance FROM card WHERE number = ?;", (number,))
                self.transfer_account_info = cursor.fetchone()
                self.account = self.transfer_account_info[0]
                self.balance = self.transfer_account_info[1]

            except AttributeError:
                print("Such a card does not exist.")

    transfer_account_number = input("Transfer:\n"
                                    "Enter card number:\n")

    if customer.account == transfer_account_number:
        print("You can't transfer money to the same account!")
        account_menu()

    def money_transfer():
        if transfer_account:
            transfer_money = input("Enter how much money you want to transfer:")
            if int(transfer_money) > int(customer.balance):
                print("Not enough money!")
            else:
                new_balance_trans = int(transfer_money) + transfer_account.balance
                new_balance_main = customer.balance - int(transfer_money)
                cursor.execute("UPDATE card SET balance = ? WHERE number = ?;",
                               (new_balance_trans, transfer_account.account))
                connection.commit()
                cursor.execute("UPDATE card SET balance = ? WHERE number =?;",
                               (new_balance_main, str(customer.account)))
                connection.commit()
                print("Success!")
        else:
            print("Such a card does not exist.")

    def validate_account(account__number):
        """Checks if the account is valid according to Luhn´s Algorithm
        parameter account_number is the account we want to validate
        Returns: True or False"""
        last_digit = account__number[-1]
        reduced_account_number = account__number[0:-1]
        control_number = []
        for i in reduced_account_number[1::2]:
            control_number.append(int(i))
        for i in reduced_account_number[0::2]:
            i = int(i) * 2
            if i > 9:
                i = i - 9
                control_number.append(i)
            else:
                control_number.append(i)

        check_sum = sum(control_number)
        check_sum = check_sum + (int(last_digit))
        mod10 = check_sum % 10
        if mod10 == 0:
            return True
        else:
            return False

    valid = validate_account(transfer_account_number)

    if valid:
        transfer_account = TransferAccount(transfer_account_number)
        money_transfer()
    else:
        print("Probably you made a mistake in the card number. Please try again!")


def log_in():
    user_input_account = input("Enter your card number:\n")
    user_input_pin = input("Enter your PIN:\n")
    global customer
    customer = CustomerAccount(user_input_account, user_input_pin)
    try:
        if customer.account:
            print("You have successfully logged in!")
            account_menu()
            return customer

    except AttributeError:
        print("Wrong card number or PIN!")
        main_menu()
    connection.commit()


def account_menu():
    choice2 = int(input("\n"
                        "1. Balance\n"
                        "2. Add income\n"
                        "3. Do transfer\n"
                        "4. Close account\n"
                        "5. Log out\n"
                        "0. Exit\n"))
    while choice2 != 0:
        if choice2 == 1:
            customer.show_balance()
            account_menu()
        elif choice2 == 2:
            customer.add_income()
            account_menu()
        elif choice2 == 3:
            transfer()
            account_menu()
        elif choice2 == 4:
            customer.delete_account()
            account_menu()
        elif choice2 == 5:
            print("You have successfully logged out!")
            main_menu()
    else:
        exit("Bye!")


def main_menu():
    choice = int(input("\n"
                       "1. Create an account\n"
                       "2. Log into account\n"
                       "0. Exit\n"))
    while choice != 0:
        if choice == 1:
            create_new_account()
            main_menu()
            """choice = int(input("\n"
                               "1. Create an account\n"
                               "2. Log into account\n"
                               "0. Exit\n"))"""
        elif choice == 2:
            log_in()

    else:
        exit("Bye!")



# _________________EXECUTE_______________________

create_table()
main_menu()
