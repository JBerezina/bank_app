from asyncio.windows_events import NULL
import bank
import json
import re
import pymongo
from random import randint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_users = client.bank_app
users = db_users.u


#reading JSON file
def get_all_accounts():
    with open('accounts.json') as json_file:
        accounts = json.load(json_file)
        json_file.close()
        return accounts

def add_accounts_to_mongo_from_json():
    accounts=get_all_accounts()
    for user in accounts['data']['users']:
        if not users.find_one({'name':user['name']}):
            print(user)
            users.insert_one(user)


def create_new_account(full_name, phone, email, password, balance):
    a=""
    for name in full_name.split(" "):
        a +=name[0]
    account_number=a + str(randint(1000, 9999))

    if users.find_one({'email':  email}):
        print("This email exist")
    if users.find_one({'phone':  phone}):
        print("This phone exist")

    new_user={
        "name": full_name,
        "account_number": account_number,
        "phone": phone,
        "email": email,
        "balance": balance,
        "password": password,
        "transaction_history": {},
        "balance_history" : {}
    }

    users.insert_one(new_user)
    print("ACCOUNT CREATED")

def delete_account(email):
    users.delete_one({'email': email})
    print("YOUR ACCOUNT DELETED")
  
#VALIDATIONS
def check_if_email_and_password_exist(email, password):
    try:
        if users.find_one({'email': email}) and users.find_one({'password': password}):
            return True
        else:
            print("This email and password don't much our database")
            print("Please try again")   
    except BaseException:
        print("Sorry, cannot find connection to database!")

def validate_item(object_to_validate, regex):
   
    if re.fullmatch(regex, object_to_validate):
        return True
    else:
        return False

def validate_email_and_phone(item):
    validation = False
    inputed_item=""


    while not validation:
        if item=="email":
            
            inputed_item=input("Please enter your email: ").lower()    
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            validation = validate_item(inputed_item, regex)

            if not validation:
                print("Make sure to input correct email")
            else:
                break
        elif item == "phone":
         
            inputed_item = input("Please enter your full phone (format: +n-nnn-nnn-nnnn) ")
            regex = re.compile(r"\(?\d{3}\)?[-\s]\d{3}[-s]\d{4}|\d{10}")
            validation = validate_item(inputed_item, regex)
            if not validation:
                print("Make sure to input correct phone (format: +n-nnn-nnn-nnnn)")
            else:
                break
    return inputed_item
#-----------------------------------------------

def main():
    add_accounts_to_mongo_from_json()
    print("*"*30)
    print("WELCOME")
    print("*"*30)
    print("Q for exit the system")
    print("*"*30)

    while True:
        print("q for exit the system")
        client_exist=input("Are you existing client? yes or no: ").lower()
        

        if client_exist == "yes":
            email = validate_email_and_phone("email")
            password=int(input("Please enter your password"))
            print("*"*30)
            
            if check_if_email_and_password_exist(email, password):
                u=users.find_one({"email": email})
                new_user = bank.Bank(u['name'], u['phone'], u['email'], u['account_number'],  u['balance'], u['password'], u['transaction_history'], u['balance_history'])
                while True:
                    print("*"*30)
                  
                    print("Welcome " + new_user.name)
                    print("*"*30)
                    print("PLease pick your transation: ")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Show details")
                    print("5. Delete account")

                    print("6.Quit")

                    choice = int(input("Select your option: "))
                    print("*"*30)
                    if choice == 1:
                        while True:
                            try:
                                amount=int(input("How much do you want to deposit: "))
                            except ValueError:
                                print("TYPE CORRECT AMOUNT")
                            else:
                                new_user.deposit(amount)
                                break
                        
                    elif choice == 2:
                          while True:
                            try:
                                amount=int(input("How much do you want to withdraw: "))
                            except ValueError:
                                print("TYPE CORRECT AMOUNT")
                            else:
                                new_user.withdraw(amount)
                                break
                        
                    elif choice ==3:
                        print("\n")
                        new_user.view_balance()
                    elif choice == 4:
                        new_user.show_account_details() 
                    elif choice == 5:
                        delete_account(email)
                        break
                    elif choice == 6:
                        def update_database():
                            users.update_many({'name': new_user.name}, 
                            { '$set' :{"balance": new_user.balance, "transaction_history": new_user.transaction_history, "balance_history" : new_user.balance_history}})
                            print("Goodbuy")
                        update_database()
                        break
                    else:
                        print("Please choose given option")

        elif client_exist == "no":
            print("LETS CREATE ACCOUNT")

            #EMAIL VALIDATION 
            email = validate_email_and_phone("email")

            #PHONE VALIDATION
            phone = validate_email_and_phone("phone")

            full_name = input("Please enter your full name: ")
            password=int(input("Please enter your password"))
            balance = int(input("Please enter initial deposit: "))
            

            create_new_account(full_name, phone, email, password, balance)
            print("*"*30)
            print("Please SIGNIN again to access your account")
            
        elif client_exist == "q":
            break
        else:
            print("Make sure to input yes or no")
        

main()