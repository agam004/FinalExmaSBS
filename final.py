# Name - Guragampreet Singh
# Student Number - 8913870
# Date - 04/16/2025
import psycopg2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


DB_NAME = "Customer Orders Management System"
DB_USER = "Customer Orders Management System_owner"
DB_PASSWORD = "npg_mkILy7YStWj4"
DB_HOST = "ep-floral-truth-a4ws76ib-pooler.us-east-1.aws.neon.tech"

def PopulateOrders():#refreshing table data in after operations and start
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()
        
        
        cur.execute("""
            SELECT * FROM orders
        """)#Get all data from database
        ordersFetched = cur.fetchall()
        
        cur.close()
        conn.close()
        for item in recordtable.get_children():
            recordtable.delete(item)#remove all old data

        for item in ordersFetched:
            recordtable.insert("",tk.END,values=item)#add new data 
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating table: {str(e)}")

#empty all input fields
def ClearInput():
    nameInput.delete(0,tk.END)
    productInput.delete(0,tk.END)
    quantityInput.delete(0,tk.END)
    priceInput.delete(0,tk.END)

def CreateTable():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()
        
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                product VARCHAR(100) NOT NULL,
                quantity INT NOT NULL DEFAULT 1 CHECK (quantity >= 0),
                price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
                order_date TIMESTAMP NOT NULL DEFAULT NOW());
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating table: {str(e)}")
        print(e)
        return


def CreateOrder():
    #Get data from entries and save as strings
    Customer_Name = nameInput.get().strip()
    Product_Name = productInput.get().strip()
    Quantity_Str = quantityInput.get().strip()
    Price_Str = priceInput.get().strip()


    if not Customer_Name or not Product_Name or not Quantity_Str or not Price_Str:  
        messagebox.showerror("Error", "Must Fill Values in All fields!")
        return

    try:
        #Convert Quantity and Price to int and float
        Quantity = int(Quantity_Str)
        Price = float(Price_Str)
        if(Quantity<=0 or Price<=0):#check if both are not 0
            messagebox.showerror("Error","Quantity and Price must be a positive value!!!")
            return
    except:
        messagebox.showerror("Error","Price or quauntity value must be number")
        return

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()

       #Get all the validated data and save to database 
        cur.execute("INSERT INTO orders (customer_name,product,quantity,price) VALUES (%s,%s,%s,%s)", (Customer_Name,Product_Name,Quantity,Price))
        conn.commit()  

        messagebox.showinfo("Success", f"Order for '{Customer_Name}' added successfully!")
        ClearInput() #clear all inputs
        PopulateOrders() #refrsh UI table data
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))



#creating root window
root = tk.Tk()
root.title("Customer Order Management System")
root.geometry("600x600")
CreateTable()
#adding basic UI Elements(Labels, Inputs, treeview,etc.)
titleLabel = tk.Label(root,text="Orders Management",font=("default",26))
titleLabel.pack()

nameLbl = tk.Label(root, text="Customer Name:")
nameLbl.place(x=50,y=100)
nameInput = tk.Entry(root)
nameInput.place(x=200,y=100)

productLbl = tk.Label(root,text="Product Name:")
productLbl.place(x=50,y=125)
productInput = tk.Entry(root)
productInput.place(x=200,y=125)

quantityLbl = tk.Label(root,text="Quantity :")
quantityLbl.place(x=50,y=150)
quantityInput = tk.Entry(root)
quantityInput.place(x=200,y=150)

priceLbl = tk.Label(root,text="Price :")
priceLbl.place(x=50,y=175)
priceInput = tk.Entry(root)
priceInput.place(x=200,y=175)

createOrderBtn = ttk.Button(root,text="Create New Order",command=CreateOrder)
createOrderBtn.place(x=100,y=200)

clearFieldsBtn = ttk.Button(root,text="Clear Inputs",command=ClearInput)
clearFieldsBtn.place(x=210,y=200)
recordtable = ttk.Treeview(root,columns=("Id","Customer Name","Product Name","Quantity","Price","Order Date"),show="headings")
recordtable.heading("Id",text="Id")
recordtable.column("Id", width=50,anchor=tk.CENTER)
recordtable.heading("Customer Name", text="Customer Name")
recordtable.column("Customer Name", width=150, anchor=tk.CENTER)
recordtable.heading("Product Name", text="Product Name")
recordtable.column("Product Name", width=120, anchor=tk.CENTER)
recordtable.heading("Quantity", text="Quantity")
recordtable.column("Quantity", width=80, anchor=tk.CENTER)
recordtable.heading("Price", text="Price")
recordtable.column("Price", width=80, anchor=tk.CENTER)
recordtable.heading("Order Date", text="Order Date")
recordtable.column("Order Date", width=100, anchor=tk.CENTER)
recordtable.place(x=10,y=250)

#Add db data in tree
PopulateOrders()

#keep main screen open
root.mainloop()