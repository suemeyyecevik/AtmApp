import os
from datetime import datetime
import locale

path = 'accounts.csv'

country_locales = {
    "TR": "tr_TR.UTF-8",  # Türkiye - Türk Lirası (₺)
    "DE": "de_DE.UTF-8",  # Almanya - Euro (€)
    "NL": "nl_NL.UTF-8",  # Hollanda - Euro (€)
    "US": "en_US.UTF-8",  # Amerika - Amerikan Doları ($)
    "GB": "en_GB.UTF-8",  # Ingiltere - Pound (£)
}

def OpenFile(path):
    if os.path.exists(path):
        return open(path, "r+", encoding="UTF-8")
    else:
        return open(path, "w+", encoding="UTF-8")
    
# GetAccounts fonksiyonu ile csv dosyamizdaki verileri 
# bir dictionary icine alip bu dictionary ile calisicaz.
# pseudocode daki bellege alma islemini GetAccounts fonksiyonu ile yapmis oluyoruz. 
def GetAccounts():
    file = OpenFile(path)
    accounts_list = file.readlines()  # hesaplarimizin listesi. Her satir bir list elemani.
    file.close()
    account_dict = {}
    for record in accounts_list:
        account_number, account_type, holder_name, balance, password, transactions = record.strip().split(";")
        account_dict[account_number] = {
            "holder_name":holder_name,
            "account_number": account_number,
            "account_type": account_type,
            "balance":float(balance),
            "password":password,
            "transactions":transactions.split("|") if transactions else []
        }
    return account_dict   



def CreateAccount(accounts):
    # kullanici ismini alalim
    holder_name = input("Please enter account owner name: ")
    # hesap turunu ogrenme
    account_type = SetAccountType()
    # Hesap numarasi olusturma
    # account_number = str(int(datetime.now().timestamp()))[-6:] bu sekilde de yapilabilir. 
    account_number = str(datetime.now().timestamp()).replace('.', '')[-6:]
    # password create etme
    password = input("Please make a password: ")
    # validation
    while len(password) != 4:
        print("Your password must be 4 digits!")
        password = input("Please make a valid password: ")
        
    accounts[account_number] = {
        "holder_name":holder_name,
        "account_number": account_number,
        "account_type": account_type,
        "balance": 0.0,
        "password":password,
        "transactions": []
    }
    
    recordAccounts(accounts)
    print(f"Your account is created.  {account_number}")
    

# createAccount(accounts)
    
def SetAccountType():
    type_menu = """
    Please select an account type:
        1 - ₺ (Turkish Liras) 
        2 - € (Euro)
        3 - £ (Pound)
        4 - $ (USD)
    """
    selected_type = input(type_menu)
    
    match selected_type:
        case "1":
            account_type = country_locales['TR']
        case "2":
            account_type = country_locales['DE']
        case "3":
            account_type = country_locales['GB']
        case "4":
            account_type = country_locales['US']
        case _:
            print("Please select valid currency!")
            return SetAccountType()

    # locale.setlocale(locale.LC_ALL, account_type)
    
    return account_type

# test ettik
# hesap_turu = SetAccountType()
# print(locale.currency(2313213321.78, grouping=True))

# dosyaya kaydetme 
def recordAccounts(accounts):
    file = OpenFile(path)
    file.seek(0)  # imleci dosyanin en basina tasidik. 
    file.truncate()  # dosyayi temizledik.
    for account in accounts.values():
        transaction_str = "|".join(account['transactions'])
        # account_number, account_type, holder_name, balance, password, transactions
        file.write(f"{account['account_number']};{account['account_type']};{account['holder_name']};{account['balance']};{account['password']};{transaction_str}\n")
    file.close()  # dosyayi kapattik. 
        

# CreateAccount(accounts)

def LoginAccount(accounts):
    
    while True:
        account_number = input("Please enter your account number (Press 'q' to Exit): ")
        
        if account_number == 'q':
            return None
        
        if account_number not in accounts:
            print("The account is not found!")
            continue
        
        password = input("Please enter your password: ")
        
        if accounts[account_number]['password'] == password:
            print(f"\nWelcome, {accounts[account_number]['holder_name']}!\n")
            return account_number  # bunu kullanabiliriz diye return ettirdik.(main de kullandik.) 
        else:
            print("Incorrect Password!")


