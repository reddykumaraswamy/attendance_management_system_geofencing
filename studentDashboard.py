from tkinter import *
import tkinter as tk
from tkinter import ttk
from random import choice
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import font
from datetime import *
import time
import json
from tkcalendar import *
from time import strftime
import webbrowser
import subprocess
import loginPage
import pyrebase
from firebase_admin import db


# firebaseConfig = {
#   'apiKey': "AIzaSyDqPoqD2wCzIX1PZ9WIFqn8Wn1-bBxbyx0",
#   'authDomain': "tkinter-attendancesystem.firebaseapp.com",
#   'databaseURL': "https://tkinter-attendancesystem-default-rtdb.firebaseio.com",
#   'projectId': "tkinter-attendancesystem",
#   'storageBucket': "tkinter-attendancesystem.appspot.com",
#   'messagingSenderId': "958719958339",
#   'appId': "1:958719958339:web:fcf81f7252df3cc8b1a3f6",
#   'measurementId': "G-EYK3PMMX1X"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
#
# storage = firebase.storage()

def run_python_script():
    script_path = r"C:\Users\reddy\PycharmProjects\Face_Recognition_Based_Attendance_System\main.py"
    subprocess.run(["python", script_path])


def add_face_script():
    script_path = r"C:\Users\reddy\PycharmProjects\Face_Recognition_Based_Attendance_System\add_faces.py"
    subprocess.run(["python", script_path])


