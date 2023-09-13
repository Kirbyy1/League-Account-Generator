import os
import random
import string
import sys
import threading
import tkinter as tk
from ctypes import windll

import customtkinter
from CTkMessagebox import CTkMessagebox
from PIL import ImageTk, Image

from account_generator import GenerateAccount


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Setting application variables:
        self.window_title = 'Riot Generator v1.0'  # Change here title of your app

        self.put_icon = True

        self.maximized = False

        # Creating fonts:
        self.small_calibri_font = customtkinter.CTkFont(family='Calibri', size=15)
        self.small_helvetica_font = customtkinter.CTkFont(family='Helvetica', size=12)

        self.button_font = customtkinter.CTkFont(family='Helvetica', size=25)

        self.bottom_font_bold = customtkinter.CTkFont(family='Helvetica', weight='bold', size=14)
        self.bottom_font_thin = customtkinter.CTkFont(family='Helvetica', size=12)

        # Configuring window:
        self.geometry(f"{572}x{849}")
        self.resizable(False, False)
        self.title(self.window_title)
        self.overrideredirect(True)
        self.attributes('-topmost', True, '-alpha', 0.998)

        # Creating title bar:
        self.title_bar_color = '#141414'
        self.text_color = 'white'
        self.hover_button_color = '#7c7d7c'
        self.hover_close_button_color = '#ff4d4d'

        self.w_width = self.winfo_width()
        self.title_bar = customtkinter.CTkFrame(self, fg_color=self.title_bar_color, width=self.w_width, height=28,
                                                corner_radius=0)
        self.title_bar.grid_propagate(False)
        self.title_bar.grid(row=0, column=0, sticky='w')
        self.title_bar.columnconfigure(0, weight=1)

        self.s_width = self.winfo_screenwidth()
        self.s_height = self.winfo_screenheight()
        self.title_bar_height = self.title_bar.winfo_height()
        self.main_frame_maximized_height = self.s_height - self.title_bar_height

        def minimize(hide=False):
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.user32.ShowWindow(hwnd, 0 if hide else 6)

        # Creating buttons, label and icon on title bar:
        self.minimize_button = customtkinter.CTkButton(self.title_bar, text='  🗕  ', command=minimize,
                                                       font=self.small_calibri_font, height=28, width=45,
                                                       corner_radius=0, fg_color=self.title_bar_color,
                                                       hover_color=self.hover_button_color, text_color=self.text_color)
        self.minimize_button.grid(row=0, column=1, sticky='w')

        self.close_button = customtkinter.CTkButton(self.title_bar, text='  🗙  ', command=self.destroy,
                                                    font=self.small_calibri_font, height=28, width=46, corner_radius=0,
                                                    fg_color=self.title_bar_color,
                                                    hover_color=self.hover_close_button_color,
                                                    text_color=self.text_color)
        self.close_button.grid(row=0, column=3, sticky='e')

        self.title_bar_title = customtkinter.CTkLabel(self.title_bar, text=self.window_title,
                                                      fg_color=self.title_bar_color, font=self.small_helvetica_font)
        self.title_bar_title.grid(row=0, column=0, sticky='w', padx=5)

        if self.put_icon == True:
            self.app_icon = customtkinter.CTkImage(dark_image=Image.open(resource_path("assets/rglogo.ico")),
                                                   size=(17, 17))
            self.title_bar_title.configure(image=self.app_icon, compound='left', text=(f' {self.window_title}'))

        self.main_frame = tk.Frame(self, bg="#141414", width=572, height=849)
        self.main_frame.place(x=0, y=28)

        # Open the image
        image = Image.open(resource_path("assets/rglogo.png"))
        # Resize the image
        new_width = 212
        new_height = 212
        resized_image = image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(resized_image)

        # Create a label widget and place it at the desired position
        image_label = customtkinter.CTkLabel(self, image=photo_image, text="", bg_color='#141414')
        image_label.place(x=180, y=62)

        # Creating main frame and your main app:
        self.information_frame = tk.Frame(self, bg="#1B1B1B", width=475, height=130)
        self.information_frame.place(x=48, y=319)

        # Number of accounts

        image_label = customtkinter.CTkLabel(self,
                                             image=ImageTk.PhotoImage(
                                                 Image.open(resource_path("assets/user3.png")).resize((28, 28))),
                                             text="", bg_color='#1B1B1B')
        image_label.place(x=59, y=329)

        customtkinter.CTkLabel(self, text='Number of account', font=self.small_helvetica_font, bg_color="#1B1B1B",
                               text_color='#7F7F7F').place(
            x=95, y=331)

        self.nof_entry = customtkinter.CTkEntry(self, bg_color='#1B1B1B', height=22, width=233, corner_radius=8)
        self.nof_entry.place(x=227, y=332)

        # CapMonster Key
        customtkinter.CTkLabel(self,
                               image=ImageTk.PhotoImage(Image.open(resource_path("assets/key1.png")).resize((28, 28))),
                               text="", bg_color='#1B1B1B').place(x=54, y=372)

        customtkinter.CTkLabel(self, text='CapMonster Key', bg_color="#1B1B1B", text_color='#7F7F7F').place(
            x=95, y=375)

        self.CapMonster = customtkinter.CTkEntry(self, bg_color='#1B1B1B', height=22, width=233, corner_radius=8)
        self.CapMonster.place(x=227, y=377)

        # Region

        customtkinter.CTkLabel(self,
                               image=ImageTk.PhotoImage(
                                   Image.open(resource_path("assets/countries.png")).resize((28, 28))),
                               text="", bg_color='#1B1B1B').place(x=56, y=419)

        customtkinter.CTkLabel(self, text='Region', bg_color="#1B1B1B", text_color='#7F7F7F').place(
            x=95, y=417)

        combobox_var = customtkinter.StringVar(value="EUW")
        self.Region = customtkinter.CTkComboBox(master=self,
                                                values=["EUW", "EUNE", 'NA', 'BR', 'TR', 'RU', 'OCE', 'LAN', 'LAS',
                                                        'JP',
                                                        'PH', 'SG', 'TH', 'TW', 'PBE'],
                                                variable=combobox_var)
        self.Region.place(x=227, y=415)

        self.create_button = customtkinter.CTkButton(self, text='Create', width=221, height=66, text_color='#E2E2E2',
                                                     fg_color='#CC2828', font=self.button_font, hover_color='#dd5555',
                                                     command=self.generate_accounts_in_thread)
        self.create_button.place(x=175, y=565)

        # Creating bottom frame frame
        self.bottom_frame = tk.Frame(self, bg="#101010", width=583, height=177)
        self.bottom_frame.place(x=0, y=672)

        # ------------------------------------------------
        # Open the image
        image = Image.open(resource_path("assets/rglogo.png"))
        # Resize the image
        new_width = 80
        new_height = 80
        resized_image = image.resize((new_width, new_height))

        # Convert the resized image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(resized_image)

        # Create a label widget and place it at the desired position
        customtkinter.CTkLabel(self, image=photo_image, text="", bg_color='#101010').place(x=19, y=717)

        # support and privacy
        customtkinter.CTkLabel(self, text='Support and Privacy', font=self.bottom_font_bold, text_color='#282727',
                               bg_color='#101010').place(x=149, y=694)

        # Help Center
        customtkinter.CTkLabel(self, text='Help Center', font=self.bottom_font_thin, text_color='#282727',
                               bg_color='#101010').place(x=149, y=716)

        # TOS
        customtkinter.CTkLabel(self, text='Terms of Use', font=self.bottom_font_thin, text_color='#282727',
                               bg_color='#101010').place(x=149, y=738)

        # Privacy Policy
        customtkinter.CTkLabel(self, text='Privacy Policy', font=self.bottom_font_thin, text_color='#282727',
                               bg_color='#101010').place(x=149, y=760)

        # ------------------------------------------------
        # Social
        customtkinter.CTkLabel(self, text='Social', font=self.bottom_font_bold, text_color='#282727',
                               bg_color='#101010').place(x=354, y=694)

        # Discord
        customtkinter.CTkLabel(self, text='Discord', font=self.bottom_font_thin, text_color='#282727',
                               bg_color='#101010').place(x=354, y=720)

        # Youtube
        customtkinter.CTkLabel(self, text='Youtube', font=self.bottom_font_thin, text_color='#282727',
                               bg_color='#101010').place(x=354, y=741)

        # ------------------------------------------------

        # ――――――――――

        def get_pos(event):
            xwin = self.winfo_x()
            ywin = self.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event):
                self.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

            def release_window(event):
                self.config(cursor="arrow")

            self.title_bar.bind('<B1-Motion>', move_window)
            self.title_bar.bind('<ButtonRelease-1>', release_window)
            self.title_bar_title.bind('<B1-Motion>', move_window)
            self.title_bar_title.bind('<ButtonRelease-1>', release_window)

        self.title_bar.bind('<Button-1>', get_pos)
        self.title_bar_title.bind('<Button-1>', get_pos)

        def set_appwindow(mainWindow):
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080

            hwnd = windll.user32.GetParent(mainWindow.winfo_id())
            stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            stylew = stylew & ~WS_EX_TOOLWINDOW
            stylew = stylew | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

            mainWindow.wm_withdraw()
            mainWindow.after(10, lambda: mainWindow.wm_deiconify())

        set_appwindow(self)

    def generate_account(self):
        num_accounts = self.nof_entry.get()

        accounts = []
        if not num_accounts.isdigit() or int(num_accounts) <= 0:
            CTkMessagebox(title="Invalid Input",
                          message="Please enter a valid positive integer for the number of accounts.", icon="cancel")

            return

        num_accounts = int(num_accounts)

        try:
            account_generator = GenerateAccount()
            account_generator.CAPMONSTER_KEY = self.CapMonster.get()  # Set the CAPMONSTER_KEY

            for _ in range(num_accounts):
                self.create_button.configure(text=f'Generating ({_} / {num_accounts})', state='disabled')
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                username = ''.join(random.choices(string.ascii_lowercase, k=8))
                Region = self.Region.get()
                response = account_generator.generate_account(password, username, Region)

                accounts.append(f"Username: {username}, Password: {password}, Region: {Region}")

            # Save the accounts to a text file
            file_name = f"{num_accounts}x{Region} {random.randint(1000, 12345)}.txt"
            with open(file_name, "w") as file:
                file.write("\n".join(accounts))

            CTkMessagebox(title="Accounts Saved", message=f"Accounts saved to {file_name}", icon="info")

            self.create_button.configure(text=f'Create', state='normal')
        except Exception as e:

            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}", icon="cancel")

    def generate_accounts_in_thread(self):
        num_accounts = self.nof_entry.get()

        if num_accounts.isdigit() and int(num_accounts) > 0:
            thread = threading.Thread(target=self.generate_account)
            thread.start()

        else:

            CTkMessagebox(title="Invalid Input",
                          message="Please enter a valid positive integer for the number of accounts.", icon="cancel",
                          bg_color='#141414', fg_color='#1D1D1D')


if __name__ == "__main__":
    app = App()
    app.mainloop()
