# pages/account_page.py
import tkinter as tk
from app.libs import Global  # Import the Global module
import customtkinter

class AccountPage(tk.Frame):
    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(main_frame, bg="#FFFFFF", width=1200, height=500, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=1200, height=880, bg="white")
        admin_info = Global.currentAdmin

        id = admin_info.get('id', '')
        username = admin_info.get('username', '')
        password = admin_info.get('password', '')
        phone = admin_info.get('phone', '')
        address = admin_info.get('address', '')
        email = admin_info.get('email', '')

        username_lb = tk.Label(self, text='Tên đăng nhập:', font=('Bold', 28))
        username_lb.place(x=100, y=50)
        username_entry = tk.Entry(self, font=('Bold', 28))
        username_entry.insert(0, username)
        username_entry.place(x=100, y=100, width=350, height=50)

        password_lb = tk.Label(self, text='Mật khẩu:', font=('Bold', 28))
        password_lb.place(x=600, y=50)
        password_entry = tk.Entry(self, font=('Bold', 28))
        password_entry.insert(0, password)
        password_entry.place(x=600, y=100, width=350, height=50)

        phone_lb = tk.Label(self, text='Số điện thoại:', font=('Bold', 28))
        phone_lb.place(x=100, y=150)
        phone_entry = tk.Entry(self, font=('Bold', 28))
        phone_entry.insert(0, phone)
        phone_entry.place(x=100, y=200, width=350, height=50)

        address_lb = tk.Label(self, text='Địa chỉ:', font=('Bold', 28))
        address_lb.place(x=600, y=150)
        address_entry = tk.Entry(self, font=('Bold', 28))
        address_entry.insert(0, address)
        address_entry.place(x=600, y=200, width=350, height=50)

        email_lb = tk.Label(self, text='Email:', font=('Bold', 28))
        email_lb.place(x=100, y=250)
        email_entry = tk.Entry(self, font=('Bold', 28))
        email_entry.insert(0, email)
        email_entry.place(x=100, y=300, width=350, height=50)

        id_lb = tk.Label(self, text='ID:', font=('Bold', 28))
        id_lb.place(x=600, y=250)
        id_entry = tk.Entry(self, font=('Bold', 28))
        id_entry.insert(0, id)
        id_entry.place(x=600, y=300, width=350, height=50)

        # Print the widget hierarchy to help diagnose the issue
        print("Widget Hierarchy:", self.winfo_parent(), self.winfo_name(), address_entry.winfo_parent(),
              address_entry.winfo_name())

        self.canvas.pack()
        self.canvas.bind("<Button-1>")
        self.bind_all("<Key>")


def account_page(main_frame):
    return AccountPage(main_frame)
