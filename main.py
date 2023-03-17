import random
import string
import tkinter as tk

# Create the GUI window
root = tk.Tk()
root.title("Password Generator")

# Create a label widget
label = tk.Label(root, text="Generate a Password", font=("Arial", 14))
label.pack(pady=10)

# Create a function to generate a random password


def generate_password():
    # Define the password length
    password_length = 12

    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password
    password = ''.join(random.choice(characters)
                       for i in range(password_length))

    # Update the label text with the generated password
    label.config(text=password)


# Create a button to generate the password
button = tk.Button(root, text="Generate", command=generate_password)
button.pack()

# Start the GUI event loop
root.mainloop()