def UserMenu(accounts, account_number):
    USER_MENU = f"""
    Your Account Number: {account_number}
    1 - Deposit Money
    2 - Withdraw Money
    3 - Balance
    4 - Transaction History
    5 - Exit
    """
    while True:
        print(USER_MENU)
        
        process = input("Your Process: ")
        
        if process == '1':
            DepositMoney(accounts, account_number)
        elif process == '2':
            WithdrawMoney(accounts, account_number)
        elif process == '3':
            Balance(accounts, account_number)
        elif process == '4':
            TransactionHistory(accounts, account_number)
        elif process == '5':
            print("Your session has ended.")
            break
        else:
            print("Invalid Selection!")
        
def DepositMoney(accounts, account_number):
    try:
        amount = float(input("Amount the Deposit: ")) 
        if amount <= 0:
            print("invalid amount!")
            return 
    except ValueError:
        print("Please enter valid amount!")
        return 
    
    # kisinin hesabina girilen miktari ekle
    accounts[account_number]['balance'] += amount
    # islem gecmisi (hesap dokumu - log)
    accounts[account_number]['transactions'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DEPOSIT: +{amount}")
    
    # kayit
    recordAccounts(accounts)
    
    
    print(f"New Balance: {locale.currency(accounts[account_number]['balance'], grouping=True)}")
    
    
def WithdrawMoney(accounts, account_number):
    try:
        amount = float(input("Amount the Withdraw: ")) 
        if amount <= 0:
            print("invalid amount!")
            return 
    except ValueError:
        print("Please enter valid amount!")
        return 
    
    # Hesapta yeterli para var mi?
    if accounts[account_number]['balance'] > amount:
        accounts[account_number]['balance'] -= amount
        # islem gecmisi (hesap dokumu - log)
        accounts[account_number]['transactions'].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WITHDRAW AMOUNT: -{amount}")
  
        # kayit
        recordAccounts(accounts)
        # locale.setlocale(locale.LC_ALL, accounts[account_number]['account_type'])
        print(f"New Balance: {locale.currency(accounts[account_number]['balance'], grouping=True)}")
    else:
        print("Insufficient Balance!")
        
        
def Balance(accounts, account_number):
    print(f"Current Balance: {locale.currency(accounts[account_number]['balance'], grouping=True)}\n")


def TransactionHistory(accounts, account_number):
    print("\n---Transaction History---")
    for trasaction in accounts[account_number]['transactions']:
        print(trasaction)
    print(f"Current Balance: {locale.currency(accounts[account_number]['balance'], grouping=True)}\n")

# Ana menu
MENU = """
Please select the process you want to take: 
1 - Open New Account
2 - Login Account
3 - Exit
"""

def main():
    accounts = GetAccounts()  # accounts degiskenine kayitlarimizi tutan dict'i atadik.
    
    while True:
        process = input(MENU)
        if process == '1':
            CreateAccount(accounts)
            locale.setlocale(locale.LC_ALL, accounts[account_number]['account_type'])
        elif process == '2': 
            account_number = LoginAccount(accounts)
            locale.setlocale(locale.LC_ALL, accounts[account_number]['account_type'])
            if account_number:
                UserMenu(accounts, account_number)
        elif process == '3': 
            print("Your session has ended.")
            print("Thank you for banking with us. See you again!")
            break
        else:
            print("Invalid Selection!")
    
    
        
if __name__ == "__main__":
    main()


    
# TODO nesne yonelimli yap
# qt designer (https://doc.qt.io/qt-6/qtdesigner-manual.html). Gorsellestirme (ui uzantili dosyadan view.py)
# from PyQt5 import uic
# ui_filename = "EqualGrapher.ui"
# py_ui_filename = "view.py"

# with open(py_ui_filename, "w", encoding="utf-8") as fout:
#     uic.compileUi(ui_filename, fout)
# 
# password 3 kere yanlis girildiginde bloke. 
# ayni kisi hem euro, hem dolar hesabi acmak isterse
# veri tabani eklenebilir. (sqLite ile yapilabilir cunku basit bir proje.)






     


    





    
    

    
        
    

