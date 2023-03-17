import random
import string
import tkinter as tk
from tkinter import ttk

# Create the GUI window
root = tk.Tk()
root.title("Password Generator")

# Define the font
font = ("Arial", 14)

# Set the window size and center it on the screen
window_width = 600
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the background color
root.configure(bg='#F0F0F0')

# Create a frame to hold the label, spinbox, and button
frame = tk.Frame(root, bg='#F0F0F0')
frame.pack(pady=20)

# Create a label widget
label = tk.Label(
    frame, text="Click the button to generate a password", font=font, bg='#F0F0F0')
label.pack(pady=10)

# Create a spinbox widget to select the password length
length_label = tk.Label(frame, text="Password Length", font=font, bg='#F0F0F0')
length_label.pack()
length_spinbox = tk.Spinbox(frame, from_=8, to=48, font=font)
length_spinbox.pack()

# Create a function to generate a random password


def generate_password():
    # Get the password length from the spinbox
    password_length = int(length_spinbox.get())

    # Define the characters to use for the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation.replace('"', '').replace("'", "")

    # Ensure that the password meets the requirements of Google Gmail
    while True:
        password = ''.join(random.choice(lowercase) for i in range(2))
        password += ''.join(random.choice(uppercase) for i in range(2))
        password += ''.join(random.choice(digits) for i in range(2))
        password += ''.join(random.choice(symbols) for i in range(2))
        password += ''.join(random.choice(lowercase + uppercase + digits + symbols)
                            for i in range(password_length - 8))
        if (any(c.islower() for c in password) and any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and any(c in symbols for c in password)):
            break

    # Update the label text with the generated password
    label.config(text=password)


# Create a button to generate the password
style = ttk.Style()
style.configure('Custom.TButton', font=font)
button = ttk.Button(frame, text="Generate Password",
                    style='Custom.TButton', command=generate_password)
button.pack()

# Start the GUI event loop
root.mainloop()
