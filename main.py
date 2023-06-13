from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password_entry.delete(0, END)
    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list1 = [random.choice(letters) for _ in range(nr_letters)]
    password_list2 = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list3 = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_list2 + password_list1 + password_list3
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_entry():
    password = password_entry.get()
    website = website_entry.get().title()
    username = username_entry.get()
    dict = {
        website: {
            'Email': username,
            'Password': password
        }
    }

    if len(password) == 0 or len(website) == 0 or len(username) == 0:
        messagebox.showerror(message='Field left empty!')
    elif messagebox.askokcancel(title=website, message=f'Confirm details:\nEmail: {username}\nPassword: {password}'):
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                data.update(dict)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump(dict, file)
        else:
            with open('data.json', 'w') as file1:
                json.dump(data, file1, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ---------------------------- Search Functionality ------------------------------- #


def search_entry():
    website = website_entry.get().title()
    # print(website)  # Check
    try:
        with open('data.json') as file:
            data = json.load(file)
            email = data[website]['Email']
            password = data[website]['Password']
    except KeyError:
        messagebox.showerror(message=f'Cant find the data for website input')
    except FileNotFoundError:
        messagebox.showerror(message='The data file has not yet been created, please add data to the data file')
    else:
        messagebox.showinfo(message=f'Email: {email}\nPassword:{password}')
    finally:
        website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=300, height=300)
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# All Labels
website_label = Label(text="Website :")
website_label.grid(column=0, row=1)

username_label = Label(text='Email / Username :')
username_label.grid(column=0, row=2)

password_label = Label(text='Password :')
password_label.grid(column=0, row=3)

# All Entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = Entry(width=35)
username_entry.insert(0, '<Your-Email>@example.com')
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# All Buttons
generate_password = Button(text="Generate",  width=10, command=password_generator)
generate_password.grid(column=2, row=3)

add_entry = Button(text='Add', width=33, command=save_entry)
add_entry.grid(column=1, row=4, columnspan=2)

search = Button(text='Search', width=10, command=search_entry)
search.grid(column=2, row=1)

window.mainloop()
