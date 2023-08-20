import hashlib
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter import ttk
import csv
import random

# Frontend & Backend implementation
class Inventory:
    def __init__(self):
        pass
class LoginPage(tk.Frame):
    def __init__(self, parent, inventory):
        super().__init__(parent)
        self.inventory = inventory
        self.parent = parent
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):

        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self, textvariable=self.username_var)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        # Add your authentication logic here
        if username == "admin" and password == "password":
            self.parent.show_front_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class FrontPage(tk.Frame):
    def __init__(self, parent, inventory):
        super().__init__(parent)
        self.inventory = inventory
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        add_button = tk.Button(self, text="Add product", command=self.add_product)
        add_button.pack(padx=5, pady=5)

        remove_button = tk.Button(self, text="Remove product", command=self.remove_product)
        remove_button.pack(padx=5, pady=5)

        search_button = tk.Button(self, text="Search product", command=self.search_product)
        search_button.pack(padx=5, pady=5)

        list_button = tk.Button(self, text="List all products", command=self.list_products)
        list_button.pack(padx=5, pady=5)

        exit_button = tk.Button(self, text="Exit", command=self.parent.quit)
        exit_button.pack(padx=5, pady=5)

    def add_product(self):
        add_product_window = tk.Toplevel(self)
        add_product_window.title("Add Product")
        add_product_window.geometry("300x200")

        name_label = tk.Label(add_product_window, text="Product Name:")
        name_label.pack(padx=5, pady=5)
        name_entry = tk.Entry(add_product_window)
        name_entry.pack(padx=5, pady=5)

        price_label = tk.Label(add_product_window, text="Product Price:")
        price_label.pack(padx=5, pady=5)
        price_entry = tk.Entry(add_product_window)
        price_entry.pack(padx=5, pady=5)

        quantity_label = tk.Label(add_product_window, text="Product Quantity:")
        quantity_label.pack(padx=5, pady=5)
        quantity_entry = tk.Entry(add_product_window)
        quantity_entry.pack(padx=5, pady=5)

        add_button = tk.Button(add_product_window, text="Add", command=lambda: self.add_product_confirm(
            name_entry.get(), float(price_entry.get()), int(quantity_entry.get()), add_product_window))
        add_button.pack(padx=5, pady=5)

    def add_product_confirm(self, name, price, quantity, window):
        #check
        flag = 0
        with open('shop.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for element in row:
                    if element == name:
                        flag = 1
        if flag == 1:
            def update_newlist(j):
                with open('shop.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(j)

            new_list = []

            with open('shop.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    new_list.append(row)
                    for element in row:
                        if element == name:
                            data = [row[0], name, price, quantity,row[4]]
                            index = new_list.index(row)
                            new_list[index] = data

            update_newlist(new_list)
            messagebox.showinfo("Success", "Product updated successfully!")
            window.destroy()
        else:
            getpid = random.randint(0, 10000)
            hashno = hashlib.md5(str(name).encode()).hexdigest()
            product = [getpid, name, price, quantity,hashno]
            #add
            with open('shop.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(product)
            messagebox.showinfo("Success", "Product added successfully!")
            window.destroy()

    def remove_product(self):
        remove_product_window = tk.Toplevel(self)
        remove_product_window.title("Remove Product")
        remove_product_window.geometry("300x100")

        name_label = tk.Label(remove_product_window, text="Product Name to Remove:")
        name_label.pack(padx=5, pady=5)
        name_entry = tk.Entry(remove_product_window)
        name_entry.pack(padx=5, pady=5)

        remove_button = tk.Button(remove_product_window, text="Remove", command=lambda: self.remove_product_confirm(
            name_entry.get(), remove_product_window))
        remove_button.pack(padx=5, pady=5)

    def remove_product_confirm(self, name, window):
        #self.inventory.remove_product(name)
        def save(j):
            with open('shop.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(j)

        new_list = []
        with open('shop.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                new_list.append(row)

                for element in row:
                    if element == name:
                        new_list.remove(row)
        save(new_list)
        messagebox.showinfo("Success", "Product removed successfully!")
        window.destroy()

    def search_product(self):
        search_product_window = tk.Toplevel(self)
        search_product_window.title("Search Product")
        search_product_window.geometry("300x100")

        name_label = tk.Label(search_product_window, text="Product Name to Search:")
        name_label.pack(padx=5, pady=5)
        name_entry = tk.Entry(search_product_window)
        name_entry.pack(padx=5, pady=5)

        search_button = tk.Button(search_product_window, text="Search", command=lambda: self.search_product_confirm(
            name_entry.get(), search_product_window))
        search_button.pack(padx=5, pady=5)

    def search_product_confirm(self, name, window):
        data = []
        with open('shop.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for element in row:
                    if (element == name):
                        data.append(row)
        if data == []:
            messagebox.showinfo("Error", "No Data Found!")
            window.destroy()
        else:
            product_list_window = tk.Toplevel(self)
            product_list_window.title("Product List")
            product_list_window.geometry("400x400")

            product_list_label = tk.Label(product_list_window, text="List of Products:")
            product_list_label.pack(padx=5, pady=5)

            product_list_frame = Frame(product_list_window)
            product_list_frame.place(x=0, y=50, width=400, height=350)

            scroll_x = ttk.Scrollbar(product_list_frame, orient=HORIZONTAL)
            scroll_y = ttk.Scrollbar(product_list_frame, orient=VERTICAL)

            product_list = ttk.Treeview(product_list_frame, column=("ProductID","Name", "Price", "Quantity","HashCode"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)

            scroll_x.config(command=product_list.xview)
            scroll_y.config(command=product_list.yview)

            product_list.heading("ProductID", text="ProductID")
            product_list.heading("Name", text="Name")
            product_list.heading("Price", text="Price")
            product_list.heading("Quantity", text="Quantity")
            product_list.heading("HashCode", text="HashCode")

            product_list["show"] = "headings"

            product_list.column("ProductID", width=100)
            product_list.column("Name", width=100)
            product_list.column("Price", width=100)
            product_list.column("Quantity", width=100)
            product_list.column("HashCode", width=150)

            product_list.pack(fill=BOTH, side=TOP)
            product_list.delete(*product_list.get_children())
            for i in data:
                product_list.insert("", END, values=i)
            window.destroy()

    def list_products(self):
        product_list_window = tk.Toplevel(self)
        product_list_window.title("Product List")
        product_list_window.geometry("400x400")

        product_list_label = tk.Label(product_list_window, text="List of Products:")
        product_list_label.pack(padx=5, pady=5)

        product_list_frame =Frame(product_list_window)
        product_list_frame.place(x=0,y=50,width=400,height=350)

        scroll_x = ttk.Scrollbar(product_list_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(product_list_frame, orient=VERTICAL)

        product_list = ttk.Treeview(product_list_frame,column=("ProductID","Name","Price","Quantity","HashCode"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=product_list.xview)
        scroll_y.config(command=product_list.yview)

        product_list.heading("ProductID", text="ProductID")
        product_list.heading("Name",text="Name")
        product_list.heading("Price",text="Price")
        product_list.heading("Quantity",text="Quantity")
        product_list.heading("HashCode", text="HashCode")

        product_list["show"] = "headings"

        product_list.column("ProductID", width=100)
        product_list.column("Name",width=100)
        product_list.column("Price",width=100)
        product_list.column("Quantity",width=100)
        product_list.column("HashCode", width=150)

        product_list.pack(fill=BOTH, side = TOP)
        data = []

        with open('shop.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        product_list.delete(*product_list.get_children())
        for i in data:
            product_list.insert("", END, values=i)


class Application(tk.Tk):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory
        self.title("Online Shopping Management System")
        self.geometry("300x200+200+200")
        '''''''''
        frame = Frame(self, width=500, height=300)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)
        img = ImageTk.PhotoImage(Image.open("login.png"))
        label = Label(frame, image=img)
        label.pack()
        self.mainloop()
        '''''
        self.login_page = LoginPage(self, self.inventory)
        self.front_page = FrontPage(self, self.inventory)
        self.login_page.pack()


    def show_front_page(self):
        self.login_page.pack_forget()
        self.front_page.pack()

if __name__ == "__main__":
    inventory = Inventory()
    app = Application(inventory)
    app.mainloop()
