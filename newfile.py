import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

# ---------- Database Connection ----------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vehicle_service"
    )

# ---------- Main Menu ----------

def open_main_menu():
    home = tk.Tk()
    home.title("Home - Vehicle Service Center")
    home.geometry("400x350")
    home.configure(bg="#E8F8F5")

    tk.Label(home, text="Welcome to Vehicle Service Center", bg="#E8F8F5", font=('Arial', 14, 'bold')).pack(pady=20)
    tk.Button(home, text="Add Customer", width=25, bg="#AED6F1", command=lambda: [home.destroy(), open_main_ui()]).pack(pady=5)
    tk.Button(home, text="Vehicle in Service", width=25, bg="#A3E4D7", command=lambda: [home.destroy(), vehicle_in_service_module()]).pack(pady=5)
    tk.Button(home, text="Customers", width=25, bg="#F9E79F", command=lambda: [home.destroy(), show_database_window()]).pack(pady=5)
    tk.Button(home, text="Inventory", width=25, bg="#F5B7B1", command=lambda: [home.destroy(), open_inventory_module()]).pack(pady=5)
    tk.Button(home, text="Exit", width=25, bg="#F1948A", command=home.quit).pack(pady=20)

    home.mainloop()

# ---------- Add Customer Module ----------

def insert_record():
    name = name_entry.get()
    vehicle = vehicle_entry.get()
    service = service_entry.get()
    cost = cost_entry.get()

    if not (name and vehicle and service and cost):
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO services (customer_name, vehicle_model, service_type, cost) VALUES (%s, %s, %s, %s)", (name, vehicle, service, cost))
        cursor.execute("INSERT INTO vehicles_in_service (customer_name, vehicle_model, problem_description, service_status) VALUES (%s, %s, %s, %s)", (name, vehicle, service, "In Progress"))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Customer added and vehicle marked 'In Service'.")
        clear_entries()
        vehicle_in_service_module()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_database_window():
    win = tk.Toplevel()
    win.title("Service Records")
    win.geometry("650x400")
    win.configure(bg="#E6F0FA")

    tree = ttk.Treeview(win, columns=("ID", "Name", "Vehicle", "Service", "Cost"), show='headings')
    for col in ("ID", "Name", "Vehicle", "Service", "Cost"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM services")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)
    db.close()

    tk.Button(win, text="Main Menu", command=lambda: [win.destroy(), open_main_menu()]).pack(pady=10)

def show_chart():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT service_type, SUM(cost) FROM services GROUP BY service_type")
    data = cursor.fetchall()
    db.close()

    service_types = [row[0] for row in data]
    total_costs = [row[1] for row in data]

    plt.figure(figsize=(8, 5))
    plt.bar(service_types, total_costs, color='skyblue')
    plt.xlabel("Service Type")
    plt.ylabel("Total Cost")
    plt.title("Service Costs by Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def search_record():
    name = search_entry.get()
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM services WHERE customer_name LIKE %s", ("%" + name + "%",))
    rows = cursor.fetchall()
    db.close()

    results_window = tk.Toplevel()
    results_window.title("Search Results")
    results_window.geometry("650x300")
    results_window.configure(bg="#E6F0FA")

    tree = ttk.Treeview(results_window, columns=("ID", "Name", "Vehicle", "Service", "Cost"), show='headings')
    for col in ("ID", "Name", "Vehicle", "Service", "Cost"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    for row in rows:
        tree.insert('', tk.END, values=row)

def clear_entries():
    name_entry.delete(0, tk.END)
    vehicle_entry.delete(0, tk.END)
    service_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)

def open_main_ui():
    global name_entry, vehicle_entry, service_entry, cost_entry, search_entry

    root = tk.Tk()
    root.title("Add Customer - Vehicle Service Center")
    root.geometry("700x500")
    root.configure(bg="#E6F0FA")

    tk.Label(root, text="Customer Name", bg="#E6F0FA").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(root, text="Vehicle Model", bg="#E6F0FA").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(root, text="Service Type", bg="#E6F0FA").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(root, text="Cost", bg="#E6F0FA").grid(row=3, column=0, padx=10, pady=10)

    name_entry = tk.Entry(root)
    vehicle_entry = tk.Entry(root)
    service_entry = tk.Entry(root)
    cost_entry = tk.Entry(root)

    name_entry.grid(row=0, column=1)
    vehicle_entry.grid(row=1, column=1)
    service_entry.grid(row=2, column=1)
    cost_entry.grid(row=3, column=1)

    tk.Button(root, text="Insert Record", bg="#5DADE2", command=insert_record).grid(row=4, column=1, pady=10)
    tk.Button(root, text="Show Cost Chart", bg="#58D68D", command=show_chart).grid(row=5, column=1, pady=10)
    tk.Button(root, text="Show All Records", bg="#F5B041", command=show_database_window).grid(row=6, column=1, pady=10)

    tk.Label(root, text="Search by Customer Name:", bg="#E6F0FA").grid(row=7, column=0, pady=10)
    search_entry = tk.Entry(root)
    search_entry.grid(row=7, column=1)
    tk.Button(root, text="Search", bg="#AF7AC5", command=search_record).grid(row=7, column=2, padx=10)

    tk.Button(root, text="Main Menu", command=lambda: [root.destroy(), open_main_menu()]).grid(row=8, column=1, pady=20)

    root.mainloop()

# ---------- Vehicle in Service Module ----------

def vehicle_in_service_module():
    win = tk.Tk()
    win.title("Vehicle in Service")
    win.geometry("750x400")
    win.configure(bg="#F2F4F4")

    def fetch_service_data():
        for row in tree.get_children():
            tree.delete(row)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM vehicles_in_service")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        db.close()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a record to remove")
            return
        db = connect_db()
        cursor = db.cursor()
        for sel in selected:
            row = tree.item(sel)['values']
            cursor.execute("DELETE FROM vehicles_in_service WHERE id = %s", (row[0],))
        db.commit()
        db.close()
        fetch_service_data()

    tree = ttk.Treeview(win, columns=("ID", "Name", "Model", "Problem", "Status"), show='headings')
    for col in ("ID", "Name", "Model", "Problem", "Status"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(win, text="Remove Selected", bg="#F1948A", command=delete_selected).pack(pady=10)
    tk.Button(win, text="Main Menu", command=lambda: [win.destroy(), open_main_menu()]).pack(pady=10)

    fetch_service_data()

# ---------- Inventory Module ----------

def open_inventory_module():
    win = tk.Tk()
    win.title("Inventory Management")
    win.geometry("700x400")
    win.configure(bg="#FAFAD2")

    def fetch_inventory():
        for row in tree.get_children():
            tree.delete(row)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        db.close()

    def add_inventory():
        item = item_entry.get()
        quantity = quantity_entry.get()
        if not (item and quantity):
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO inventory (item_name, quantity) VALUES (%s, %s)", (item, quantity))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Inventory item added.")
            item_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            fetch_inventory()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_inventory():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select an item to delete")
            return
        db = connect_db()
        cursor = db.cursor()
        for sel in selected:
            row = tree.item(sel)['values']
            cursor.execute("DELETE FROM inventory WHERE id = %s", (row[0],))
        db.commit()
        db.close()
        fetch_inventory()

    tk.Label(win, text="Item Name", bg="#FAFAD2").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(win, text="Quantity", bg="#FAFAD2").grid(row=1, column=0, padx=10, pady=10)

    item_entry = tk.Entry(win)
    quantity_entry = tk.Entry(win)
    item_entry.grid(row=0, column=1)
    quantity_entry.grid(row=1, column=1)

    tk.Button(win, text="Add Item", bg="#90EE90", command=add_inventory).grid(row=2, column=1, pady=10)
    tk.Button(win, text="Delete Selected", bg="#FFB6C1", command=delete_inventory).grid(row=3, column=1, pady=10)

    tree = ttk.Treeview(win, columns=("ID", "Item", "Quantity"), show='headings')
    for col in ("ID", "Item", "Quantity"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    tk.Button(win, text="Main Menu", command=lambda: [win.destroy(), open_main_menu()]).grid(row=5, column=1, pady=10)

    fetch_inventory()

# ---------- Login Window ----------

login_window = tk.Tk()
login_window.title("Login - Vehicle Service Center")
login_window.geometry("300x200")
login_window.configure(bg="#D6EAF8")

username_entry = tk.Entry(login_window)
password_entry = tk.Entry(login_window, show="*")

tk.Label(login_window, text="Username:", bg="#D6EAF8").pack(pady=10)
username_entry.pack()
tk.Label(login_window, text="Password:", bg="#D6EAF8").pack(pady=10)
password_entry.pack()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "a" and password == "a":
        login_window.destroy()
        open_main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

tk.Button(login_window, text="Login", command=login, bg="#5DADE2").pack(pady=20)

login_window.mainloop()
