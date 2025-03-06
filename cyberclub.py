import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from PIL import Image, ImageTk  
import re  
import random  

# Database setup
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    name TEXT,
                    email TEXT)''')
conn.commit()

# Cybersecurity-Themed Welcome Messages
welcome_messages = [
    "Access Granted, {}! Welcome to the CDU Cybersecurity Club! 🔓🚀.\n\nFurther info will be sent to your email soon.",
    "Intruder detected… just kidding! Welcome to the CDU Cybersecurity Club, {}! 😆🔍\n\nFurther info will be sent to your email soon.",
    "Alert! {} has just entered the Cybersecurity Club network! 🚨🖥️\n\nFurther info will be sent to your email soon.",
    "Encryption complete! {} is now securely added to the club database! 🔒📁\n\nFurther info will be sent to your email soon.",
    "You’re now authenticated, {}! Welcome to the CDU Cybersecurity Club! 🏆🔍\n\nFurther info will be sent to your email soon."
]

# Function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Function to enable submit button when all fields are filled
def check_fields(*args):
    student_id = entry_student_id.get().strip()
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    
    if student_id and name and is_valid_email(email):
        submit_button.config(state="normal")
    else:
        submit_button.config(state="disabled")

# Function to handle form submission
def submit_form():
    student_id = entry_student_id.get().strip()
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    
    if not student_id or not name or not is_valid_email(email):
        messagebox.showwarning("Invalid Input", "Please fill out all fields correctly!")
        return
    
    cursor.execute("INSERT INTO members (student_id, name, email) VALUES (?, ?, ?)", (student_id, name, email))
    conn.commit()
    
    entry_student_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    submit_button.config(state="disabled")

    show_message_page(name)  # Show message page

def show_message_page(name):
    form_frame.pack_forget()
    welcome_label.pack_forget()
    join_button.pack_forget()

    message_text = random.choice(welcome_messages).format(name)  
    split_message = message_text.split(name)  

    # Clear previous messages before displaying a new one
    message_label.pack_forget()
    name_label.pack_forget()
    message_label2.pack_forget()

    # Display first part of the message (bold)
    message_label.config(text=split_message[0], fg="white", font=("Helvetica", 30, "bold"))
    message_label.pack(pady=(50, 10))  # Space above

    # Highlight user name in Matrix Green
    name_label.config(text=name, fg="#00FF00", font=("Helvetica", 36, "bold"))
    name_label.pack(pady=(0, 10))

    # Display the rest of the message
    message_label2.config(text=split_message[1], fg="white", font=("Helvetica", 28))
    message_label2.pack(pady=(0, 50))  # Space below for balance

    # Ensure the welcome page restores correctly after redirection
    root.after(5000, restore_welcome_screen)
    

def restore_welcome_screen():
    # Hide message labels to prevent clutter on the welcome screen
    message_label.pack_forget()
    name_label.pack_forget()
    message_label2.pack_forget()

    # Restore the welcome message and button
    welcome_label.pack(pady=40)
    join_button.pack(pady=30, ipadx=30, ipady=15)

# Function to show registered members
def show_members(event=None):
    top = tk.Toplevel(root)
    top.title("Registered Members")
    top.geometry("700x500")

    columns = ("#", "Student ID", "Name", "Email")
    tree = ttk.Treeview(top, columns=columns, show="headings")
    tree.heading("#", text="No.")
    tree.heading("Student ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    
    cursor.execute("SELECT student_id, name, email FROM members")
    records = cursor.fetchall()
    
    for i, record in enumerate(records, start=1):
        tree.insert("", "end", values=(i, record[0], record[1], record[2]))

    tree.pack(expand=True, fill="both")

# Function to securely exit application
def secure_exit(event=None):
    security_code = "shiraz"
    entered_code = simpledialog.askstring("Security Code", "Enter security code to exit:", show='*')
    if entered_code == security_code:
        root.attributes("-fullscreen", False)
        root.destroy()
    else:
        messagebox.showwarning("Access Denied", "Incorrect security code!")

# Function to show the form page
def show_form():
    welcome_label.pack_forget()
    join_button.pack_forget()
    message_label.pack_forget()
    name_label.pack_forget()
    message_label2.pack_forget()
    form_frame.pack(pady=40)
    entry_student_id.focus_set()
    submit_button.config(state="disabled")  # Ensure button is initially disabled

# Function to go back to the welcome screen
def show_welcome_screen():
    form_frame.pack_forget()
    message_label.pack_forget()
    name_label.pack_forget()
    message_label2.pack_forget()
    welcome_label.pack(pady=40)
    join_button.pack(pady=30, ipadx=30, ipady=15)  

# GUI Setup
root = tk.Tk()
root.title("CDU Cybersecurity Club")
root.geometry("900x700")
root.configure(bg="black")
root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("Restricted", "You cannot close this application manually!"))
root.attributes("-fullscreen", True)

# Load CDU Cybersecurity Club Logo
logo_img = Image.open("cyberclublogo.jpg")
logo_img = logo_img.resize((400, 400))
logo_photo = ImageTk.PhotoImage(logo_img)

# Display the logo at the top
logo_label = tk.Label(root, image=logo_photo, bg="black")
logo_label.pack(pady=30)

# Welcome Screen
welcome_label = tk.Label(root, text="Welcome to CDU Cybersecurity Club", font=("Helvetica", 32, "bold"), fg="#00FF00", bg="black")
welcome_label.pack(pady=40)

join_button = tk.Button(root, text="Become a Member", font=("Helvetica", 22, "bold"), bg="white", fg="black", command=show_form)
join_button.pack(pady=30, ipadx=30, ipady=15)

# Form Screen
form_frame = tk.Frame(root, bg="black")

tk.Label(form_frame, text="Student ID:", font=("Helvetica", 24), fg="white", bg="black").grid(row=0, column=0, pady=15, padx=15)
entry_student_id = tk.Entry(form_frame, font=("Helvetica", 24))
entry_student_id.grid(row=0, column=1, pady=15, padx=15)

tk.Label(form_frame, text="Name:", font=("Helvetica", 24), fg="white", bg="black").grid(row=1, column=0, pady=15, padx=15)
entry_name = tk.Entry(form_frame, font=("Helvetica", 24))
entry_name.grid(row=1, column=1, pady=15, padx=15)

tk.Label(form_frame, text="Email:", font=("Helvetica", 24), fg="white", bg="black").grid(row=2, column=0, pady=15, padx=15)
entry_email = tk.Entry(form_frame, font=("Helvetica", 24))
entry_email.grid(row=2, column=1, pady=15, padx=15)

submit_button = tk.Button(form_frame, text="Submit", font=("Helvetica", 22, "bold"), bg="white", fg="black", state="disabled", command=submit_form)
submit_button.grid(row=3, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

go_back_button = tk.Button(form_frame, text="Go Back", font=("Helvetica", 22, "bold"), bg="white", fg="black", command=show_welcome_screen)
go_back_button.grid(row=4, column=0, columnspan=2, pady=10, ipadx=20, ipady=10)

# Message Page
message_label = tk.Label(root, text="", font=("Helvetica", 30, "bold"), bg="black")
name_label = tk.Label(root, text="", font=("Helvetica", 30, "bold"), bg="black")
message_label2 = tk.Label(root, text="", font=("Helvetica", 30, "bold"), bg="black")

# **Bind Entry Fields**
entry_student_id.bind("<KeyRelease>", check_fields)
entry_name.bind("<KeyRelease>", check_fields)
entry_email.bind("<KeyRelease>", check_fields)

# **Rebind Shortcuts**
root.bind("<Control-Shift-X>", secure_exit)
root.bind("<Control-Shift-V>", show_members)

# Run the application
root.mainloop()