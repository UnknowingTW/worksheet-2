import random

#     Framework class for various account kinds

class BankAccount:
    def __init__(self, account_id, passcode, account_category, funds=0):
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds
        
    # Method to deposit cash
    def deposit(self, amount):
        if amount > 0:
            self.funds += amount
            return "Deposit Completed"
        return "Invalid amount for deposit."
    
    # Method to withdraw cash
    def withdraw(self, amount):
        if 0 < amount <= self.funds:
            self.funds -= amount
            return "Withdrawal Completed"
        return "Insufficient funds or invalid withdrawal sum."
    
    # Method to deliver cash to another account
    def transfer(self, amount, recipient_account):
        withdrawal_msg = self.withdraw(amount)
        if withdrawal_msg == "Withdrawal Completed":
            recipient_account.deposit(amount)
            return "Transfer Completed"
        return withdrawal_msg

# Acquired class for Personal accounts
class PersonalAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Personal", funds)

# Acquired class for Business accounts
class BusinessAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Business", funds)

# Banking System class to manage accounts and Communication
class BankingSystem:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    # Load accounts from file
    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    account_id, passcode, account_category, funds = line.strip().split(",")
                    funds = float(funds)  # Convert funds to float
                    if account_category == "Personal":
                        account = PersonalAccount(account_id, passcode, funds)
                    else:
                        account = BusinessAccount(account_id, passcode, funds)
                    accounts[account_id] = account  # Add account to the dictionary
        except FileNotFoundError:
            pass
        return accounts

    # Save accounts to file
    def save_accounts(self):
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.account_id},{account.passcode},{account.account_category},{account.funds}\n")

    # Create a new account and add it to the network
    def create_account(self, account_type):
        account_id = str(random.randint(10000, 99999))  # Generate random account ID
        passcode = str(random.randint(10000, 99999))  # Generate random passcode
        if account_type == "Personal":
            account = PersonalAccount(account_id, passcode)
        else:
            account = BusinessAccount(account_id, passcode)
        self.accounts[account_id] = account  # Add new account to the dictionary
        self.save_accounts()  # Save changes
        return account

    # Log in to an existing account
    def login(self, account_id, passcode):
        account = self.accounts.get(account_id)
        if account and account.passcode == passcode:
            return account
        raise ValueError("Account number or password is not recognized")
    
    # Delete an existing account from the network
    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")

# Main function to run the banking system
def main():
    bank = BankingSystem()
    while True:
        # Display main menu
        print("\nHello. How can I assist you?\n1. Open Account\n2. Login to your Account\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Open new account
            account_type = input("Select account type {1 for Personal, 2 for Business}: ")
            if account_type == "1":
                account = bank.create_account("Personal")
            elif account_type == "2":
                account = bank.create_account("Business")
            else:
                print("Unsupported account type")
                continue
            print(f"Account created. Account id: {account.account_id}, Passcode: {account.passcode}")

        elif choice == "2":
            # Log in to existing account
            account_id = input("Enter your account id: ")
            passcode = input("Enter your passcode: ")
            try: 
                account = bank.login(account_id, passcode)
                while True:
                    # Display account menu
                    print("\n1. Check Funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Delete Account\n6. Logout")
                    action = input("Enter your choice: ")

                    if action == "1":
                        # Check account balance
                        print(f"Your funds is {account.funds}")
                    elif action == "2":
                        # Deposit money
                        amount = float(input("Enter amount to deposit: "))
                        print(account.deposit(amount))
                        bank.save_accounts()
                    elif action == "3":
                        # Withdraw money
                        amount = float(input("Please input the withdrawal amount: "))
                        print(account.withdraw(amount))
                        bank.save_accounts()
                    elif action == "4":
                        # Transfer money to another account
                        recipient_id = input("Enter recipient account id: ")
                        amount = float(input("Enter amount to transfer: "))
                        try:
                            recipient_account = bank.accounts[recipient_id]
                            print(account.transfer(amount, recipient_account))
                            bank.save_accounts()
                        except KeyError:
                            print("Recipient account does not exist.")
                    elif action == "5":
                        # Delete account
                        bank.delete_account(account_id)
                        print("Account deletion completed.")
                        break
                    elif action == "6":
                        # Logout
                        break
                    else:
                        print("Please select a valid option.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            # Exit the program
            break
        else:
            print("Select a valid option")

if __name__ == "__main__":
    main()