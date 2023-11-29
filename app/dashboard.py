import tkinter as tk
from tkinter import TOP, BOTH
from tkinter import *
import customtkinter
from PIL import ImageTk, Image
from datetime import time, date
import math
from app.libs import Global
import time
from time import strftime

from pages.Home_Page import home_page
from pages.addperson import addperson
from pages.intrusion_warning_page import intrusion_warning_page
from pages.camerapage import camera_page
from pages.account_page import account_page

class Admin_Dashboard(customtkinter.CTk):
    def __init__(self, master):
        self.master = master

        # getting screen width and height of display
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        # setting tkinter window size
        master.geometry("%dx%d" % (width, height))
        master.title("Security Management System dashboard")

        # Add the following line to initialize self.main_frame
        self.main_frame = tk.Frame(master, highlightbackground='black', highlightthickness=2)

        self.create_widgets()

    def create_widgets(self):
        admin_info = Global.currentAdmin
        print("Admin Info:", admin_info)  # Add this line to print the admin info

        username = admin_info.get('username', '')


        north_frame = customtkinter.CTkFrame(master=self.master, height=80, corner_radius=0)
        north_frame.pack(side=TOP)
        north_frame.pack_propagate(False)
        north_frame.configure(width=1880, height=80)
        # +++++++++++++++++++++++++++++++++++Welcome Label++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        welcomelabel_text = "Welcome {}".format(username)
        welcomelabel = customtkinter.CTkLabel(master=north_frame, text=welcomelabel_text, font=('Bold', 30))
        welcomelabel.place(x=1500, y=10)
        welcomelabel.pack()

        title_lb = customtkinter.CTkLabel(master=north_frame, text=" Admin Dashboard", font=('Bold', 30))
        title_lb.place(x=0, y=10)
        # Move the options_frame packing here
        self.options_frame = tk.Frame(self.master, bg="#FFFFFF")

        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=200, height=1200)

        self.home_btn = self.create_button("Home", self.home_button_click, 300)
        self.add_person_btn = self.create_button("Add Person", self.add_person_button_click, 400)
        self.intrusion_warning_btn = self.create_button("Intrusion Warning", self.intrusion_warning_button_click, 500)
        self.camera_btn = self.create_button("Camera Live", self.camera_button_click, 600)



        self.create_indicator_frames()


        self.main_frame = tk.Frame(self.master, highlightbackground='black', highlightthickness=2)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=1600, height=1366)


        user_image = ImageTk.PhotoImage(Image.open(
            "/Users/lvc/PycharmProjects/pythonProject4/app/images/admin_img.png"))
        user_image_label = Label( self.options_frame , image=user_image, bg="#FFFFFF")
        user_image_label.image = user_image
        user_image_label.place(x=60, y=40)

        def my_time():
            time_string = strftime('%I:%M:%S %p')  # time format
            l1.configure(text=time_string,fg_color='#2b2b2b')
            l1.after(1000, my_time)

            # time delay of 1000 milliseconds

        l1 = customtkinter.CTkLabel(master=self.options_frame, font=('Bold', 30))


        l1.place(x=20, y=150)
        my_time()

        self.home_frame = home_page(self.main_frame)
        self.add_person_frame = addperson(self.main_frame)
        self.intrusion_warning_frame = intrusion_warning_page(self.main_frame)
        self.camera_frame = camera_page(self.main_frame)


    def create_button(self, text, command, y_position):
        btn = tk.Button(self.options_frame, text=text, fg="#158aff", bd=0, font=('Bold', 15),
                        command=command, relief="flat", highlightthickness=0, borderwidth=0, bg="#FFFFFF")
        btn.place(x=60, y=y_position, width=150, height=50)
        return btn

    def create_indicator_frames(self):
        self.home_indicate = tk.Frame(self.options_frame, bg="#FFFFFF")
        self.home_indicate.place(x=0, y=300, width=60, height=50)

        self.add_person_indicate = tk.Frame(self.options_frame, bg="#FFFFFF")
        self.add_person_indicate.place(x=0, y=400, width=60, height=50)

        self.intrusion_warning_indicate = tk.Frame(self.options_frame, bg="#FFFFFF")
        self.intrusion_warning_indicate.place(x=0, y=500, width=60, height=50)

        self.camera_indicate = tk.Frame(self.options_frame, bg="#FFFFFF")
        self.camera_indicate.place(x=0, y=600, width=60, height=50)





    def home_button_click(self):
        self.indicate(self.home_indicate, self.home_frame)


    def add_person_button_click(self):
        self.indicate(self.add_person_indicate, self.add_person_frame)

    def intrusion_warning_button_click(self):
        self.indicate(self.intrusion_warning_indicate, self.intrusion_warning_frame)

    def camera_button_click(self):
        self.indicate(self.camera_indicate, self.camera_frame)



    def hide_indicator(self):
        indicators = [self.home_indicate, self.add_person_indicate,
                      self.intrusion_warning_indicate, self.camera_indicate
                     ]

        for indicator in indicators:
            indicator.config(bg="#FFFFFF")

    def indicate(self, lb, page_frame):
        for child in self.main_frame.winfo_children():
            child.pack_forget()

        # Set the background color for all indicators
        indicators = [self.home_indicate, self.add_person_indicate,
                      self.intrusion_warning_indicate, self.camera_indicate]

        for indicator in indicators:
            indicator.config(bg="#FFFFFF")

        lb.config(bg="#158aff")
        page_frame.pack(pady=20)

if __name__=='__main__':
    main=customtkinter.CTk()
    Admin_Dashboard(main)
    main.mainloop()