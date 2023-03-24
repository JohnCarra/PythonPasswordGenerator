import tkinter as tk
from tkinter import ttk
import pyperclip
import password_utils
from clipboard import clear_clipboard


def set_window_size_and_center(root):
    # Set the window size and center it on the screen
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width/2) - (WINDOW_WIDTH/2))
    y = int((screen_height/2) - (WINDOW_HEIGHT/2))
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def configure_window(root):
    # Set the background color
    root.configure(bg='#D4D4D4')


def create_frame(root):
    # Create a frame to hold the label, spinbox, and button
    frame = tk.Frame(root, bg='#D4D4D4')
    frame.pack(pady=20, padx=20)
    return frame


def create_widgets(frame):
    # Create the label, spinbox, and button widgets
    font = ("Arial", 14)
    label, length_spinbox, strength_label = create_label_spinbox_strength_label(
        frame, font)
    button_frame = create_button_frame(frame)
    create_generate_password_button(
        button_frame, font, label, length_spinbox, strength_label)
    create_copy_and_clear_buttons(button_frame, font, label)


def create_label_spinbox_strength_label(frame, font):
    # Create a label widget
    label = tk.Label(frame, text="Click the button to generate a password",
                     font=font, bg='#D4D4D4', wraplength=500)
    label.pack(pady=10)

    # Create a spinbox widget to select the password length
    length_label = tk.Label(
        frame, text="Password Length", font=font, bg='#D4D4D4')
    length_label.pack()
    length_spinbox = tk.Spinbox(frame, from_=8, to=48, font=font, width=4)
    length_spinbox.pack()

    strength_label = tk.Label(frame, text="", font=font, bg='#D4D4D4')
    strength_label.pack(pady=10)

    return label, length_spinbox, strength_label


def create_button_frame(frame):
    # Create a frame to hold the buttons
    button_frame = tk.Frame(frame, bg='#D4D4D4')
    button_frame.pack(pady=10)
    return button_frame


def create_generate_password_button(frame, font, label, length_spinbox, strength_label):
    # Create a button to generate the password
    style = ttk.Style()
    style.configure('Custom.TButton', font=font)
    button = ttk.Button(frame, text="Generate Password", style='Custom.TButton',
                        command=lambda: generate_password(label, length_spinbox, strength_label))
    button.pack(side='left', padx=10)


def create_copy_and_clear_buttons(frame, font, label):
    # Create a button to copy the password to the clipboard
    copy_button = ttk.Button(frame, text="Copy to Clipboard", style='Custom.TButton', command=lambda: [
                             pyperclip.copy(label.cget("text")), clear_password(label)])
    copy_button.pack(side='left', padx=10)

    # Create a button to clear the clipboard
    clear_button = ttk.Button(
        frame, text="Clear Clipboard", style='Custom.TButton', command=clear_clipboard)
    clear_button.pack(side='left', padx=10)


def generate_password(label, length_spinbox, strength_label):
    # This function generates a password, updates the label widget, and copies the password to the clipboard

    password_length = int(length_spinbox.get())
    password = password_utils.create_valid_password(password_length)

    score, strength = password_utils.get_password_strength(password)
    encrypted_password = password_utils.encrypt_password(password)

    pyperclip.copy(encrypted_password.decode())
    update_labels(label, strength_label, password, strength)


def update_labels(label, strength_label, password, strength):
    label.config(text=password)
    strength_label.config(text=strength)


def clear_password(label):
    # This function clears the password from the label widget

    password = label.cget("text")
    password_utils.overwrite_password_with_random_data(password)
    label.config(text="Password deleted after copy for security purposes.")


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
