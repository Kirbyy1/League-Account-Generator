import os
import random
import string
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image
from tkextrafont import Font

from account_generator import GenerateAccount

# Define the regions
REGIONS = {
    'EUW': 'EUW1',
    'EUNE': 'EUN1',
    'NA': 'NA1',
    'BR': 'BR1',
    'TR': 'TR1',
    'RU': 'RU',
    'OCE': 'OC1',
    'LAN': 'LA1',
    'LAS': 'LA2',
    'JP': 'JP1',
    'PH': 'PH2',
    'SG': 'SG2',
    'TH': 'TH2',
    'TW': 'TW2',
    'VN': None,
    'PBE': 'PBE1'
}


def generate_accounts_in_thread():
    num_accounts = num_accounts_entry.get()

    if num_accounts.isdigit() and int(num_accounts) > 0:
        thread = threading.Thread(target=generate_account)
        thread.start()
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number of accounts.")


def generate_account():
    num_accounts = num_accounts_entry.get()

    if not num_accounts.isdigit() or int(num_accounts) <= 0:
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number of accounts.")
        return

    num_accounts = int(num_accounts)

    try:
        account_generator = GenerateAccount()
        account_generator.CAPMONSTER_KEY = api_key_entry.get()  # Set the CAPMONSTER_KEY
        for _ in range(num_accounts):
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            username = ''.join(random.choices(string.ascii_lowercase, k=8))
            region = region_combobox.get()
            response = account_generator.generate_account(password, username, region)
            account_treeview.insert('', tk.END, values=(username, password))
        messagebox.showinfo("Accounts Generated", f"{num_accounts} accounts generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def save_accounts():
    items = account_treeview.get_children()
    accounts = []
    for item in items:
        values = account_treeview.item(item, 'values')
        accounts.append(f"{values[0]}:{values[1]}")
    accounts_text = '\n'.join(accounts)

    # Open a file dialog to choose the file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Save the accounts text to the chosen file
        with open(file_path, "w") as file:
            file.write(accounts_text)
        messagebox.showinfo("Accounts Saved", "Accounts saved successfully!")


# This function can get temp path for your resource file
# relative_path is your icon file name
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Create the window
window = tk.Tk()
window.title("Account Generator")
window.geometry("500x800")

# Set the window icon
window.iconbitmap(resource_path("assets/rglogo.ico"))

# Load the image
image_path = resource_path("assets/rglogo.png")
image = Image.open(image_path)

# Resize the image
width, height = 170, 170  # Set the desired width and height
image = image.resize((width, height))
font1 = Font(file='assets/Nexa Bold (1).ttf', family="Nexa")
# Convert the image to Tkinter-compatible format
tk_image = ImageTk.PhotoImage(image)

# Create a label and set the image
image_label = tk.Label(window, image=tk_image)

# Pack the label to display it in the window
image_label.grid(row=0, column=0, padx=160, pady=10, sticky="nsew")

# Create the style for the elements
style = tk.ttk.Style()
style.configure('TEntry', font=('Arial', 14))
style.configure('TLabel', font=('Arial', 14))
style.configure('TCombobox', font=('Arial', 14))

# Create the widgets
num_accounts_label = tk.ttk.Label(window, text="Number of Accounts", borderwidth=0)
num_accounts_entry = tk.Entry(window, width=27, relief=tk.FLAT, bg='#F9F9F9', fg='black',
                              insertbackground='black')

api_key_label = tk.ttk.Label(window, text="CAPMONSTER API Key")
api_key_entry = tk.ttk.Entry(window)

region_label = tk.ttk.Label(window, text="Region")
region_combobox = ttk.Combobox(window, values=list(REGIONS.keys()))

# Configure the style for the generate button

generate_button = tk.Button(window,
                            background="#CC2828",
                            foreground='white',
                            activebackground='#8E1E1E',
                            activeforeground='white',
                            highlightthickness=2,
                            highlightcolor='white',
                            width=23,
                            height=2,

                            text="Generate Accounts",
                            command=generate_accounts_in_thread)

# Create the accounts treeview
account_treeview = ttk.Treeview(window, columns=('Username', 'Password'), show='headings')
account_treeview.heading('Username', text='Username')
account_treeview.heading('Password', text='Password')

save_button = tk.Button(window,
                        background="#CC2828",
                        foreground='white',
                        activebackground='#8E1E1E',
                        activeforeground='white',
                        highlightthickness=2,
                        highlightcolor='white',
                        width=23,
                        height=2,
                        text="Save Accounts",
                        command=save_accounts,
                        )

# Add the widgets to the window
num_accounts_label.grid(row=2, column=0, padx=50, pady=10, sticky="w")
num_accounts_entry.grid(row=2, column=0, padx=90, pady=10, ipady=5, sticky="e")

# api_key_label.pack(pady=10)
# api_key_entry.pack(pady=5)
# region_label.pack(pady=10)
# region_combobox.pack(pady=5)
# generate_button.pack(pady=20)
# account_treeview.pack(pady=10)
# save_button.pack(pady=10)

# Run the event loop
window.mainloop()
