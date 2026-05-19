import tkinter as tk
import json

class ExpenseTracker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("400x570")
        self.expenses = self.load_expenses()
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.create_widgets()
        self.refresh_list()
        self.window.mainloop()

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                expenses = json.load(file)
                return expenses
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    def refresh_list(self):
        total = 0
        index = 1
        self.listBox.delete(0,tk.END)
        for expense in self.expenses:
            self.listBox.insert(tk.END, f"{index}.{expense['Expense']:<15} | ₹{expense['Amount']:<7.2f}| {expense['Category']:<7}")
            total += expense["Amount"]
            index += 1
        self.totalLabel.config(text=f"Total: ₹{total:.2f}")

    def delete_button(self):
        selected = self.listBox.curselection()
        if not selected:
            self.messageLabel_3.config(text="Click on an expense to delete!")
        else:
            del self.expenses[selected[0]]
            self.save_expenses()
            self.refresh_list()
            self.messageLabel_3.config(text="Expense Deleted!")

    def add_button(self):
        name = self.expenseEntry.get()
        if name.strip() == "":
            self.messageLabel_1.config(text="expense name can't be empty!")
            return
        category = self.category_var.get()
        amount = float(self.amountEntry.get())
        if amount == 0 or amount < 0:
            self.messageLabel_2.config(text="Invalid amount!")
            return
        try:
            amount = float(self.amountEntry.get())
            expense =  {"Expense" : name,
                        "Amount" : amount,
                        "Category" : category}
            self.expenses.append(expense)
            self.save_expenses()
            self.expenseEntry.delete(0, tk.END)
            self.amountEntry.delete(0, tk.END)
            self.messageLabel_1.config(text="")
            self.messageLabel_2.config(text="")
            self.messageLabel_3.config(text="Expense Added!")

            self.refresh_list()

        except ValueError:
            self.messageLabel_2.config(text="expense amount should be numbers!")

    def create_widgets(self):
        self.topLabel = tk.Label(self.frame,
                              text="EXPENSE TRACKER APP",
                              font=("Consolas", 25, "bold"))
        self.topLabel.grid(row=0,column=0,columnspan=4)


        self.expenseLabel = tk.Label(self.frame,
                              text="Name of the expense",
                              font=("Consolas", 15, "bold"))
        self.expenseLabel.grid(row=1,column=0,columnspan=4)


        self.expenseEntry = tk.Entry(self.frame,
                                     font=("Consolas", 20))
        self.expenseEntry.grid(row=2,column=0,columnspan=4)

        self.messageLabel_1 = tk.Label(self.frame,
                              text="",
                              font=("Consolas", 12))
        self.messageLabel_1.grid(row=3,column=0,columnspan=4)


        self.amountLabel = tk.Label(self.frame,
                              text="Amount for the expense",
                              font=("Consolas", 15, "bold"))
        self.amountLabel.grid(row=4,column=0,columnspan=4)


        self.amountEntry = tk.Entry(self.frame,
                                     font=("Consolas", 20))
        self.amountEntry.grid(row=5,column=0,columnspan=4)

        self.messageLabel_2 = tk.Label(self.frame,
                              text="",
                              font=("Consolas", 12))
        self.messageLabel_2.grid(row=6,column=0,columnspan=4)

        self.category_var = tk.StringVar(value="Food")
        self.category_menu = tk.OptionMenu(self.frame,
                                           self.category_var,
                                           "Food", "Transport", "Shopping", "Bills", "Other")
        self.category_menu.grid(row=7,column=0,columnspan=4)
        self.category_menu.config(font=("Consolas", 15))

        self.addButton = tk.Button(self.frame,
                                   text="ADD",
                                   font=("Consolas", 30, "bold"),
                                   relief="raised",
                                   overrelief="ridge",
                                   bd=5,
                                   command=self.add_button)
        self.addButton.grid(row=8,column=1,columnspan=1,sticky="ew")

        self.deleteButton = tk.Button(self.frame,
                                   text="DEL",
                                   font=("Consolas", 30, "bold"),
                                   relief="raised",
                                   overrelief="ridge",
                                   bd=5,
                                   command=self.delete_button)
        self.deleteButton.grid(row=8,column=2,columnspan=1,sticky="ew")


        self.messageLabel_3 = tk.Label(self.frame,
                              text="",
                              font=("Consolas", 12))
        self.messageLabel_3.grid(row=9,column=0,columnspan=4,pady=5)


        self.listBox = tk.Listbox(self.frame,
                                  font=("Consolas", 13),
                                  width=40,
                                  height=6)
        self.listBox.grid(row=10,column=0,columnspan=4)


        self.totalLabel = tk.Label(self.frame,
                                    text="Total: ₹0",
                                    font=("Consolas", 15, "bold"))
        self.totalLabel.grid(row=11,column=0,columnspan=4)

app = ExpenseTracker()