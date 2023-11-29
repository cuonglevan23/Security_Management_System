import tkinter as tk
import customtkinter
from dbms.login_management import AdminInfo, adminLogin,createAdmin
from dashboard import Admin_Dashboard
from app.libs import Global

root = tk.Tk()
root.geometry("500x700")
root.title("Security Management System")
root.configure(bg="white")

login_admin_icon = tk.PhotoImage(file="/Users/lvc/PycharmProjects/pythonProject4/app/images/admin_img.png")
add_user_icon = tk.PhotoImage(file="/Users/lvc/PycharmProjects/pythonProject4/app/images/add_student_img.png")

bg_color = "#273b7a"




def welcome_page():
    def foward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def create_account():
        welcome_page_fm.destroy()
        root.update()
        create_account_page()
    welcome_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3, bg="white", border=0)

    heading_lb = tk.Label(welcome_page_fm, text="Welcome to Security Management System", bg=bg_color, fg="white",
                          font=("Bold", 18))
    heading_lb.place(x=0, y=0, width=400)

    login_btn = tk.Button(welcome_page_fm, text="Login Admin", bg=bg_color, fg="black", font=('Bold', 15), bd=0,
                          borderwidth=0, highlightthickness=0, command=foward_to_admin_login_page)
    login_btn.place(x=120, y=125, width=200, height=50)

    login_icon = tk.Button(welcome_page_fm, image=login_admin_icon, bg=bg_color, bd=0, borderwidth=0,
                           highlightthickness=0, command=foward_to_admin_login_page)
    login_icon.place(x=30, y=100)

    create_user_btn = tk.Button(welcome_page_fm, text="Create Account", bg=bg_color, fg="black", font=('Bold', 15),
                                bd=0, borderwidth=0, highlightthickness=0, command=create_account)
    create_user_btn.place(x=120, y=225, width=200, height=50)

    create_user_icon = tk.Button(welcome_page_fm, image=add_user_icon, bg=bg_color, bd=0, borderwidth=0,
                                 highlightthickness=0, command=create_account)
    create_user_icon.place(x=30, y=200)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)

def open_dashboard_window():
    dashboard_window = tk.Toplevel(root)
    dashboard_window.protocol("WM_DELETE_WINDOW", root.destroy)


    root.iconify()

    # Close the root window when the Admin_Dashboard window is closed

    admin_dashboard = Admin_Dashboard(dashboard_window)
    dashboard_window.mainloop()

def admin_login_page():
    def login_clicked():
        username = userName_ent.get()
        password = password_ent.get()

        # Call the adminLogin function with the entered credentials
        admin_info = AdminInfo(username, password)
        login_result = adminLogin(admin_info)

        if login_result:
            print("Login successful. Admin details:", login_result)
            Global.currentAdmin = {
                'id': login_result[0],  # Replace with the correct index for the 'id' column
                'username': login_result[1],  # Replace with the correct index for the 'username' column
                'password': login_result[2],
                'phone': login_result[3],  # Replace with the correct index for the 'phone' column
                'address': login_result[4],  # Replace with the correct index for the 'address' column
                'email': login_result[5],

            }
            open_dashboard_window()
            # Add code to navigate to the next page or perform other actions after successful login
        else:
            print("Login failed. Invalid username or password.")
    def toggle_password():
        current_state = password_ent.cget("show")
        if current_state == "":
            password_ent.config(show="*")  # Ẩn mật khẩu
        else:
            password_ent.config(show="")

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()
    admin_login_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3, bg="white")

    heading_lb = tk.Label(admin_login_page_fm, text="Admin Login", bg=bg_color, fg="white",
                          font=("Bold", 18))
    heading_lb.place(x=0, y=0, width=400)
    back_btn = tk.Button(admin_login_page_fm, text="⬅️", bg='white', fg="black", font=('Bold', 25), bd=0,
                         borderwidth=0, highlightthickness=0, command=forward_to_welcome_page)
    back_btn.place(x=5, y=40, width=50, height=50)
    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon, bg=bg_color)
    admin_icon_lb.place(x=150, y=50)

    userName_lb = tk.Label(admin_login_page_fm, text="Enter User Name:", bg="white", fg="black", font=("Bold", 15))
    userName_lb.place(x=80, y=140)
    userName_ent = tk.Entry(admin_login_page_fm, bg='white', font=("Bold", 15), justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, fg='black')
    userName_ent.place(x=80, y=190, width=250, height=35)

    userPassword_lb = tk.Label(admin_login_page_fm, text="Enter Password:", bg="white", fg="black", font=("Bold", 15))
    userPassword_lb.place(x=80, y=240)

    password_ent = tk.Entry(admin_login_page_fm, bg='white', font=("Bold", 15), show="*", justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, fg='black')
    password_ent.place(x=80, y=290, width=250, height=35)

    show_password_var = tk.BooleanVar()
    show_password_cb = tk.Checkbutton(admin_login_page_fm, text="Show Password", bg='white', fg="black",
                                      font=('Bold', 12), variable=show_password_var, command=toggle_password)
    show_password_cb.place(x=80, y=330, width=120, height=30)

    login_btn = tk.Button(admin_login_page_fm, text="Login", bg=bg_color, font=('Bold', 15),
                          highlightbackground=bg_color, command=login_clicked)
    login_btn.place(x=80, y=400, width=250, height=40)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height=520)


