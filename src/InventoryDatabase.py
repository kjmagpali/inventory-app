from InventoryEntry import InventoryEntry
import csv
import json

class InventoryDatabase:

    def __init__(self, init = False, dbName = 'PDM_Inventory.db'):
        self.dbName = dbName
        self.csv_file = 'PDM_Inventory_CSV.csv'
        self.json_file = 'PDM_Inventory_JSON.json'

        self.entries = []
        print('Initialization Complete.')
    
    def fetch_inventory(self, code, item, category, stock, price):
        print('\nFetch Inventory')
        inventory_list = [(entry.code, entry.item, entry.category, entry.stock, entry.price) for entry in self.entries]
        return inventory_list
    
    def insert_item(self, code, item, category, stock, price):
        new_item = InventoryEntry(code = code, item = item, category = category, stock = stock, price = price)
        self.entries.append(new_item)
        print('PDM Inventory System: Item successfully added.')
    
    def delete_item(self, code):
        for entry in self.entries:
            if entry.code == code:
                self.entries.remove(entry)
                break
        print('PDM Inventory System: Item successfully removed.')
    
    def update_item(self, new_item, new_category, new_stock, new_price, code):
        for entry in self.entries:
            if entry.code == code:
                entry.item = new_item
                entry.category = new_category
                entry.stock = new_stock
                entry.price = new_price
                break
        print('PDM Inventory System: Item successfully updated.')
    
    def export_csv(self):
        with open(self.csv_file, "w") as filehandle:
            for entry in self.entries:
                filehandle.write(f"{entry.code},{entry.item},{entry.category},{entry.stock},{entry.price}\n")
        print('PDM Inventory System: Successfully exported to CSV.')

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

        with open(self.json_file, "w") as filehandle:
            json.dump(entries_json, filehandle, indent=2)

        print('PDM Inventory System: Successfully exported to JSON.')

    def import_csv(self, csv_file):
        with open(csv_file, 'r') as filehandle:
            csv_reader = csv.reader(filehandle)
            for row in csv_reader:
                code, item, category, stock, price = map(str.strip, row)

                if not self.code_exists(code):
                    unit = InventoryEntry(code=code, item=item, category=category, stock=stock, price=price)
                    self.entries.append(unit)
                else:
                    print(f"Skipping import for code {code} as it already exists.")
                    
        print('PDM Inventory System: Successfully imported inventory data.')

    def code_exists(self, code):
        return any(entry.code == code for entry in self.entries)
