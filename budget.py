class Category:

  #------------CONSTRUCTOR
  def __init__(self, name):
    self.name = name
    self.ledger = []

  #------------STR
  def __str__(self):
    # TITULO:
    title = self.name.center(30, '*')
    # CONTENIDO LEDGER:
    ledger_lines = ""
    for item in self.ledger:
      description = item['description'][:23].ljust(23)
      amount = format(item['amount'], '.2f').rjust(7)
      ledger_lines += f"{description}{amount}\n"

    # TOTAL:
    total = sum(item['amount'] for item in self.ledger)

    result = f"{title}\n{ledger_lines}"
    result += "Total: " + format(total, ".2f")

    return result

  #------------DEPOSIT
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  #------------TRANSFER
  def transfer(self, amount, anothercategory):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + anothercategory.name)
      anothercategory.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False

  #------------WITHDRAW
  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": amount * -1, "description": description})
      return True
    else:
      return False

  #------------GET_BALANCE
  def get_balance(self):
    total = sum(entry['amount'] for entry in self.ledger)
    return total

  #------------CHECK_FUNDS
  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    else:
      return True

#------------GET_WITHDRAWALS

  def get_withdrawals(self):
    withdrawals = sum(item['amount'] for item in self.ledger
                      if item['amount'] < 0)
    return abs(withdrawals)


#################################################################


def create_spend_chart(categories):
  total_withdrawals = sum(category.get_withdrawals()
                          for category in categories)
  percentages = [(category.get_withdrawals() / total_withdrawals) * 100
                 for category in categories]

  chart = "Percentage spent by category\n"
  for i in range(100, -10, -10):
    chart += str(i).rjust(3) + "| "
    for percentage in percentages:
      if percentage >= i:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"

  chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

  max_name_length = max(len(category.name) for category in categories)
  for i in range(max_name_length):
    chart += "     "
    for category in categories:
      if i < len(category.name):
        chart += category.name[i] + "  "
      else:
        chart += "   "
    if i < max_name_length - 1:
      chart += "\n"

  return chart
