import random
import pyperclip
from tkinter import *
from tkinter import messagebox
import json

# ---------------------------- CONSTANTS ------------------------#
PURPLE = "#C4D3F3"
RED = "#E93A37"
MAROON = "#75031F"
DARK_PURPLE = "#9CA5D1"
ENTRY_BG="#E8E9F7"
FONT="Comic Sans MS"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list += password_letter + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data={
        website:{
            "email":email,
            "password":password,
        }

    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Incomplete Information", message="All data fields are required")
    else:
        try:
            with open("data.json","r") as data_file:
                #Reading Old data
                data=json.load(data_file)
        except FileNotFoundError:
            with open("data.json","w") as data_file:
                json.dump(new_data,data_file,indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saves the updated data to json file
                json.dump(data,data_file,indent=4)
        finally:
                website_input.delete(0, END)
                password_input.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo()
    else:
        if website in data:
            email= data[website]["email"]
            password =data[website]["password"]
            messagebox.showinfo(title=f"{website}",message=f"Email/Username:{email}\nPassword:{password}")
        else:
            messagebox.showerror(title="Error",message=f"No data found for {website}")
    finally:
        website_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg=PURPLE)

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0, bg=PURPLE)
logo_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=0, row=0, columnspan=3, pady=20)

# Labels
website_label = Label(text="Website 🌐 :", bg=PURPLE,font=(FONT,12))
website_label.grid(column=0, row=1, sticky="E", padx=10, pady=5)

email_label = Label(text="Email 📧/Username 👤 :", bg=PURPLE , font=(FONT,12))
email_label.grid(column=0, row=2, sticky="E", padx=10, pady=5)

password_label = Label(text="Password 🔑:", bg=PURPLE , font=(FONT,12))
password_label.grid(column=0, row=3, sticky="E", padx=10, pady=5)

# Entry Fields
website_input = Entry(width=35,bg=ENTRY_BG,font=(FONT,12))
website_input.grid(column=1, row=1,sticky="EW", padx=10)

email_input = Entry(width=35,bg=ENTRY_BG,font=(FONT,12))
email_input.grid(column=1, row=2, columnspan=2, sticky="EW", padx=10)
email_input.insert(0, "xyx@abc.com")

password_input = Entry(width=25,bg=ENTRY_BG,font=(FONT,12))
password_input.grid(column=1, row=3, sticky="EW", padx=10)

# Buttons
Search_button = Button(text="Search", width=15, command=find_password,bg="#FF9F43", fg="black",font=(FONT,12))
Search_button.grid(column=2, row=1, sticky="W", padx=10)

generate_password_button = Button(text="Generate Password", width=15, command=generate_password, bg="#FFC107", fg="black" ,font=(FONT,12))
generate_password_button.grid(column=2, row=3, sticky="W", padx=10)

add_password_button = Button(text="ADD", width=36, command=save, bg=RED, fg="white",font=('Montserrat',12,'bold'))
add_password_button.grid(column=1, row=4, columnspan=2, sticky="EW", pady=10, padx=10)

# Configure grid weights for dynamic resizing
window.grid_columnconfigure(1, weight=1)

window.mainloop()