class Dashboard:

    def __init__(self):
        self.root = Toplevel()
        self.root.title("Amity IntelliAMS | Student Dashboard")
        # self.root.geometry("1199x600+100+50")
        # self.root.state('zoomed')
        self.root.geometry("1720x800")
        self.root.resizable(1, 1)
        self.root.config(background='#F0F0FF')

        # =================== icon =============== #
        img1 = PhotoImage(file="images/icon.png")
        self.root.iconphoto(False, img1)

        # =================== getting unique student ID =============== #
        with open("data/data.json") as file:
            self.uniqueStudentID = json.load(file)

        # self.studentDetails = db.child('students/'+self.uniqueStudentID['uniqueStudentID']).get()
        ref = db.reference('students')

        # Get the student's data from the database
        self.student_data = ref.child(self.uniqueStudentID['uniqueStudentID']).get()
        # print(self.student_data)

        # ====================== Header frame ==================#
        self.header = Frame(self.root, bg="#3A6B35")
        self.header.place(relx=1.0, y=0, anchor="ne", relwidth=0.85, relheight=0.08)

        # ===================== dashboard heading ======== #
        self.dash_image = Image.open("images/dash.webp")
        self.dash_image = self.dash_image.resize((50, 50))
        img_dash = ImageTk.PhotoImage(self.dash_image)
        self.dash = Label(self.root, image=img_dash, cursor="hand2", bd=0, bg="#3A6B35")
        self.dash.image = img_dash
        self.dash.place(x=320, y=10)

        self.heading = Label(self.root, text="Student Dashboard", font=("Eras Bold ITC", 28), cursor="hand2",
                             fg="#EEEEDF", bg="#3A6B35")
        self.heading.place(x=380, y=8)

        # ================== face registration button ================ #
        self.face_register = Button(self.header, text="Register your Face", fg="red", bg="#E3B448", font=("Eras Bold ITC", 20, "underline"), bd=0,
                                  cursor="hand2", command=add_face_script, activebackground="grey")
        self.face_register.place(x=720, y=12, height=40, width=300)

        # ====================== logout ================ #
        self.lout_image = Image.open("images/logout.png")
        self.lout_image = self.lout_image.resize((35, 35))
        img_lout = ImageTk.PhotoImage(self.lout_image)
        self.lout = Label(self.header, image = img_lout, bd = 0, bg = "#EEEEDF")
        self.lout.image = img_lout
        self.lout.place(x=1225, y=12, height=40, width=50)

        self.logout_text = Button(self.header, text="Logout", fg="black", bg="#EEEEDF", font=("Arial Black", 18), bd=0,
                                  cursor="hand2", command=self.logout_function, activebackground="grey")
        self.logout_text.place(x=1112, y=12, height=40, width=120)


        # ============== left side bar ================== #

        self.sidebar = Frame(self.root, bg="#E3B448")
        self.sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

        self.topRightBox = Frame(self.sidebar, bg="#EEEEDF")
        self.topRightBox.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.15)

        # ================ time and date =============== #
        self.time_image = Image.open("images/clock.png")
        self.time_image = self.time_image.resize((60, 60))
        img_time = ImageTk.PhotoImage(self.time_image)
        self.time = Label(self.sidebar, image=img_time, bd=0, bg="#EEEEDF")
        self.time.image = img_time
        self.time.place(x=20, y=50)

        # ===================== retrieving profile image ============= #
        # self.imageBlob = storage.child('student_image/'+self.uniqueStudentID['uniqueStudentID']+'.jpg').download()
        # print(self.imageBlob)

        # ===================== profile image ============= #
        self.image1 = Image.open("images/student.png")
        self.image1 = self.image1.resize((130, 130))
        pic = ImageTk.PhotoImage(self.image1)
        self.logo = Label(self.sidebar, image=pic, bg="#E3B448")
        self.logo.image = pic
        self.logo.place(x=90, y=180)

        # =============== profile name ================= #
        self.name = Label(self.sidebar, text=self.student_data['fullname'], bg="#E3B448", font=("Arial Black", 17))
        self.name.place(relx=0, rely=0.36, relwidth=1, relheight=0.05)

        self.edit_pic = Label(self.sidebar, text="Edit photo", cursor='hand2', bg="#E3B448",
                              font=("Bookman Old Style", 11, 'underline'), fg="blue")
        self.edit_pic.place(relx=0, rely=0.41, relwidth=1, relheight=0.02)


        # ========== my profile button ========== #
        self.home_image = Image.open("images\home.png")
        self.home_image = self.home_image.resize((30, 30))
        img_h = ImageTk.PhotoImage(self.home_image)
        self.home = Label(self.sidebar, text="My Profile", font=("Arial Black", 16), cursor="hand2", bd=0, fg="#EEEEDF",
                          bg="#3A6B35")
        self.home.image = img_h
        self.home.place(relx=0, rely=0.48, relwidth=1, relheight=0.06)

        # self.home_text = Button(self.sidebar, text = "Home", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.home_text.place(x = 115, y = 320)

        # ========== time table button ============ #
        self.tt_image = Image.open("images\manage-icon.png")
        self.tt_image = self.tt_image.resize((25, 30))
        img_tt = ImageTk.PhotoImage(self.tt_image)
        self.tt = Label(self.sidebar, text="Time Table", font=("Arial Black", 16), cursor="hand2", bd=0, fg="#EEEEDF",
                        bg="#3A6B35")
        # self.tt = Label(self.sidebar, image = img_tt, bd=0, bg="#3A6B35")
        self.tt.image = img_tt
        self.tt.place(relx=0, rely=0.56, relwidth=1, relheight=0.06)

        # self.timetable_text = Button(self.sidebar, text = "Time-Table", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.timetable_text.place(x = 115, y = 380)

        # ============== faculty button ============== #
        self.fac_image = Image.open("images\staf.png")
        self.fac_image = self.fac_image.resize((27, 27))
        img_fac = ImageTk.PhotoImage(self.fac_image)
        self.fac = Label(self.sidebar, text="Faculty", font=("Arial Black", 16), cursor="hand2", bd=0, fg="#EEEEDF",
                         bg="#3A6B35")
        # self.fac = Label(self.sidebar, image = img_fac, bd=0, bg="#3A6B35")
        self.fac.image = img_fac
        self.fac.place(relx=0, rely=0.64, relwidth=1, relheight=0.06)

        # self.faculty_text = Button(self.sidebar, text = "Faculty", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.faculty_text.place(x = 115, y = 440)

        # ============== my attendance button ============== #
        self.note_image = Image.open("images\msg.png")
        self.note_image = self.note_image.resize((27, 27))
        img_note = ImageTk.PhotoImage(self.note_image)
        self.note = Label(self.sidebar, text="My Attendance", font=("Arial Black", 16), cursor="hand2", bd=0,
                          fg="#EEEEDF", bg="#3A6B35")
        # self.note = Label(self.sidebar, image = img_note, bd=0, bg="#3A6B35")
        self.note.image = img_note
        self.note.place(relx=0, rely=0.72, relwidth=1, relheight=0.06)

        # self.note_text = Button(self.sidebar, text = "Notifications", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.note_text.place(x = 115, y = 500)

        # ==================== notifications button ============== #
        self.atto_image = Image.open("images\came.png")
        self.atto_image = self.atto_image.resize((27, 27))
        img_atto = ImageTk.PhotoImage(self.atto_image)
        self.atto = Label(self.sidebar, text="Notifications", font=("Arial Black", 16), cursor="hand2", bd=0,
                          fg="#EEEEDF", bg="#3A6B35")
        # self.atto = Label(self.sidebar, image = img_atto, bd=0, bg="#3A6B35")
        self.atto.image = img_atto
        self.atto.place(relx=0, rely=0.80, relwidth=1, relheight=0.06)

        # self.attendance_text = Button(self.sidebar, text = "My Attendance", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.attendance_text.place(x = 115, y = 560)

        # ================= settings button =========== #
        self.reach_image = Image.open("images\out.png")
        self.reach_image = self.reach_image.resize((27, 27))
        img_r = ImageTk.PhotoImage(self.reach_image)
        self.reach = Label(self.sidebar, text="Settings", font=("Arial Black", 16), cursor="hand2", bd=0, fg="#EEEEDF",
                           bg="#3A6B35")
        self.reach.image = img_r
        self.reach.place(relx=0, rely=0.88, relwidth=1, relheight=0.06)

        # self.reach_text = Button(self.sidebar, text = "Reach out", bg = "#ffffff", font = ("times new roman", 13, "bold"), bd = 0, cursor = "hand2", activebackground= "grey")
        # self.reach_text.place(x = 115, y = 620)

        # ================= body frame 1 =============== #

        self.bodyframe1 = Frame(self.root, bg = "#C8FFD4")
        self.bodyframe1.place(x = 330, y = 110, width = 250, height = 230)

        self.frame1_text = Label(self.bodyframe1, text = "Go to Attendance", font = ("times new roman", 15, "bold"), bg = "#C8FFD4")
        self.frame1_text.place(x = 40, y = 65)

        self.first = Button(self.bodyframe1, text = "Take Attendance", command=run_python_script, bg = "lightgrey", fg = "black", font = ("times new roman", 13), bd = 0, cursor = "hand2", activebackground = "grey")
        self.first.place(x = 75, y = 125)


        # =================== body frame 2 =================== #

        
        self.bodyframe2 = Frame(self.root, bg = "#C8FFD4")
        self.bodyframe2.place(x = 620, y = 110, width = 330, height = 230)

        self.frame2_text = Label(self.bodyframe2, text = "Today's Attendance Status:", font = ("times new roman", 13, "bold"), bg = "#C8FFD4")
        self.frame2_text.place(x = 40, y = 25)

        self.accept_image = Image.open("images\green.png")
        self.accept_image = self.accept_image.resize((20, 20))
        img_acc = ImageTk.PhotoImage(self.accept_image)
        self.accept = Label(self.bodyframe2, image = img_acc, bd = 0, bg ="#C8FFD4")
        self.accept.image = img_acc
        self.accept.place(x = 40, y = 65)

        self.accept_text = Label(self.bodyframe2, text = "Accepted  (DS class)", bg = "#C8FFD4", font = ("times new roman", 11, "bold"), bd = 0, cursor = "hand2")
        self.accept_text.place(x = 65, y = 65)

        self.accept_image = Image.open("images\green.png")
        self.accept_image = self.accept_image.resize((20, 20))
        img_acc = ImageTk.PhotoImage(self.accept_image)
        self.accept = Label(self.bodyframe2, image = img_acc, bd = 0, bg ="#C8FFD4")
        self.accept.image = img_acc
        self.accept.place(x = 40, y = 105)

        self.accept_text = Label(self.bodyframe2, text = "Accepted  (OS class)", bg = "#C8FFD4", font = ("times new roman", 11, "bold"), bd = 0, cursor = "hand2")
        self.accept_text.place(x = 65, y = 105)

        self.reject_image = Image.open("images\cross.png")
        self.reject_image = self.reject_image.resize((20, 20))
        img_rej = ImageTk.PhotoImage(self.reject_image)
        self.reject = Label(self.bodyframe2, image = img_rej, bd = 0, bg ="#C8FFD4")
        self.reject.image = img_rej
        self.reject.place(x = 40, y = 145)

        self.reject_text = Label(self.bodyframe2, text = "Denied  (CN class)", bg = "#C8FFD4", font = ("times new roman", 11, "bold"), bd = 0, cursor = "hand2")
        self.reject_text.place(x = 65, y = 145)


        self.pending_image = Image.open("images\pend.png")
        self.pending_image = self.pending_image.resize((20, 20))
        img_pend = ImageTk.PhotoImage(self.pending_image)
        self.pending = Label(self.bodyframe2, image = img_pend, bd = 0, bg ="#C8FFD4")
        self.pending.image = img_pend
        self.pending.place(x = 40, y = 185)

        self.reject_text = Label(self.bodyframe2, text = "Pending  (DBMS class)", bg = "#C8FFD4", font = ("times new roman", 11, "bold"), bd = 0, cursor = "hand2")
        self.reject_text.place(x = 65, y = 185)



        # ======================== body frame 3 ====================== #

        
        self.bodyframe3 = Frame(self.root, bg = "#F8E8EE")
        self.bodyframe3.place(x = 328, y = 360, width = 580, height = 300)

        Codes = ['101  -  (10:00 - 11:00)', '102  -  (11:00 - 12:00)', '103  -  (12:00 - 1:00)', '104  -  (2:00 - 3:00)', '105  -  (3:00 - 4:00)']
        Courses = ['Data Science - ( Prof.Darwin )', 'Operating Systems - ( Prof.Rahul )', 'Computer Networks - ( Prof.Anna Park )', 'Database Management System - ( Prof.Damon )', 'Cloud Computing - ( Prof.Elena )']


        table = ttk.Treeview(self.bodyframe3, columns = ('first', 'last'), show = 'headings')
        table.heading('first', text = 'Code')
        table.heading('last', text = 'Course')
        table.pack(fill = 'both', expand = True)
        table.place(x = 10, y = 20, width = 560, height = 250)


        for i in range(7):

            first = choice(Codes)
            last = choice(Courses)
            data = (first, last)
            table.insert(parent = '', index = 0, values = data)

        table.insert(parent = '', index = tk.END, values = ('XXXXX', 'YYYYY', 'ZZZZZ'))


        def item_select(_):
            print(table.selection())
            for i in table.selection():
                print(table.item(i)['values'])


        def delete_items(_):
            print('delete')
            for i in table.selection():
                table.delete(i)

        table.bind('<<TreeviewSelect>>', item_select)
        table.bind('<Delete>', delete_items)


        # Create a Frame widget
        frame = Frame(self.root, bg="#CBD18F", bd=0, highlightthickness=0)
        frame.place(relx=1.0, rely=1.0, anchor="se", relwidth=0.25, relheight=0.92)

        # ================= body frame 4 =============== #

        self.bodyframe4 = Frame(self.root, bg="#C8FFD4")
        # self.bodyframe4.place(x = 940, y = 360, width = 310, height = 300)
        self.bodyframe4.place(relx=0.985, rely=0.96, anchor="se", relwidth=0.22, relheight=0.49)

        self.frame4_text1 = Label(self.bodyframe4, text="Student ID:", font=("Arial Black", 14, "bold"), bg="#C8FFD4")
        self.frame4_text1.place(x=30, y=40)

        self.frame4_text2 = Label(self.bodyframe4, text=self.uniqueStudentID['uniqueStudentID'], font=("Bookman Old Style", 13, "bold"), fg="blue",
                                  bg="#C8FFD4")
        self.frame4_text2.place(x=160, y=44)

        self.frame4_text3 = Label(self.bodyframe4, text="Student Mail ID:", font=("Arial Black", 14, "bold"),
                                  bg="#C8FFD4")
        self.frame4_text3.place(x=30, y=80)

        self.frame4_text4 = Label(self.bodyframe4, text=self.student_data['email'],
                                  font=("Bookman Old Style", 13, "underline"), fg='blue', bg="#C8FFD4")
        self.frame4_text4.place(x=65, y=110)

        self.frame4_text5 = Label(self.bodyframe4, text="Password:", font=("Arial Black", 14, "bold"), bg="#C8FFD4")
        self.frame4_text5.place(x=30, y=145)

        self.frame4_text6 = Label(self.bodyframe4, text=self.student_data['password'], font=("Bookman Old Style", 13, "bold"), bg="#C8FFD4")
        self.frame4_text6.place(x=65, y=175)

        self.frame4_text7 = Label(self.bodyframe4, text="Contact No.:", font=("Arial Black", 14, "bold"), bg="#C8FFD4")
        self.frame4_text7.place(x=30, y=210)

        self.frame4_text8 = Label(self.bodyframe4, text=self.student_data['contact'], font=("Bookman Old Style", 13), bg="#C8FFD4")
        self.frame4_text8.place(x=65, y=240)

        self.frame4_text9 = Label(self.bodyframe4, text="Batch:", font=("Arial Black", 14, "bold"), bg="#C8FFD4")
        self.frame4_text9.place(x=30, y=275)

        self.frame4_text10 = Label(self.bodyframe4, text=self.student_data['batch'], font=("Bookman Old Style", 13), bg="#C8FFD4")
        self.frame4_text10.place(x=65, y=305)

        # Create the editing button
        self.edit_button = Button(self.bodyframe4, text="Edit details", cursor="hand2", font=("Arial Black", 14),
                                  fg='white', bg="#6666CD")
        self.edit_button.place(x=70, y=350, width=190, height=40)


        # ===================== calendar ===================== #

        self.cal_image = Image.open("images/calendar.png")
        self.cal_image = self.cal_image.resize((30, 30))
        img_cal = ImageTk.PhotoImage(self.cal_image)
        self.cal = Label(self.root, image=img_cal, bd=0, bg="#CBD18F")
        self.cal.image = img_cal
        self.cal.place(relx=0.79, rely=0.145, anchor="se")

        self.cal_heading = Label(self.root, text="Calendar", font=("Arial Black", 18), fg="black", bg="#CBD18F")
        self.cal_heading.place(relx=0.875, rely=0.15, anchor="se")

        self.mycal = Calendar(self.root, setmode="day", date_pattern="d/m/yy", font=("Bookman Old Style", 10, "bold"))
        self.mycal.place(relx=0.985, rely=0.42, anchor="se", height=220, width=340)


        # ================ time ================= #
        def time():
            string = StringVar()
            string = strftime('%A - %x\n\n%H:%M:%S %p')

            self.disp_time.config(text=string)
            self.disp_time.after(1000, time)

        self.disp_time = Label(self.sidebar, font=('Arial Black', 14), fg='black', bg="#EEEEDF")
        self.disp_time.place(x=80, y=33)

        time()

    def logout_function(self):
        messagebox.showinfo("Logout", f"Logging out!", parent=self.root)

        self.root.destroy()
        loginPage.Login()


if __name__ == '__main__':
    root = Tk()
    obj = loginPage.Login(root)
    root.mainloop()
