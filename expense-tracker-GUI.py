import tkinter as tk
from tkinter import ttk
import json


class ExpenseTracker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("560x680")
        self.window.resizable(False, False)

        self.bg_color = "#1E1E2E"
        self.card_color = "#25273C"
        self.text_color = "#EAEAEA"
        self.entry_color = "#31344A"
        self.accent_color = "#89B4FA"
        self.success_color = "#00C896"
        self.danger_color = "#FF5C5C"

        self.window.configure(bg=self.bg_color)

        self.expenses = self.load_expenses()

        self.setup_styles()

        self.frame = ttk.Frame(self.window, style="Card.TFrame")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()
        self.refresh_list()

        self.window.mainloop()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background=self.card_color)

        style.configure(
            "Title.TLabel",
            background=self.card_color,
            foreground=self.accent_color,
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Label.TLabel",
            background=self.card_color,
            foreground=self.text_color,
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Modern.TEntry",
            fieldbackground=self.entry_color,
            foreground=self.text_color,
            padding=8,
            borderwidth=0
        )

        style.configure(
            "Add.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=10
        )

        style.map(
            "Add.TButton",
            background=[("!disabled", self.success_color)]
        )

        style.configure(
            "Delete.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=10
        )

        style.map(
            "Delete.TButton",
            background=[("!disabled", self.danger_color)]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.entry_color,
            background=self.entry_color,
            foreground=self.text_color,
            arrowcolor=self.text_color,
            padding=8
        )

        self.window.option_add("*TCombobox*Listbox.background", self.entry_color)
        self.window.option_add("*TCombobox*Listbox.foreground", self.text_color)
        self.window.option_add("*TCombobox*Listbox.selectBackground", self.accent_color)
        self.window.option_add("*TCombobox*Listbox.selectForeground", "#000000")

        style.configure(
            "Treeview",
            background=self.entry_color,
            foreground=self.text_color,
            fieldbackground=self.entry_color,
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.accent_color,
            foreground="black",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", self.accent_color)],
            foreground=[("selected", "black")]
        )

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    def refresh_list(self):
        total = 0

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, expense in enumerate(self.expenses):
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                "end",
                values=(
                    expense["Expense"],
                    f"₹{expense['Amount']:.2f}",
                    expense["Category"]
                ),
                tags=(tag,)
            )

            total += expense["Amount"]

        self.totalLabel.config(text=f"Total Expenses: ₹{total:.2f}")

    def delete_button(self):
        selected = self.tree.selection()

        if not selected:
            self.messageLabel_3.config(text="Select an expense to delete!", fg=self.danger_color)
            return

        index = self.tree.index(selected[0])
        del self.expenses[index]

        self.save_expenses()
        self.refresh_list()

        self.messageLabel_3.config(text="Expense Deleted Successfully", fg=self.success_color)

    def add_button(self):
        name = self.expenseEntry.get().strip()

        if not name:
            self.messageLabel_1.config(text="Expense name cannot be empty!")
            return

        try:
            amount = float(self.amountEntry.get())
            if amount <= 0:
                self.messageLabel_2.config(text="Amount must be greater than 0!")
                return
        except ValueError:
            self.messageLabel_2.config(text="Amount must contain numbers only!")
            return

        expense = {
            "Expense": name,
            "Amount": amount,
            "Category": self.category_var.get()
        }

        self.expenses.append(expense)
        self.save_expenses()

        self.expenseEntry.delete(0, tk.END)
        self.amountEntry.delete(0, tk.END)

        self.messageLabel_1.config(text="")
        self.messageLabel_2.config(text="")
        self.messageLabel_3.config(text="Expense Added Successfully", fg=self.success_color)

        self.refresh_list()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="💰 EXPENSE TRACKER",
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=4, pady=(10, 25))

        ttk.Label(
            self.frame,
            text="Expense Name",
            style="Label.TLabel"
        ).grid(row=1, column=0, columnspan=4, sticky="w", padx=20)

        self.expenseEntry = ttk.Entry(self.frame, font=("Segoe UI", 12))
        self.expenseEntry.grid(row=2, column=0, columnspan=4, padx=20, sticky="ew")

        self.messageLabel_1 = tk.Label(self.frame, bg=self.card_color, fg=self.danger_color)
        self.messageLabel_1.grid(row=3, column=0, columnspan=4)

        ttk.Label(
            self.frame,
            text="Amount",
            style="Label.TLabel"
        ).grid(row=4, column=0, columnspan=4, sticky="w", padx=20, pady=(10, 0))

        self.amountEntry = ttk.Entry(self.frame, font=("Segoe UI", 12))
        self.amountEntry.grid(row=5, column=0, columnspan=4, padx=20, sticky="ew")

        self.messageLabel_2 = tk.Label(self.frame, bg=self.card_color, fg=self.danger_color)
        self.messageLabel_2.grid(row=6, column=0, columnspan=4)

        self.category_var = tk.StringVar(value="Food")

        self.category_menu = ttk.Combobox(
            self.frame,
            textvariable=self.category_var,
            state="readonly",
            values=["Food", "Transport", "Shopping", "Bills", "Other"]
        )

        self.category_menu.grid(row=7, column=0, columnspan=4, padx=20, pady=15, sticky="ew")

        ttk.Button(
            self.frame,
            text="ADD EXPENSE",
            command=self.add_button,
            style="Add.TButton"
        ).grid(row=8, column=1, padx=5, pady=10, sticky="ew")

        ttk.Button(
            self.frame,
            text="DELETE",
            command=self.delete_button,
            style="Delete.TButton"
        ).grid(row=8, column=2, padx=5, pady=10, sticky="ew")

        self.messageLabel_3 = tk.Label(
            self.frame,
            bg=self.card_color,
            fg=self.success_color,
            font=("Segoe UI", 10, "bold")
        )
        self.messageLabel_3.grid(row=9, column=0, columnspan=4, pady=10)

        self.tree = ttk.Treeview(
            self.frame,
            columns=("Expense", "Amount", "Category"),
            show="headings",
            height=4
        )

        self.tree.heading("Expense", text="Expense")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")

        self.tree.column("Expense", width=220)
        self.tree.column("Amount", width=120, anchor="center")
        self.tree.column("Category", width=120, anchor="center")

        self.tree.tag_configure("evenrow", background="#31344A")
        self.tree.tag_configure("oddrow", background="#2A2D40")

        self.tree.grid(row=10, column=0, columnspan=4, padx=20, pady=(10, 15))

        self.totalLabel = tk.Label(
            self.frame,
            text="Total Expenses: ₹0.00",
            bg=self.card_color,
            fg=self.accent_color,
            font=("Segoe UI", 16, "bold")
        )
        self.totalLabel.grid(row=11, column=0, columnspan=4, pady=(5, 15))


app = ExpenseTracker()
