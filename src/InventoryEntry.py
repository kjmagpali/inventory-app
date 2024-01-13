class InventoryEntry:
    def __init__(self,
                 code = 'PDM0001',
                 item = 'Item',
                 category = 'Category',
                 stock = 1,
                 price = 1.00):
        
        self.code = code
        self.item = item
        self.category = category
        self.stock = stock
        self.price = price
