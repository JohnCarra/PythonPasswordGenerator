import random
import string
import tkinter as tk

# Create the GUI window
root = tk.Tk()
root.title("Password Generator")

# Define the font
font = ("Arial", 14)

# Create a frame to hold the label and button
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a label widget
label = tk.Label(
    frame, text="Click the button to generate a password", font=font)
label.pack(pady=10)

# Create a function to generate a random password


def generate_password():
    # Define the password length
    password_length = 16

    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = ''.join(random.choice(characters)
                       for i in range(password_length))

    # Update the label text with the generated password
    label.config(text=password)


# Create a button to generate the password
button = tk.Button(frame, text="Generate Password", font=font, bg="#1E90FF", fg="white", activebackground="#007FFF",
                   activeforeground="white", bd=0, padx=10, pady=5, relief="groove", command=generate_password)
button.pack()

# Set the window size and center it on the screen
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Start the GUI event loop
root.mainloop()
