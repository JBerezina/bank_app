from asyncio.windows_events import NULL
from random import randint
import datetime 
import pandas as pd


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_users = client.bank_app
users = db_users.u

class Bank():
    start_date="01/01/2022"
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
    
    def show_account_details(self):
        for date in self.transaction_history:
            self.trans +=  "\n              "+str(date) + ": " + str(self.transaction_history[date])
         
        print("Name : ", self.name)
        print("Account Number : ", self.account_number)
        print("Phone : ", self.phone)
        print("Email : ", self.email)
        print("Balance : ", self.balance)
        print("Password :", self.password)
        print("Transaction history: ", self.trans)

    def deposit(self, amount):

        #CREATE DICTIONARY FOR TRANSACTION AND BALANCE AND SET DATE AS KEY AND AMOUNT AS VALUE
        if len(self.transaction_history) == 0:
            self.start_date = pd.to_datetime("01/01/2022")
        else:
            self.start_date = pd.to_datetime(list(self.transaction_history.keys())[-1]) +  pd.DateOffset(days=5)

        self.amount=amount
        self.balance +=self.amount
        self.transaction_history[datetime.datetime.strftime(self.start_date, "%m/%d/%y")] = self.amount
        self.balance_history[datetime.datetime.strftime(self.start_date, "%m/%d/%y")] = self.balance
        print("Account balance has been updated  : $", self.balance)


    def withdraw(self, amount):
        self.amount=amount
        
        if len(self.transaction_history) == 0:
            self.start_date = pd.to_datetime("01/01/2022")
        else:
            self.start_date = pd.to_datetime(list(self.transaction_history.keys())[-1]) +  pd.DateOffset(days=5)

        if self.amount > self.balance:
            print("Insufisient balance. Available balance is $", self.balance)
        else: 
            self.balance -= self.amount
            print("Account balance has been updated  : $", self.balance )
       
        self.transaction_history[datetime.datetime.strftime(self.start_date, "%m/%d/%y")] = int("-" + str(self.amount))
        self.balance_history[datetime.datetime.strftime(self.start_date, "%m/%d/%y")] = self.balance

    def view_balance(self):
        print("Account balance is :", self.balance)

   
     