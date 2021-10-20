import json
import tkinter as t
from tkinter import messagebox
import string
import random
import pyperclip
from cryptography.fernet import Fernet
import os

window = t.Tk()
window.title('Password Manager')
window.minsize(width=400, height=400)
window.config(padx=50, pady=50)


def write_key():
    curr_dir = os.path.dirname(__file__)
    path = os.path.join(curr_dir, "key.key")
    if not os.path.exists(path):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        print("key already created")

write_key()


def load_key():
    return open("key.key", "rb").read()


def encrypt(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def add():
    website_info = website_input.get()
    user_email_info = user_email_input.get()
    pwd_info = pwd_input.get()
    new_data = {
        website_info.title():
            {"email": user_email_info,
             "password": pwd_info}
    }

    if len(website_info) == 0 or len(user_email_info) == 0 or len(pwd_info) == 0:
        messagebox.showinfo(title='Fields validation', message='All fields must be filled-in')
    else:
        user_ok = messagebox.askokcancel(title="Do you confirm", message='Do you want to add that password?')
        if user_ok:
            try:
                decrypt('data.json')
                with open('data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                with open('data.json', 'w') as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
            finally:
                website_input.delete(0, t.END)
                pwd_input.delete(0, t.END)
                encrypt('data.json')


def generate():
    pwd_input.delete(0, t.END)
    result_pwd = pwd()
    pwd_input.insert(0, result_pwd)
    pyperclip.copy(result_pwd)


def pwd():
    pwd_generated = [random.choice(string.ascii_letters + string.punctuation + string.digits) for i in range(15)]
    new_pwd = "".join(pwd_generated)
    return new_pwd


def search():
    if len(website_input.get()) == 0:
        messagebox.showinfo(title='Website empty', message='Please, enter a website name')
    else:
        try:
            decrypt('data.json')
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showinfo(title='No password saved', message='No password saved')
        except json.JSONDecodeError:
            # messagebox.showinfo(title='Empty file', message='Empty File / no {}')
            with open('data.json', 'w') as f:
                json.dump({}, f, indent=4)
        else:
            if website_input.get().title() in data:
                pwd_from_file = data[website_input.get().title()]['password']
                messagebox.showinfo(title="You password details",message=f"Username: {data[website_input.get().title()]['email']}\nPassword: {pwd_from_file}")
            else:
                messagebox.showinfo(title='No password found', message=f"No password found for {website_input.get().title()}")
            encrypt('data.json')
            # OTHER WAY --> mais plus long
            # found = 0
            # for (key, value) in data.items():
            #     if key == website_input.get():
            #         found =1
            #         messagebox.showinfo(title="You password details", message=f"Username: {data[key]['email']}\nPassword: {data[key]['password']}")
            # if found ==0:
            #     messagebox.showinfo(title='No password found', message='No password found')


# Image
canvas = t.Canvas(width=200, height=200)
image = t.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website_label = t.Label(text='Website:')
website_label.grid(column=0, row=1)

user_email_label = t.Label(text='Username:')
user_email_label.grid(column=0, row=2)

pwd_label = t.Label(text='Pwd:')
pwd_label.grid(column=0, row=3)

# Inputs
website_input = t.Entry(width=22)
website_input.grid(column=1, row=1)
website_input.focus()

user_email_input = t.Entry(width=35)
user_email_input.grid(column=1, row=2, columnspan=2)
user_email_input.insert(0, 'myemail@yopmail.com')

pwd_input = t.Entry(width=22)
pwd_input.grid(column=1, row=3)

# Buttons
generate_button = t.Button(text='Generate', command=generate, width=12)
generate_button.grid(column=2, row=3)

add_button = t.Button(text='Add', command=add, width=36)
add_button.grid(column=1, row=4, columnspan=2)

search_button = t.Button(text='Search', command=search, width=12)
search_button.grid(column=2, row=1, columnspan=2)


window.mainloop()
