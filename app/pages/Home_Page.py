from tkinter import CENTER, ttk

import customtkinter
import tkinter as tk
from app.dbms.person import countRecognizedPersonsAll, joinPersonInfoAndRecognizedPerson,countTotalPersons

class HomePage:
    def __init__(self, main_frame, *args, **kwargs):
        self.main_frame = main_frame
        self.home_frame = tk.Frame(main_frame, bg="#FFFFFF", width=1600, height=500, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        frameCenter = customtkinter.CTkFrame(master=self.home_frame, width=1600, height=1050, corner_radius=20)
        frameCenter.place(x=0, y=0)

        parent_tab = customtkinter.CTkTabview(frameCenter, width=1540)
        parent_tab.place(x=15, y=10)

        parent_tab.add('Home')
        today_count = countRecognizedPersonsAll('day')
        month_count = countRecognizedPersonsAll('month')
        year_count = countRecognizedPersonsAll('year')
        total_person_count = countTotalPersons()

        frame1 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame1.place(x=200, y=20)

        # +++++++++++++++++++++++++++++++++++Home Tab 1 Frame++++++++++++++++++++++++++++++++++++
        frame1_label2 = customtkinter.CTkLabel(master=frame1, text=f"Total \nCustomers Today \n\n{today_count}")
        frame1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

        frame2 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame2.place(x=510, y=20)
        frame2_label2 = customtkinter.CTkLabel(master=frame2, text=f"Total \nCustomers Today Month\n\n{month_count}")
        frame2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)
        frame3 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame3.place(x=810, y=20)
        frame3_label2 = customtkinter.CTkLabel(master=frame3, text=f"Total \nCustomers Years \n\n{year_count}")
        frame3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)
        frame4 = customtkinter.CTkFrame(master=parent_tab.tab('Home'), width=250, height=150, corner_radius=20)
        frame4.place(x=1120, y=20)
        frame4_label2 = customtkinter.CTkLabel(master=frame4, text=f"Total \nPerson \n\n{total_person_count}")
        frame4_label2.place(relx=0.5, rely=0.5, anchor=CENTER)


        style1 = ttk.Style()
        style1.theme_use("default")
        style1.configure("Treeview",
                         background="#2b2b2b",
                         foreground="white",
                         rowheight=25,
                         fieldbackground="#2b2b2b",
                         bordercolor="#343638",
                         borderwidth=0,
                         font=('Times New Roman', 16))
        style1.map('Treeview', background=[('selected', '#22559b')])

        style1.configure("Treeview.Heading",
                         background="#565b5e",
                         foreground="white",
                         relief="flat",
                         font=('Times New Roman', 17))
        style1.map("Treeview.Heading",
                   background=[('active', '#3484F0')], )
        bookingTable2 = ttk.Treeview(frameCenter)
        bookingTable2['columns'] = (
        'id', 'username', 'age', 'email', 'phone', 'address', 'detections')
        bookingTable2.column('#0', width=0, stretch=0)
        bookingTable2.column('id', width=180, anchor=CENTER)
        bookingTable2.column('username', width=240, anchor=CENTER)
        bookingTable2.column('age', width=150, anchor=CENTER)
        bookingTable2.column('email', width=150, anchor=CENTER)
        bookingTable2.column('phone', width=220, anchor=CENTER)
        bookingTable2.column('address', width=220, anchor=CENTER)
        bookingTable2.column('detections', width=150, anchor=CENTER)


        bookingTable2.heading('#0', text='', anchor=CENTER)
        bookingTable2.heading('id', text="ID", anchor=CENTER)
        bookingTable2.heading('username', text="UserName", anchor=CENTER)
        bookingTable2.heading('age', text="Age", anchor=CENTER)
        bookingTable2.heading('email', text="Email", anchor=CENTER)
        bookingTable2.heading('phone', text="Phone", anchor=CENTER)
        bookingTable2.heading('address', text="Address", anchor=CENTER)
        bookingTable2.heading('detections', text="Detections", anchor=CENTER)

        data_results = joinPersonInfoAndRecognizedPerson()
        for row in data_results:
            bookingTable2.insert('', 'end', values=row)

        bookingTable2.place(x=100, y=360)
    def pack(self, **kwargs):
        self.home_frame.pack(**kwargs)



def home_page(main_frame):
    return HomePage(main_frame)

