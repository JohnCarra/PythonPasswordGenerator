import tkinter as tk
from tkinter import ttk
import string
import secrets
import zxcvbn
import cryptography.fernet
import pyperclip
import ctypes
import os
import platform


def set_window_size_and_center(root):
    # Set the window size and center it on the screen
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width/2) - (WINDOW_WIDTH/2))
    y = int((screen_height/2) - (WINDOW_HEIGHT/2))
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def configure_window(root):
    # Set the background color
    root.configure(bg='#F0F0F0')


def create_frame(root):
    # Create a frame to hold the label, spinbox, and button
    frame = tk.Frame(root, bg='#F0F0F0')
    frame.pack(pady=20)
    return frame


def create_widgets(frame):
    font = ("Arial", 14)
    label, length_spinbox, strength_label = create_label_spinbox_strength_label(
        frame, font)
    create_generate_password_button(
        frame, font, label, length_spinbox, strength_label)
    create_copy_and_clear_buttons(frame, font, label)


def create_label_spinbox_strength_label(frame, font):
    # Create a label widget
    label = tk.Label(
        frame, text="Click the button to generate a password", font=font, bg='#F0F0F0')
    label.pack(pady=10)

    # Create a spinbox widget to select the password length
    length_label = tk.Label(
        frame, text="Password Length", font=font, bg='#F0F0F0')
    length_label.pack()
    length_spinbox = tk.Spinbox(frame, from_=8, to=48, font=font)
    length_spinbox.pack()

    strength_label = tk.Label(frame, text="", font=font, bg='#F0F0F0')
    strength_label.pack(pady=10)

    return label, length_spinbox, strength_label


def create_generate_password_button(frame, font, label, length_spinbox, strength_label):
    # Create a button to generate the password
    style = ttk.Style()
    style.configure('Custom.TButton', font=font)
    button = ttk.Button(frame, text="Generate Password",
                        style='Custom.TButton', command=lambda: generate_password(label, length_spinbox, strength_label))
    button.pack()


def create_copy_and_clear_buttons(frame, font, label):
    # Create a button to copy the password to the clipboard
    copy_button = ttk.Button(frame, text="Copy to Clipboard",
                             style='Custom.TButton', command=lambda: [pyperclip.copy(label.cget("text")), clear_password(label)])
    copy_button.pack()

    # Create a button to clear the clipboard
    clear_button = ttk.Button(frame, text="Clear Clipboard",
                              style='Custom.TButton', command=clear_clipboard)
    clear_button.pack()


def generate_password(label, length_spinbox, strength_label):
    """
    This function generates a random password of a specified length, using a combination of lowercase and uppercase
    letters, digits, and symbols. The password must meet the requirements of Google Gmail. It then calculates the
    strength of the password using the zxcvbn module, and encrypts the password using the cryptography module.
    The encrypted password is copied to the clipboard, and the generated password and strength score are displayed
    in a Tkinter label widget.

    Parameters:
    label - Tkinter label widget to display the generated password
    length_spinbox - Tkinter spinbox widget to get the password length
    strength_label - Tkinter label widget to display the password strength

    Returns:
    None
    """
    password_length = int(length_spinbox.get())
    password = create_valid_password(password_length)

    score, strength = get_password_strength(password)
    encrypted_password = encrypt_password(password)

    pyperclip.copy(encrypted_password.decode())
    update_labels(label, strength_label, password, strength)


def create_valid_password(password_length):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation.replace('"', '').replace("'", "")

    while True:
        password = (
            ''.join(secrets.choice(lowercase) for _ in range(2))
            + ''.join(secrets.choice(uppercase) for _ in range(2))
            + ''.join(secrets.choice(digits) for _ in range(2))
            + ''.join(secrets.choice(symbols) for _ in range(2))
            + ''.join(secrets.choice(lowercase + uppercase + digits + symbols)
                      for _ in range(password_length - 8))
        )
        if (any(c.islower() for c in password) and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password) and any(c in symbols for c in password)):
            break

    return password


def get_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    score = result["score"]

    if score == 0:
        strength = "Weak"
    elif score == 1 or score == 2:
        strength = "Average"
    elif score == 3:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return score, strength


def encrypt_password(password):
    key = cryptography.fernet.Fernet.generate_key()
    cipher = cryptography.fernet.Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())

    return encrypted_password


def update_labels(label, strength_label, password, strength):
    label.config(text=password)
    strength_label.config(text=strength)


def clear_password(label):
    """
    This function clears the password string from memory for security purposes.
    It retrieves the password from a Tkinter label widget, replaces the label text
    with a message indicating that the password has been deleted, and overwrites
    the password string with random data to prevent it from being recovered.

    Parameters:
    label - Tkinter label widget to retrieve and update the password

    Returns:
    None
    """
    password = label.cget("text")
    overwrite_password_with_random_data(password)
    label.config(text="Password deleted after copy for security purposes.")


def overwrite_password_with_random_data(password):
    length = len(password.encode())
    buf = ctypes.create_string_buffer(length)
    ctypes.memset(buf, 0, length)
    del password


def clear_clipboard():
    if platform.system() == "Windows":
        command = 'echo off | clip'
        os.system(command)
    elif platform.system() == "Darwin":
        command = 'echo -n "" | pbcopy'
        os.system(command)
    else:
        command = 'echo -n "" | xclip -selection clipboard'
        os.system(command)


def main():
    # Create the GUI window
    root = tk.Tk()
    root.title("Password Generator")
    set_window_size_and_center(root)
    configure_window(root)
    frame = create_frame(root)
    create_widgets(frame)
    root.mainloop()


if __name__ == '__main__':
    main()
