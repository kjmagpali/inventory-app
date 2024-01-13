import sqlite3
import csv
import json

class InventorySQLite:
    def __init__(self, dbName = 'PDM_Inventory.db'):
        super().__init__()
        self.dbName = dbName
        self.csv_file = 'PDM_Inventory_CSV.csv'
        self.json_file = 'PDM_Inventory_JSON.json'
        self.connect = sqlite3.connect(self.dbName)
        self.cursor = self.connect.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                code TEXT PRIMARY KEY,
                item TEXT,
                category TEXT,
                stock TEXT,
                price TEXT)''')
        self.connect.commit()
        self.connect.close()
    
    def connect_cursor(self):
        self.connect = sqlite3.connect(self.dbName)
        self.cursor = self.connect.cursor()

    def commit_close(self):
        self.connect.commit()
        self.connect.close()

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                code TEXT PRIMARY KEY,
                item TEXT,
                category TEXT,
                stock TEXT,
                price TEXT)''')
        self.commit_close()

    def fetch_inventory(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Inventory')
        inventory = self.cursor.fetchall()
        self.connect.close()
        return inventory
    
    def insert_item(self, code, item, category, stock, price):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Inventory (code, item, category, stock, price) VALUES (?, ?, ?, ?, ?)',
                    (code, item, category, stock, price))
        self.commit_close()

    def delete_item(self, code):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Inventory WHERE code = ?', (code))
        self.commit_close()

    def update_item(self, new_item, new_category, new_stock, new_price, code):
        self.connect_cursor()
        self.cursor.execute('UPDATE Inventory SET item = ?, category = ?, stock = ?, price = ? WHERE code = ?',
                    (new_item, new_category, new_stock, new_price, code))
        self.commit_close()

    def code_exists(self, code):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Inventory WHERE code = ?', (code))
        result = self.cursor.fetchone()
        self.connect.close()
        return result[0] > 0
    
    def export_csv(self):
        with open(self.csv, "w") as filehandle:
            dbEntries = self.fetch_inventory()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]}, {entry[1]}, {entry[2]}, {entry[3]}, {entry[4]}\n")
    
    def export_json(self):
        entries_json = []

        for entry in self.entries:
            entry_data = {
                "Reference Code": entry.code,
                "Item": entry.item,
                "Category": entry.category,
                "Stock Availability": entry.stock,
                "Unit Price": entry.price,
            }
            entries_json.append(entry_data)

        with open(self.json, "w") as filehandle:
            json.dump(entries_json, filehandle, indent=2)

    def import_csv(self, csv_file):
        with open(csv_file, 'r') as filehandle:
            csv_reader = csv.reader(filehandle)
            for row in csv_reader:
                code, item, category, stock, price = map(str.strip, row)
                self.insert_item(code, item, category, stock, price)

#ADD TESTS
