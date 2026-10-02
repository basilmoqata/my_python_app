class BankAccount:

  def __init__(self, owner, balance=0.0):
    self.owner = owner
    self.__balance = balance  # رصيد خاص (Encapsulation)

  def deposit(self, amount):
    if amount > 0:
      self.__balance += amount
      print(f"Deposited: ${amount:.2f}")
    else:
      print("Invalid deposit amount.")

  def withdraw(self, amount):
    if amount > self.__balance:
      print("Insufficient funds.")
    elif amount <= 0:
      print("Invalid withdrawal amount.")
    else:
      self.__balance -= amount
      print(f"Withdrew: ${amount:.2f}")

  def get_balance(self, owner_name=None):
    return f"Account Owner: {self.owner} | Current Balance: ${self.__balance:.2f}"


# تجربة تطبيق الكلاس تماماً مثل الصورة
account = BankAccount("Mais", 500.0)

print(account.get_balance())
account.deposit(200.0)
account.withdraw(150.0)
print(account.get_balance())