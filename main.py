import secrets
import string
import tkinter as tk
from tkinter import ttk
import pyperclip
import zxcvbn
import cryptography.fernet

# Create the GUI window
root = tk.Tk()
root.title("Password Generator")

# Define the font
font = ("Arial", 14)

# Set the window size and center it on the screen
window_width = 600
window_height = 350
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

strength_label = tk.Label(frame, text="", font=font, bg='#F0F0F0')
strength_label.pack(pady=10)


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
        password = ''.join(secrets.choice(lowercase) for i in range(2))
        password += ''.join(secrets.choice(uppercase) for i in range(2))
        password += ''.join(secrets.choice(digits) for i in range(2))
        password += ''.join(secrets.choice(symbols) for i in range(2))
        password += ''.join(secrets.choice(lowercase + uppercase + digits + symbols)
                            for i in range(password_length - 8))
        if (any(c.islower() for c in password) and any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and any(c in symbols for c in password)):
            break

    # Calculate the password strength score
    result = zxcvbn.zxcvbn(password)
    score = result["score"]

    # Determine the password strength based on the score
    if score == 0:
        strength = "Weak"
    elif score == 1 or score == 2:
        strength = "Average"
    elif score == 3:
        strength = "Strong"
    else:
        strength = "Very Strong"

    # Encrypt the password using the cryptography module
    # Generate a key using the Fernet module
    key = cryptography.fernet.Fernet.generate_key()

    # Create a Fernet cipher using the generated key
    cipher = cryptography.fernet.Fernet(key)

    # Encrypt the password using the cipher
    encrypted_password = cipher.encrypt(password.encode())

    # Copy the encrypted password to the clipboard
    pyperclip.copy(encrypted_password.decode())

    # Update the label text with the generated password and strength score
    label.config(text=password)
    strength_label.config(text=strength)


# Create a button to generate the password
style = ttk.Style()
style.configure('Custom.TButton', font=font)
button = ttk.Button(frame, text="Generate Password",
                    style='Custom.TButton', command=generate_password)
button.pack()

# Create a button to copy the password to the clipboard
copy_button = ttk.Button(frame, text="Copy to Clipboard",
                         style='Custom.TButton', command=lambda: pyperclip.copy(label.cget("text")))
copy_button.pack()

# Start the GUI event loop
root.mainloop()
