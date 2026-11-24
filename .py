
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Main window
root = Tk()
root.title("Bank Management System")
root.geometry("550x780")
root.config(bg="#F3F6F9")
root.resizable(True, True)

# Bank details
balance = 0
total_deposit = 0
total_withdraw = 0
transactions = []

created = False
customer = ""
mobile = ""
account_no = 1001

# Colours
blue = "#173B57"
green = "#15966F"
red = "#C65353"
white = "#FFFFFF"
bg = "#F3F6F9"
grey = "#718096"


# Update account details on screen
def update_balance():

    balance_label.config(text=f"₹ {balance:.2f}")
    customer_label.config(text=f"Welcome, {customer}!")
    account_label.config(text=f"Account No: {account_no}")

    deposit_label.config(text=f"₹ {total_deposit:.2f}")
    withdraw_label.config(text=f"₹ {total_withdraw:.2f}")


# Save transaction details
def save_transaction(action, amount):

    time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    transactions.append(
        f"{action} | ₹ {amount:.2f} | {time}"
    )


# Clear input fields
def clear():

    name_entry.delete(0, END)
    mobile_entry.delete(0, END)
    amount_entry.delete(0, END)


# Create a new bank account
def create_account():

    global balance, created, customer, mobile

    name = name_entry.get().strip()
    phone = mobile_entry.get().strip()
    amount = amount_entry.get().strip()

    if name == "" or phone == "" or amount == "":
        messagebox.showerror("Error", "Please fill all details")
        return

    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Enter a valid name")
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Enter a valid mobile number")
        return

    if created:
        messagebox.showerror("Error", "Account already exists")
        return

    try:
        amount = float(amount)

        if amount < 0:
            messagebox.showerror("Error", "Invalid amount")
            return

        if amount != round(amount, 2):
            messagebox.showerror("Error", "Enter maximum 2 decimal places")
            return

    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")
        return

    customer = name
    mobile = phone
    balance = amount
    created = True

    save_transaction("Account Created", amount)

    update_balance()
    clear()

    name_entry.config(state="disabled")
    mobile_entry.config(state="disabled")
    create_button.config(state="disabled")

    messagebox.showinfo(
        "Success",
        f"Account created successfully!\n\n"
        f"Customer: {customer}\n"
        f"Account No: {account_no}"
    )

    status_label.config(
        text="Account created successfully!",
        fg=green
    )


# Deposit money
def deposit():

    global balance, total_deposit

    if not created:
        messagebox.showerror("Error", "Create account first")
        return

    try:
        amount = float(amount_entry.get())

        if amount <= 0 or amount != round(amount, 2):
            messagebox.showerror("Error", "Enter a valid amount")
            return

        if messagebox.askyesno(
            "Confirm Deposit",
            f"Do you want to deposit ₹ {amount:.2f}?"
        ):

            balance += amount
            total_deposit += amount

            save_transaction("Deposit", amount)

            update_balance()
            amount_entry.delete(0, END)

            status_label.config(
                text="Money deposited successfully!",
                fg=green
            )

    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")


# Withdraw money
def withdraw():

    global balance, total_withdraw

    if not created:
        messagebox.showerror("Error", "Create account first")
        return

    try:
        amount = float(amount_entry.get())

        if amount <= 0 or amount != round(amount, 2):
            messagebox.showerror("Error", "Enter a valid amount")
            return

        if amount > balance:
            messagebox.showerror(
                "Error",
                "Insufficient balance!"
            )
            return

        if messagebox.askyesno(
            "Confirm Withdrawal",
            f"Do you want to withdraw ₹ {amount:.2f}?"
        ):

            balance -= amount
            total_withdraw += amount

            save_transaction("Withdrawal", amount)

            update_balance()
            amount_entry.delete(0, END)

            status_label.config(
                text="Withdrawal successful!",
                fg=green
            )

    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")


# Show transaction history
def history():

    if not created:
        messagebox.showerror("Error", "Create account first")
        return

    win = Toplevel(root)
    win.title("Transaction History")
    win.geometry("470x400")
    win.config(bg=bg)

    Label(
        win,
        text="TRANSACTION HISTORY",
        font=("Segoe UI", 17, "bold"),
        bg=bg,
        fg=blue
    ).pack(pady=15)

    box = Listbox(
        win,
        width=53,
        height=15,
        font=("Segoe UI", 10),
        bg=white,
        fg=blue,
        bd=0
    )

    box.pack(padx=15, pady=10, fill="both", expand=True)

    for item in transactions:
        box.insert(END, item)


# Show account report
def report():

    if not created:
        messagebox.showerror("Error", "Create account first")
        return

    messagebox.showinfo(
        "Account Report",
        f"Customer Name: {customer}\n"
        f"Mobile Number: {mobile}\n"
        f"Account Number: {account_no}\n\n"
        f"Current Balance: ₹ {balance:.2f}\n"
        f"Total Deposits: ₹ {total_deposit:.2f}\n"
        f"Total Withdrawals: ₹ {total_withdraw:.2f}\n\n"
        f"Total Transactions: {len(transactions)}"
    )


# Button hover effect
def hover(button, color, hover_color):

    button.bind(
        "<Enter>",
        lambda e: button.config(bg=hover_color)
    )

    button.bind(
        "<Leave>",
        lambda e: button.config(bg=color)
    )


