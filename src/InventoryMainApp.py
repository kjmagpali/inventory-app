from InventoryDatabase import InventoryDatabase
from InventoryGUI import InventoryGUI

def main():
    db = InventoryDatabase(init = False, dbName = 'PDM_Inventory.csv')
    app = InventoryGUI(dataBase = db)
    app.mainloop()

if __name__ == "__main__":
    main()
