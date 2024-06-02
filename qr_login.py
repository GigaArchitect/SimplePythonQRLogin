import tkinter as tk


def open_generate_window():
    # Create a new window (top-level window)
    new_window = tk.Toplevel(root)
    new_window.title("Info")

    # Set the size of the new window
    new_window.geometry("350x350+105+105")

    # Add a label to the new window
    label = tk.Label(new_window, text="Enter Credintials")
    label.pack(pady=10)

    nameLabel = tk.Label(new_window, text="Name : ")
    passwordLabel = tk.Label(new_window, text="Password : ")
    passwordConfirmLabel = tk.Label(new_window, text="Confirm : ")

    nameLabel.place(x=5, y=35)
    passwordLabel.place(x=5, y=75)
    passwordConfirmLabel.place(x=5, y=105)
    # Name and Password input
    name = tk.Entry(
        new_window,
        width=15,
    )
    password = tk.Entry(new_window, width=15, show="*")
    password_confirm = tk.Entry(new_window, width=15, show="*")

    name.place(x=85, y=35)
    password.place(x=85, y=75)
    password_confirm.place(x=85, y=105)

    # Add a button to close the new window
    close_button = tk.Button(new_window, text="generate")
    close_button.pack(pady=95)


root = tk.Tk()
root.geometry("500x500+250+250")
root.title("QR Login System")


registerLabel = tk.Label(root, text="Register : ", font=("Arial", 16))
registerLabel.place(x= 15, y = 55)
registerButton = tk.Button(root, text= "Register", font=("Arial", 16), command=open_generate_window)
registerButton.place(x=250, y = 50)

loginLabel = tk.Label(root, text="Login : ", font=("Arial", 16))
loginLabel.place(x= 15, y = 155)
loginButton = tk.Button(root, text= "Login", font=("Arial", 16))
loginButton.place(x=265, y = 150)

root.mainloop()
