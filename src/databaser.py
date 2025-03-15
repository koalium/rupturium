import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import os
import csv
import random

class Database:
    def __init__(self, db_name):
        # Ensure the database exists in the current directory
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.import_csv_if_exists()

    def create_table(self):
        # Create the 'tested' table with the specified schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tested (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type VARCHAR(15),
                size VARCHAR(8),
                layers VARCHAR(127),
                bp VARCHAR(15),
                bt VARCHAR(7),
                rbp VARCHAR(7),
                fh VARCHAR(15),
                drw VARCHAR(63)
            )
        ''')
        self.conn.commit()

    def import_csv_if_exists(self):
        # Check if 'results.csv' exists in the current directory
        csv_path = os.path.join(os.getcwd(), 'results.csv')
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row
                    for row in reader:
                        # Ensure the row has the correct number of columns
                        if len(row) == 8:
                            self.cursor.execute('''
                                INSERT INTO tested (id,type, size, layers, bp, bt, rbp, fh, drw)
                                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', row)
                self.conn.commit()
                messagebox.showinfo("Success", "Data imported from results.csv successfully")
            except Exception as e:
                messagebox.showerror("CSV Import Error", str(e))
        else:
            messagebox.showwarning("CSV Not Found", "results.csv not found in the current directory")

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                sql_script = file.read()
            self.cursor.executescript(sql_script)
            self.conn.commit()
            messagebox.showinfo("Success", "SQL file executed successfully")
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))

    def find_nearest(self, size, type_, rbp):
        try:
            # Map type to its corresponding value
            type_map = {"1": "reverse", "2": "forward", "3": "flat"}
            type_ = type_map.get(type_, type_)

            # Cast size to integer (even though it's stored as VARCHAR)
            size = str(int(size))

            # Find nearest greater
            self.cursor.execute('''
                SELECT rbp FROM tested
                WHERE size = ? AND type = ? AND CAST(rbp AS REAL) > ?
                ORDER BY CAST(rbp AS REAL) ASC LIMIT 1
            ''', (size, type_, float(rbp)))
            greater = self.cursor.fetchone()

            # Find nearest lesser
            self.cursor.execute('''
                SELECT rbp FROM tested
                WHERE size = ? AND type = ? AND CAST(rbp AS REAL) < ?
                ORDER BY CAST(rbp AS REAL) DESC LIMIT 1
            ''', (size, type_, float(rbp)))
            lesser = self.cursor.fetchone()

            return (
                greater[0] if greater else None,
                lesser[0] if lesser else None
            )
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return None, None

    def get_random_rows(self, limit=10):
        try:
            self.cursor.execute('''
                SELECT * FROM tested
                ORDER BY RANDOM()
                LIMIT ?
            ''', (limit,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def add_entry(self, type_, size, layers, bp, bt, rbp, fh=None, drw=None):
        try:
            self.cursor.execute('''
                INSERT INTO tested (type, size, layers, bp, bt, rbp, fh, drw)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (type_, size, layers, bp, bt, rbp, fh, drw))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return False

    def __del__(self):
        self.conn.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rupturium DB Manager")
        self.db = Database('rupturium_db.db')
        self.create_widgets()

    def create_widgets(self):
        # Search Frame
        search_frame = tk.LabelFrame(self, text="Search Parameters")
        search_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(search_frame, text="Size:").grid(row=0, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(search_frame)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="Type (1=reverse, 2=forward, 3=flat):").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(search_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="RBP:").grid(row=2, column=0, padx=5, pady=5)
        self.rbp_entry = tk.Entry(search_frame)
        self.rbp_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Search", command=self.on_search).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add New Entry", command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Import SQL File", command=self.import_sql_file).pack(side=tk.LEFT, padx=5)

        # Results
        self.result_label = tk.Label(self, text="", font=('Arial', 10), justify=tk.LEFT)
        self.result_label.pack(pady=10)

    def on_search(self):
        try:
            size = self.size_entry.get()
            type_ = self.type_entry.get()
            rbp = self.rbp_entry.get()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values")
            return

        greater, lesser = self.db.find_nearest(size, type_, rbp)
        
        if greater is None and lesser is None:
            # No results found, show 10 random rows
            random_rows = self.db.get_random_rows(10)
            if random_rows:
                result_text = ["No matching results found. Showing 10 random rows:\n"]
                for row in random_rows:
                    result_text.append(f"ID: {row[0]}, Type: {row[1]}, Size: {row[2]}, Layers: {row[3]}, BP: {row[4]}, BT: {row[5]}, RBP: {row[6]}, FH: {row[7]}, DRW: {row[8]}")
                self.result_label.config(text="\n".join(result_text))
            else:
                self.result_label.config(text="No data available in the database.")
        else:
            result_text = []
            if greater is not None:
                result_text.append(f"Nearest greater RBP: {greater}")
            else:
                result_text.append("No greater RBP found")
            
            if lesser is not None:
                result_text.append(f"Nearest lesser RBP: {lesser}")
            else:
                result_text.append("No lesser RBP found")
            
            self.result_label.config(text="\n".join(result_text))

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add New Entry")

        # Form fields
        fields = [
            ("Type (VARCHAR 15):", "type"),
            ("Size (VARCHAR 8):", "size"),
            ("Layers (VARCHAR 127):", "layers"),
            ("BP (VARCHAR 15):", "bp"),
            ("BT (VARCHAR 7):", "bt"),
            ("RBP (VARCHAR 7):", "rbp"),
            ("FH (VARCHAR 15, optional):", "fh"),
            ("DRW (VARCHAR 63, optional):", "drw")
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry

        def submit_entry():
            try:
                # Get values from entries
                type_ = self.entries["type"].get()
                size = self.entries["size"].get()
                layers = self.entries["layers"].get()
                bp = self.entries["bp"].get()
                bt = self.entries["bt"].get()
                rbp = self.entries["rbp"].get()
                fh = self.entries["fh"].get() or None
                drw = self.entries["drw"].get() or None

                # Validate lengths
                if (len(type_) > 15 or len(size) > 8 or len(layers) > 127 or
                    (fh and len(fh) > 15) or (drw and len(drw) > 63)):
                    messagebox.showerror("Input Error", "Field lengths exceed maximum allowed")
                    return

                # Add entry to database
                if self.db.add_entry(type_, size, layers, bp, bt, rbp, fh, drw):
                    messagebox.showinfo("Success", "Entry added successfully")
                    add_window.destroy()
            except Exception as e:
                messagebox.showerror("Input Error", str(e))

        tk.Button(add_window, text="Submit", command=submit_entry).grid(row=len(fields), columnspan=2, pady=10)

    def import_sql_file(self):
        # Ask the user to select an SQL file
        file_path = filedialog.askopenfilename(
            title="Select SQL File",
            filetypes=[("SQL Files", "*.sql")]
        )

        if file_path:
            self.db.execute_sql_file(file_path)

if __name__ == "__main__":
    app = Application()
    app.mainloop()