import os
import re
import uuid
import requests
import datetime
from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import Tk, ttk, Label, Entry, Button, filedialog, messagebox, Frame, PhotoImage
import loginPage

import firebase_admin
from firebase_admin import credentials, storage, db

# Initialize the Firebase SDK
cred = credentials.Certificate('serviceAccountKey.json')
app1 = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tkinter-attendancesystem-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://tkinter-attendancesystem.appspot.com'
})

# Create a reference to the Firebase Realtime Database
ref = db.reference('students')


def validate_contact_no(contact_no):
    pattern = r'^\d{0,10}$'
    if not re.match(pattern, contact_no):
        messagebox.showerror("Invalid Contact No.", "Contact No. should be 10 digits.")
        return False
    return True


class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Amity IntelliAMS | Registration")
        self.root.geometry("1080x680")
        self.root.resizable(False, False)

        # Load window icon image
        img1 = PhotoImage(file="images/icon.png")
        self.root.iconphoto(False, img1)

        # Load the background image
        background_image = Image.open("images/background_pattern2.jpg")
        blurred_image = background_image.filter(ImageFilter.BLUR)
        blurred_image = blurred_image.resize((1080, 680))
        self.background_photo = ImageTk.PhotoImage(blurred_image)

        # Create a label to display the background image
        background_label = Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a transparent image
        transparent_image = PhotoImage(width=1, height=1)

        # Load the logo image
        img = Image.open("images/Amity-University-Logo.jpg")
        img = img.resize((130, 80))

        self.logo = ImageTk.PhotoImage(img)
        self.logo_image = Label(self.root, image=self.logo)
        self.logo_image.place(x=0, y=0)

        # Create a Frame widget
        frame = Frame(self.root, bg="#EEEEDF", bd=0, highlightthickness=0)
        frame.place(relx=0.15, rely=0.5, anchor="w", relwidth=0.85, relheight=0.85)

        # Load the Registration icon for the window
        self.attend_image = Image.open("images/register_icon.png")
        self.attend_image = self.attend_image.resize((260, 210))
        img_att = ImageTk.PhotoImage(self.attend_image)
        self.attend = Label(self.root, image=img_att, bd=0, bg="#EEEEDF")
        self.attend.image = img_att
        self.attend.place(x=190, y=230)

        self.title = Label(self.root, text="REGISTER", font=("Eras Bold ITC", 45), fg="#6666CD", bg="#EEEEDF")
        # self.title.grid(row=1, column=3, pady=20, sticky=W)
        self.title.place(x=220, y=60)

        # Create the login button
        self.login_button = Button(self.root, text="LOGIN", command=self.login_function, cursor="hand2", font=("Arial Black", 14), fg="white", bg="green")
        self.login_button.place(x=850, y=60, width=180, height=40)
        # Create the login instruction label
        self.login_inst_label = Label(self.root, text="Already Registered!", font=("Arial Black", 10), fg="red", bg="#EEEEDF")
        self.login_inst_label.place(x=860, y=100)

        # Create the student ID label and entry field
        self.student_id_label = Label(self.root, text="Student ID:", font=("Arial Black", 15), bg="#EEEEDF")
        # self.student_id_label.grid(row=3, column=3, padx=10, pady=10, sticky=E)
        self.student_id_label.place(x=480, y=170)
        self.student_id_text = Entry(self.root, state='readonly', font=("Bookman Old Style", 12, "bold"))
        # self.student_id_text.grid(row=3, column=4, padx=10, pady=10)
        self.student_id_text.place(x=640, y=170, width=350, height=30)

        # Generate a random Student ID
        self.generate_student_id()

        # Create the full name label and entry field
        self.fullname_label = Label(self.root, text="Full Name:", font=("Arial Black", 15), bg="#EEEEDF")
        # self.fullname_label.grid(row=4, column=3, padx=10, pady=10, sticky=E)
        self.fullname_label.place(x=485, y=225)
        self.fullname_text = Entry(self.root, highlightthickness=1, highlightbackground="white", font=("Bookman Old Style", 12))
        # self.fullname_text.grid(row=4, column=4, padx=10, pady=10)
        self.fullname_text.place(x=640, y=225, width=350, height=30)

        # Create the email label and entry field
        self.email_label = Label(self.root, text="Email:", font=("Arial Black", 15), bg="#EEEEDF")
        # self.email_label.grid(row=5, column=3, padx=10, pady=10, sticky=E)
        self.email_label.place(x=535, y=280)
        self.email_text = Entry(self.root, highlightthickness=1, highlightbackground="white", font=("Bookman Old Style", 12))
        # self.email_text.grid(row=5, column=4, padx=10, pady=10)
        self.email_text.place(x=640, y=280, width=350, height=30)

        # Create the batch label and entry field
        self.batch_label = Label(self.root, text="Batch:", font=("Arial Black", 15), bg="#EEEEDF")
        self.batch_label.place(x=535, y=335)
        batch_values = ["B. Tech (CSE)", "B. Tech (IT)", "B Com.", "BCA", "M Com."]  # Example list of batch values
        self.batch_combobox = ttk.Combobox(self.root, values=batch_values, font=("Bookman Old Style", 12))
        self.batch_combobox.place(x=640, y=335, width=350, height=30)

        # Create the contact no. label and entry field
        self.contact_label = Label(self.root, text="Contact No.:", font=("Arial Black", 15), bg="#EEEEDF")
        self.contact_label.place(x=470, y=390)
        self.contact_entry = Entry(self.root, highlightthickness=1, highlightbackground="white", font=("Bookman Old Style", 12))
        self.contact_entry.place(x=640, y=390, width=350, height=30)

        # Validate Contact No.
        validate_contact = (self.root.register(validate_contact_no), '%P')
        self.contact_entry.config(validate='key', validatecommand=validate_contact)

        # Create the password label and entry field
        self.password_label = Label(self.root, text="Password:", font=("Arial Black", 15), bg="#EEEEDF")
        # self.password_label.grid(row=6, column=3, padx=10, pady=10, sticky=E)
        self.password_label.place(x=500, y=445)
        self.password_text = Entry(self.root, show="*", highlightthickness=1, highlightbackground="white", font=("Bookman Old Style", 12))
        # self.password_text.grid(row=6, column=4, padx=10, pady=10)
        self.password_text.place(x=640, y=445, width=350, height=30)

        # Create the confirm password label and entry field
        self.confirm_password_label = Label(self.root, text="Confirm Password:", font=("Arial Black", 15), bg="#EEEEDF")
        # self.confirm_password_label.grid(row=7, column=3, padx=10, pady=10, sticky=E)
        self.confirm_password_label.place(x=410, y=500)
        self.confirm_password_text = Entry(self.root, show="*", highlightthickness=1, highlightbackground="white", font=("Bookman Old Style", 12))
        # self.confirm_password_text.grid(row=7, column=4, padx=10, pady=10)
        self.confirm_password_text.place(x=640, y=500, width=350, height=30)

        # Create the image upload label and entry field
        self.upload_label = Label(self.root, text="Upload Image:", font=("Arial Black", 15), bg="#EEEEDF")
        self.upload_label.place(x=460, y=555)
        # Create the image upload button
        self.upload_button = Button(self.root, text="Select", command=self.upload_file, cursor="hand2", font=("Arial Black", 12))
        # self.upload_button.grid(row=8, column=3, padx=10, pady=10)
        self.upload_button.place(x=640, y=555, width=200, height=30)

        # Create the label to display the selected file name
        self.selected_file_label = Label(self.root, text="", bg="#EEEEDF")
        self.selected_file_label.place(x=850, y=560)

        # Create the register button
        self.register_button = Button(self.root, text="Register", command=self.register_function, cursor="hand2", font=("Arial Black", 14), bg="#6666CD")
        # self.register_button.grid(row=9, column=4, padx=10, pady=10)
        self.register_button.place(x=850, y=610, width=190, height=40)

    def generate_student_id(self):
        # Generate a random Student ID using the uuid module
        student_id = str(uuid.uuid4().fields[-1])[:6]
        self.student_id_text.config(state='normal')
        self.student_id_text.delete(0, END)
        self.student_id_text.insert(0, student_id)
        self.student_id_text.config(state='readonly')

    def upload_file(self):
        # Open a file dialog to select an image file
        filetypes = (("Image files", "*.jpg;*.png"), ("All files", "*.*"))
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        # Display the selected file name in the label
        if file_path:
            filename = os.path.basename(file_path)
            self.selected_file_label.config(text="" + filename, font=("Bookman Old Style", 10, "bold"), fg="green")
        else:
            self.selected_file_label.config(text="")

    def login_function(self):
        self.root.destroy()
        loginPage.Login()

    def register_function(self):
        # Get the student ID from the entry field
        student_id = self.student_id_text.get()

        # Get other input values
        fullname = self.fullname_text.get()
        email = self.email_text.get()
        batch = self.batch_combobox.get()
        contact = self.contact_entry.get()
        password = self.password_text.get()
        confirm_password = self.confirm_password_text.get()

        # Check if all fields are filled
        if not student_id or not fullname or not email or not batch or not contact or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all the fields")
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Check if an image file is selected
        if self.selected_file_label.cget("text") == "":
            messagebox.showerror("Error", "Please select an image file", parent=self.root)
            return


        # Create a new child node with the student ID as the key
        student_ref = ref.child(student_id)

        # Set the values under the student's node
        student_ref.set({
            'fullname': fullname,
            'email': email,
            'batch': batch,
            'contact': contact,
            'password': password
        })

        # Registration successful message
        # message = f"Successfully Registered!\n\nYour Student ID: {student_id}\nFull Name: {fullname}\nEmail: {email}"
        # messagebox.showinfo("Welcome", message, parent=self.root)

        # Display success message in a message box
        message = f"Data successfully saved!\n\nStudent ID: {student_id}\nName: {fullname}"
        messagebox.showinfo("Success", message)

        # Clear the input fields
        self.student_id_text.delete(0, 'end')
        self.fullname_text.delete(0, 'end')
        self.email_text.delete(0, 'end')
        self.batch_combobox.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.password_text.delete(0, 'end')
        self.confirm_password_text.delete(0, 'end')
        # Clear the selected file label
        self.selected_file_label.config(text="")

        # Reset the file path variable
        self.file_path = ""

        # Generate a new student ID
        self.generate_student_id()


if __name__ == '__main__':
    root = Tk()
    registration = RegistrationForm(root)
    root.mainloop()

