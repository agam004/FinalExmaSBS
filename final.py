# Name - Guragampreet Singh
# Student Number - 8913870
# Date - 04/16/2025
from ast import Delete
import tkinter as tk
import psycopg2
from tkinter import messagebox
from tkinter import ttk


DB_NAME = "Customer%20Orders%20Management%20System"
DB_USER = "Customer%20Orders%20Management%20System_owner"
DB_PASSWORD = "npg_mkILy7YStWj4"
DB_HOST = "ep-floral-truth-a4ws76ib-pooler.us-east-1.aws.neon.tech"

root = tk.Tk()
root.title("Customer Order Management System")
root.geometry("600x600")
root.mainloop()