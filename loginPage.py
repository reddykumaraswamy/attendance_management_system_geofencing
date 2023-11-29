import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import font
import studentDashboard
import registrationPage
from firebase_admin import db


class Login:
    def __init__(self):
        self.root = Toplevel()
        self.root.title("Amity IntelliAMS | Login")
        # self.root.geometry("1199x600+100+50")
        self.root.geometry("1080x680")
        self.root.resizable(False, False)


        # ================ icon ================== #

        img1 = PhotoImage(file="images/icon.png")
        self.root.iconphoto(False, img1)

        # ======================= back ground image ================= #
        self.bg = ImageTk.PhotoImage(file="images/Amity.jpg")

        canvas_widget = Canvas(self.root, width=800, height=600)
        canvas_widget.pack(fill="both", expand=True)

        canvas_widget.create_image(0, 0, image=self.bg, anchor="nw")

        def resize_image(e):
            global image, resized, image2

            image = Image.open("images/Amity.jpg")

            resized = image.resize((e.width, e.height), Image.ANTIALIAS)

            image2 = ImageTk.PhotoImage(resized)

            canvas_widget.create_image(0, 0, image=image2, anchor='nw')

        self.root.bind("<Configure>", resize_image)

        # =============================== amity logo ========================= #

        img = Image.open("images/Amity-University-Logo.jpg")
        img = img.resize((130, 80))

        self.logo = ImageTk.PhotoImage(img)
        self.logo_image = Label(self.root, image=self.logo).place(x=0, y=0)

        # ======================== white frame ===================== #

        Frame_login = Frame(self.root, bg="#F0F0F8")
        Frame_login.place(relx=0.25, rely=0.56, anchor="w", relwidth=0.75, relheight=0.7)

        # ============================== image in frame ========================== #

        self.attend_image = Image.open("images/20945796.jpg")
        self.attend_image = self.attend_image.resize((300, 300))
        img_att = ImageTk.PhotoImage(self.attend_image)
        self.attend = Label(Frame_login, image=img_att, bd=0, bg="#F0F0F8")
        self.attend.image = img_att
        self.attend.place(x=30, y=110)

        # =============== login here ======================== #

        self.title = Label(Frame_login, text="Login Here", font=("Eras Bold ITC", 40), fg="#0000BF", bg="#F0F0F8")
        self.title.place(x=300, y=30)

        # ================================== specified login here ====================== #

        self.desc = Label(Frame_login, text="Specified Login Area", font=("Bookman Old Style", 15, "underline"), fg="black", bg="#F0F0F8")
        self.desc.place(x=350, y=100)

        # =========================== small student icon ======================= #

        self.grad_image = Image.open("images/student.png")
        self.grad_image = self.grad_image.resize((40, 40))
        img_g = ImageTk.PhotoImage(self.grad_image)
        self.grad = Label(Frame_login, image=img_g, bd=0)
        self.grad.image = img_g
        self.grad.place(x=405, y=140)

        # ========================== small faculty icon ========================= #

        self.prof_image = Image.open("images/professor.png")
        self.prof_image = self.prof_image.resize((40, 40))
        img_p = ImageTk.PhotoImage(self.prof_image)
        self.prof = Label(Frame_login, image=img_p, bd=0)
        self.prof.image = img_p
        self.prof.place(x=535, y=140)

        # ========================== small admin icon ======================== #

        self.admin_image = Image.open("images/admin.png")
        self.admin_image = self.admin_image.resize((40, 40))
        img_a = ImageTk.PhotoImage(self.admin_image)
        self.admin = Label(Frame_login, image=img_a, bd=0)
        self.admin.image = img_a
        self.admin.place(x=665, y=140)

        # =========================== buttons in between =========================== #

        self.btn1 = Button(Frame_login, fg="white", bg="#0000BF", cursor="hand2", text="STUDENT", bd=0.5, font=("Arial Black", 12, "bold"))
        self.btn1.place(x=360, y=180, width=130, height=40)
        self.btn2 = Button(Frame_login, fg="grey", bg="#E0E0FF", cursor="hand2", text="FACULTY", bd=0.5, font=("Arial Black", 12, "bold"))
        self.btn2.place(x=490, y=180, width=130, height=40)
        self.btn3 = Button(Frame_login, fg="grey", bg="#E0E0FF", cursor="hand2", text="ADMIN", bd=0.5, font=("Arial Black", 12, "bold"))
        self.btn3.place(x=620, y=180, width=130, height=40)

        # ============================= student id ==================================== #

        self.lbl_user = Label(Frame_login, text="STUDENT ID", font=("Arial Black", 13), fg="black",bg="#F0F0F8")
        self.lbl_user.place(x=360, y=240)
        self.txt_user = Entry(Frame_login, font=("Bookman Old Style", 12), bg="white", highlightthickness=1, highlightbackground="white")
        self.txt_user.place(x=360, y=275, width=350, height=35)

        # ============================= password ========================== #

        self.lbl_pass = Label(Frame_login, text="PASSWORD", font=("Arial Black", 13), fg="black",bg="#F0F0F8")
        self.lbl_pass.place(x=360, y=320)
        self.txt_pass = Entry(Frame_login, show="*", font=("Bookman Old Style", 12), bg="white",  highlightthickness=1, highlightbackground="white")
        self.txt_pass.place(x=360, y=355, width=350, height=35)

        # ================================= forgot password ============================= #

        self.forget_btn = Button(Frame_login, text="Forgot Password?", bg="#F0F0F8", cursor="hand2", bd=0, fg="red", font=("Bookman Old Style", 12, "underline"))
        self.forget_btn.place(x=360, y=400)

        # =============================== login button =========================== #

        self.Login_btn = Button(self.root, command=self.login_function, cursor="hand2", text="LOGIN", fg="white", bg="#0000BF", font=("Arial Black", 18))
        self.Login_btn.place(x=800, y=600, width=180, height=40)


    # ========================= error fields of login button ====================================== #


    def login_function(self):
        # Get the entered student ID and password
        student_id = self.txt_user.get()
        password = self.txt_pass.get()

        data = {"uniqueStudentID": student_id}
        with open('data/data.json', 'w+') as outfile:
            json.dump(data, outfile, indent=4)

            # Check if the student ID and password are empty
        if student_id == "" or password == "":
            messagebox.showerror("Invalid Input!", "Enter Student ID and Password", parent=self.root)

        else:
            ref = db.reference('students')

            # Get the student's data from the database
            student_data = ref.child(student_id).get()

            if student_data is None:
                # Student ID not found in the database
                self.show_error_retry("Invalid Username/Password")
            else:
                # Check if the entered password matches the stored password
                stored_password = student_data.get('password')

                if password == stored_password:
                    # Password matches
                    fullname = student_data.get('fullname')
                    messagebox.showinfo("Welcome", f"Welcome, {fullname}", parent=self.root)

                    self.root.destroy()
                    studentDashboard.Dashboard()
                else:
                    # Incorrect password
                    self.show_error_retry("Invalid Username/Password")

    def show_error_retry(self, error_message):
        # Display error message with retry button
        retry = messagebox.askretrycancel("Invalid Credentials!", error_message, parent=self.root)
        if retry:
            self.txt_user.delete(0, 'end')
            self.txt_pass.delete(0, 'end')


if __name__ == '__main__':
    root = Tk()
    obj = registrationPage.RegistrationForm(root)
    root.mainloop()
