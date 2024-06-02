import tkinter as tk
from tkinter import messagebox
import sqlite3
from hashlib import md5
import pyotp
import qrcode
from PIL import Image, ImageTk
import os

# Connect to the database
connection_db = sqlite3.connect("login.db")
db_cursor = connection_db.cursor()
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name VARCHAR(35) PRIMARY KEY, 
    password VARCHAR(45), 
    seedValue VARCHAR(80)
)
""")

def display_photo(path):
    top = tk.Toplevel()
    top.title("Display Photo")

    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    label = tk.Label(top, image=img)
    label.image = img  # Keep a reference to the image to avoid garbage collection
    label.pack()

    top.mainloop()

def open_generate_window():
    new_window = tk.Toplevel(root)
    new_window.title("Info")

    new_window.geometry("350x350+105+105")

    label = tk.Label(new_window, text="Enter Credentials")
    label.pack(pady=10)

    nameLabel = tk.Label(new_window, text="Name : ")
    passwordLabel = tk.Label(new_window, text="Password : ")
    passwordConfirmLabel = tk.Label(new_window, text="Confirm : ")

    nameLabel.place(x=5, y=35)
    passwordLabel.place(x=5, y=75)
    passwordConfirmLabel.place(x=5, y=105)

    name = tk.Entry(new_window, width=15)
    password = tk.Entry(new_window, width=15, show="*")
    password_confirm = tk.Entry(new_window, width=15, show="*")

    name.place(x=85, y=35)
    password.place(x=85, y=75)
    password_confirm.place(x=85, y=105)

    key = pyotp.random_base32()
    print(f"Generated key: {key}")

    def register_helper_func():
        if password.get() == password_confirm.get():
            try:
                hashed_password = md5(password.get().encode("utf-8")).hexdigest()
                db_cursor.execute("INSERT OR REPLACE INTO users (name, password, seedValue) VALUES (?, ?, ?)",
                                  (name.get(), hashed_password, key))
                connection_db.commit()
                uri = pyotp.totp.TOTP(key).provisioning_uri(name=name.get(), issuer_name="mustafa_corporate")
                
                # Ensure images directory exists
                if not os.path.exists("images"):
                    os.makedirs("images")

                img_path = f"images/{name.get()}.png"
                qrcode.make(uri).save(img_path)
                display_photo(img_path)

                print(f"Provisioning URI: {uri}")
                messagebox.showinfo("Success", "User registered successfully!")
            except Exception as e:
                messagebox.showerror("Failed", f"An error occurred: {e}")
        else:
            messagebox.showerror("Failed", "Passwords don't match.")

    register_button = tk.Button(new_window, text="Register", command=register_helper_func)
    register_button.pack(pady=95)

def open_login_window():
    new_window = tk.Toplevel(root)
    new_window.title("Info")

    new_window.geometry("350x350+105+105")

    label = tk.Label(new_window, text="Enter Credentials")
    label.pack(pady=10)

    nameLabel = tk.Label(new_window, text="Name : ")
    passwordLabel = tk.Label(new_window, text="Password : ")
    otpLabel = tk.Label(new_window, text="OTP : ")

    nameLabel.place(x=5, y=35)
    passwordLabel.place(x=5, y=75)
    otpLabel.place(x=5, y=115)

    name = tk.Entry(new_window, width=15)
    password = tk.Entry(new_window, width=15, show="*")
    otp = tk.Entry(new_window, width=15)

    name.place(x=85, y=35)
    password.place(x=85, y=75)
    otp.place(x=85, y=115)

    def login_helper_func():
        try:
            # Fetch the user data from the database
            db_cursor.execute("SELECT password, seedValue FROM users WHERE name = ?", (name.get(),))
            result = db_cursor.fetchone()

            if result:
                stored_password, seed_value = result
                print(f"Retrieved seed: {seed_value}")
                hashed_password = md5(password.get().encode("utf-8")).hexdigest()
                
                # Validate the password
                if hashed_password == stored_password:
                    totp = pyotp.TOTP(str(seed_value))
                    current_otp = totp.now()
                    print(f"Expected OTP: {current_otp}")
                    
                    # Validate the OTP
                    if totp.verify(otp.get(), valid_window=1):  # Allow a window of 30 seconds before and after
                        messagebox.showinfo("Success", "Login successful!")
                    else:
                        messagebox.showerror("Failed", "Invalid OTP.")
                else:
                    messagebox.showerror("Failed", "Invalid password.")
            else:
                messagebox.showerror("Failed", "User not found.")
        except Exception as e:
            messagebox.showerror("Failed", f"An error occurred: {e}")

    login_button = tk.Button(new_window, text="Login", command=login_helper_func)
    login_button.pack(pady=95)

root = tk.Tk()
root.geometry("500x500+250+250")
root.title("QR Login System")


registerLabel = tk.Label(root, text="Register : ", font=("Arial", 16))
registerLabel.place(x= 15, y = 55)
registerButton = tk.Button(root, text= "Register", font=("Arial", 16), command=open_generate_window)
registerButton.place(x=250, y = 50)

loginLabel = tk.Label(root, text="Login : ", font=("Arial", 16))
loginLabel.place(x= 15, y = 155)
loginButton = tk.Button(root, text= "Login", font=("Arial", 16), command=open_login_window)

loginButton.place(x=265, y = 150)

root.mainloop()
