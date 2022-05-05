from random import randint
import datetime 

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_users = client.bank_app
users = db_users.u

class Bank():
    day=1
    month=1
  
    trans=""

    def __init__(self, name, phone, email, account_number, balance, password, transaction_history, balance_history):
        self.name=name
        self.account_number = account_number
        self.phone=phone
        self.email=email
        self.balance = balance
        self.password= password
        self.transaction_history = transaction_history
        self.balance_history=balance_history

    def create_new_date(self):
        self.transaction_history
    
    def show_account_details(self):
        for date in self.transaction_history:
            self.trans +=  "\n"+str(date) + ": " + str(self.transaction_history[date])
         
        print("Name : ", self.name)
        print("Account Number : ", self.account_number)
        print("Phone : ", self.phone)
        print("Email : ", self.email)
        print("Balance : ", self.balance)
        print("Password :", self.password)
        print("Transaction history: ", self.trans)

    def deposit(self, amount):
        self.day+=2
        self.amount=amount
        self.balance +=self.amount
        self.transaction_history[(datetime.datetime(2022, self.month, self.day)).strftime("%x")] = self.amount
        self.balance_history[(datetime.datetime(2022, self.month, self.day)).strftime("%x")] = self.balance
        print("Account balance has been updated  : $", self.balance)
        print(self.transaction_history)


    def withdraw(self, amount):
        self.amount=amount
        self.day+=1

        if self.amount > self.balance:
            print("Insufisient balance. Available balance is $", self.balance)
        else: 
            self.balance -= self.amount
            print("Account balance has been updated  : $", self.balance )
       
        self.transaction_history[(datetime.datetime(2022, self.month, self.day)).strftime("%x")] = int("-" + str(self.amount))
        self.balance_history[(datetime.datetime(2022, self.month, self.day)).strftime("%x")] = self.balance
        print(self.transaction_history)

    def view_balance(self):
        print("Account balance is :", self.balance)

   
     