def create_account_page():
    def toggle_password():
        current_state = password_ent.cget("show")
        if current_state == "":
            password_ent.config(show="*")
            Repassword_ent.config(show="*")
        else:
            password_ent.config(show="")
            Repassword_ent.config(show="")

    def forward_to_welcome_page():
        create_account_page_fm.destroy()
        root.update()
        welcome_page()

    def create_new_admin():
        # Retrieve user input
        username = userName_ent.get()
        password = password_ent.get()
        re_password = Repassword_ent.get()

        # Validate password match
        if password != re_password:
            # Display an error message or handle the mismatch
            print("Passwords do not match")
            return

        # Use your createAdmin function to add the new admin to the database
        # Assuming createAdmin takes appropriate parameters
        # Replace the placeholder values with the actual values from user input
        createAdmin(username, password)

        # You can add further logic or feedback messages based on the success or failure of admin creation

    create_account_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3, bg="white")

    heading_lb = tk.Label(create_account_page_fm, text="Create Account", bg=bg_color, fg="white", font=("Bold", 18))
    heading_lb.place(x=0, y=0, width=400)

    back_btn = tk.Button(create_account_page_fm, text="⬅️", bg='white', fg="black", font=('Bold', 25), bd=0,
                         borderwidth=0, highlightthickness=0, command=forward_to_welcome_page)
    back_btn.place(x=5, y=40, width=50, height=50)

    admin_icon_lb = tk.Label(create_account_page_fm, image=login_admin_icon, bg=bg_color)
    admin_icon_lb.place(x=150, y=50)

    userName_lb = tk.Label(create_account_page_fm, text="Enter User Name:", bg="white", fg="black", font=("Bold", 15))
    userName_lb.place(x=80, y=140)

    userName_ent = tk.Entry(create_account_page_fm, bg='white', font=("Bold", 15), justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, fg='black')
    userName_ent.place(x=80, y=190, width=250, height=35)

    userPassword_lb = tk.Label(create_account_page_fm, text="Enter Password:", bg="white", fg="black",
                               font=("Bold", 15))
    userPassword_lb.place(x=80, y=240)

    password_ent = tk.Entry(create_account_page_fm, bg='white', font=("Bold", 15), show="*", justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, fg='black')
    password_ent.place(x=80, y=290, width=250, height=35)

    RePassword_lb = tk.Label(create_account_page_fm, text="Enter RePassword:", bg="white", fg="black",
                             font=("Bold", 15))
    RePassword_lb.place(x=80, y=340)

    Repassword_ent = tk.Entry(create_account_page_fm, bg='white', font=("Bold", 15), show="*", justify=tk.CENTER,
                              highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, fg='black')
    Repassword_ent.place(x=80, y=390, width=250, height=35)

    show_password_var = tk.BooleanVar()
    show_password_cb = tk.Checkbutton(create_account_page_fm, text="Show Password", bg='white', fg="black",
                                      font=('Bold', 12), variable=show_password_var, command=toggle_password)
    show_password_cb.place(x=80, y=430, width=120, height=30)

    create_btn = tk.Button(create_account_page_fm, text="Create Account", bg=bg_color, font=('Bold', 15),
                           command=create_new_admin, highlightbackground=bg_color)
    create_btn.place(x=80, y=500, width=250, height=40)

    create_account_page_fm.pack(pady=30)
    create_account_page_fm.pack_propagate(False)
    create_account_page_fm.configure(width=400, height=820)




welcome_page()
root.mainloop()
