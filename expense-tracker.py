import re
from expense import Expense
import calendar
import datetime

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()
    
    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expense.
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    print(f"Getting User Expense!")
    
    # Get a valid expense name (only letters allowed)
    while True:
        expense_name = input("Enter expense name: ")
        if re.match("^[A-Za-z ]+$", expense_name):  # Only letters and spaces allowed
            break
        else:
            print("Invalid input. Please enter a valid expense name using only letters and spaces.")

    # Get a valid expense amount (only numbers allowed)
    while True:
        try:
            expense_amount = input("Enter expense amount: ")
            if expense_amount.replace(".", "", 1).isdigit() and expense_amount.count('.') <= 1:  # Only numbers and one decimal point allowed
                expense_amount = float(expense_amount)
                if expense_amount > 0:
                    break
                else:
                    print("Amount should be a positive number. Please try again.")
            else:
                print("Invalid amount. Please enter a valid numeric value.")
        except ValueError:
            print("Invalid amount. Please enter a valid numeric value.")

    # Define categories
    expense_categories = [
       "🍔 Food",
       "🏠 Home",
       "💼 Work",
       "🎉 Fun",
       "✨ Misc",
    ]

    # Get a valid category selection
    while True:
        print("Select a category")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
        
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}") 
    try:
        with open(expense_file_path, "a") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    except Exception as e:
        print(f"Error while saving expense: {e}")

def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expense!")
    expenses = []
    
    # Read expenses from file
    try:
        with open(expense_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name, amount=float(expense_amount), category=expense_category
                )
                expenses.append(line_expense)
    except FileNotFoundError:
        print("Expense file not found. Please make sure the file exists.")
        return
    except Exception as e:
        print(f"Error while reading expenses: {e}")
        return

    # Categorize expenses
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    # Print categorized expenses
    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():  
        print(f" {key}: ${amount:.2f}") 

    # Calculate total spent and remaining budget
    total_spent = sum([x.amount for x in expenses])  
    print(f"💵 Total Spent: ${total_spent:.2f}") 

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    # Calculate remaining days in month
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    print(f"Remaining days in this month: {remaining_days}")

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))
    else:
        print("End of month! No remaining days.")

def green(text):
    return f"\033[92m{text}\033[0m"

class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __str__(self):
        return f"{self.name} | {self.category} | ${self.amount:.2f}"

if __name__ == "__main__":
    main()