# Heading
header = Frame(root, bg=blue, height=75)
header.pack(fill="x")
header.pack_propagate(False)

Label(
    header,
    text="BANK",
    font=("Segoe UI", 25, "bold"),
    bg=blue,
    fg=white
).pack(side="left", padx=30, pady=12)

Label(
    header,
    text="BANKING SERVICES",
    font=("Segoe UI", 10, "bold"),
    bg=blue,
    fg="#B9D6E8"
).pack(side="right", padx=25)


# Dashboard heading
Label(
    root,
    text="Account Dashboard",
    font=("Segoe UI", 18, "bold"),
    bg=bg,
    fg=blue
).pack(anchor="w", padx=30, pady=(15, 3))

customer_label = Label(
    root,
    text="Welcome, New Customer!",
    font=("Segoe UI", 10, "bold"),
    bg=bg,
    fg=grey
)
customer_label.pack(anchor="w", padx=30)

account_label = Label(
    root,
    text="Account No: Not Created",
    font=("Segoe UI", 10),
    bg=bg,
    fg=grey
)
account_label.pack(anchor="w", padx=30, pady=3)


# Balance card
card = Frame(
    root,
    bg=blue,
    padx=20,
    pady=15
)
card.pack(fill="x", padx=30, pady=12)

Label(
    card,
    text="AVAILABLE BALANCE",
    font=("Segoe UI", 10, "bold"),
    bg=blue,
    fg="#B9D6E8"
).pack(anchor="w")

balance_label = Label(
    card,
    text="₹ 0.00",
    font=("Segoe UI", 27, "bold"),
    bg=blue,
    fg="#65E6C1"
)
balance_label.pack(anchor="w", pady=5)


# Deposit and withdrawal summary
summary = Frame(root, bg=bg)
summary.pack(fill="x", padx=30, pady=5)

Label(
    summary,
    text="TOTAL DEPOSITS",
    font=("Segoe UI", 9, "bold"),
    bg=bg,
    fg=green
).grid(row=0, column=0, padx=35)

Label(
    summary,
    text="TOTAL WITHDRAWALS",
    font=("Segoe UI", 9, "bold"),
    bg=bg,
    fg=red
).grid(row=0, column=1, padx=35)

deposit_label = Label(
    summary,
    text="₹ 0.00",
    font=("Segoe UI", 13, "bold"),
    bg=bg,
    fg=green
)
deposit_label.grid(row=1, column=0, pady=5)

withdraw_label = Label(
    summary,
    text="₹ 0.00",
    font=("Segoe UI", 13, "bold"),
    bg=bg,
    fg=red
)
withdraw_label.grid(row=1, column=1, pady=5)


# Account details section
form = Frame(root, bg=white, padx=20, pady=12)
form.pack(fill="x", padx=30, pady=10)

Label(
    form,
    text="CREATE BANK ACCOUNT",
    font=("Segoe UI", 12, "bold"),
    bg=white,
    fg=blue
).pack(anchor="w", pady=(0, 8))

Label(
    form,
    text="Customer Name",
    font=("Segoe UI", 10, "bold"),
    bg=white,
    fg=blue
).pack(anchor="w")

name_entry = Entry(
    form,
    font=("Segoe UI", 11),
    bd=1,
    relief="solid"
)
name_entry.pack(fill="x", pady=4, ipady=4)

Label(
    form,
    text="Mobile Number",
    font=("Segoe UI", 10, "bold"),
    bg=white,
    fg=blue
).pack(anchor="w")

mobile_entry = Entry(
    form,
    font=("Segoe UI", 11),
    bd=1,
    relief="solid"
)
mobile_entry.pack(fill="x", pady=4, ipady=4)

Label(
    form,
    text="Initial Deposit / Transaction Amount (₹)",
    font=("Segoe UI", 10, "bold"),
    bg=white,
    fg=blue
).pack(anchor="w")

amount_entry = Entry(
    form,
    font=("Segoe UI", 11),
    bd=1,
    relief="solid"
)
amount_entry.pack(fill="x", pady=4, ipady=4)


# Bank service buttons
def make_button(parent, text, command, color):

    btn = Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=white,
        font=("Segoe UI", 10, "bold"),
        width=22,
        height=1,
        relief="flat",
        cursor="hand2"
    )

    hover(btn, color, "#294B65")

    return btn


create_button = make_button(
    root,
    "CREATE ACCOUNT",
    create_account,
    blue
)
create_button.pack(pady=4)

make_button(
    root,
    "DEPOSIT MONEY",
    deposit,
    green
).pack(pady=4)

make_button(
    root,
    "WITHDRAW MONEY",
    withdraw,
    red
).pack(pady=4)

make_button(
    root,
    "TRANSACTION HISTORY",
    history,
    "#52677A"
).pack(pady=4)

make_button(
    root,
    "ACCOUNT REPORT",
    report,
    "#B78128"
).pack(pady=4)

make_button(
    root,
    "CLEAR FIELDS",
    clear,
    grey
).pack(pady=4)


# Status message
status_label = Label(
    root,
    text="Welcome to Bank",
    font=("Segoe UI", 10, "bold"),
    bg=bg,
    fg=green
)
status_label.pack(pady=8)


# Footer
Label(
    root,
    text="BANK | Banking Management System",
    font=("Segoe UI", 9),
    bg=blue,
    fg=white,
    pady=8
).pack(fill="x", side="bottom")


# Run application
root.mainloop()

