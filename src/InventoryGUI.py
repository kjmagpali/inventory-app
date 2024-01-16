import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from InventorySQLite import InventorySQLite

class InventoryGUI(customtkinter.CTk):

    def __init__(self, dataBase = InventorySQLite('PDM_Inventory.db')):
        super().__init__()
        self.db = dataBase

        self.title('Pan de Manila Inventory System')
        self.geometry('1000x600')
        self.iconbitmap('pandemanila.ico')
        self.resizable(False, False)

        self.bg = PhotoImage(file = 'window.pbm')
        window_bg = Label(self, image = self.bg, borderwidth = 0)
        window_bg.place(x = 0, y = 0)

        self.logo = tk.PhotoImage(file = 'pdmlogo.png')
        logo = tk.Label(self, image = self.logo, borderwidth = 0)
        logo.place(x = 40, y = 40)

        self.font1 = ('Arial', 16, 'bold')
        self.font2 = ('Arial', 12)
        self.font3 = ('Arial', 16)
        self.font4 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'Reference Code' Label and Entry Widgets
        self.code_label = self.newCtkLabel('Reference Code')
        self.code_label.place(x = 30, y = 190)
        self.code_entry = self.codeCtkEntry()
        self.code_entry.place(x = 191, y = 190)

        # 'Item' Label and Entry Widgets
        self.item_label = self.newCtkLabel('Item Name')
        self.item_label.place(x = 30, y = 250)
        self.item_entry = self.itemCtkEntry()
        self.item_entry.place(x = 191, y = 250)

        # 'Category' Label and Combo Box Widgets
        self.category_label = self.newCtkLabel('Category')
        self.category_label.place(x = 30, y = 310)
        self.category_cboxVar = StringVar()
        self.category_cboxOptions = ['Beverage', 'Homegrown Spread', 'Ice Cream', 'Pantry Essential', 'Specialty Bread', 'Vegan']
        self.category_cbox = self.newCtkComboBox(options=self.category_cboxOptions, 
                                    entryVariable=self.category_cboxVar)
        self.category_cbox.place(x = 191, y = 310)

        # 'Stock Availability' Label and Combo Box Widgets
        self.stock_label = self.newCtkLabel('Stock Availability')
        self.stock_label.place(x = 30, y = 370)
        self.stock_entry = self.stockCtkEntry()
        self.stock_entry.place(x = 191, y = 370)

        # 'Unit Price' Label and Entry Widgets
        self.price_label = self.newCtkLabel('Unit Price')
        self.price_label.place(x = 30, y = 430)
        self.price_entry = self.priceCtkEntry()
        self.price_entry.place(x = 191, y = 430)

        # Add Item Button
        self.add_button = self.newCtkButton(text='Add Item',
                                onClickHandler = self.add_entry,
                                fgColor = '#9cc43d',
                                textcolor = '#FFF',
                                hoverColor = '#bceb4b',
                                borderColor = '#9cc43d')
        self.add_button.place(x = 40, y = 485)

        # Delete Item Button
        self.delete_button = self.newCtkButton(text='Delete Item',
                                    onClickHandler=self.delete_entry,
                                    fgColor = '#d71818',
                                    textcolor = '#FFF',
                                    hoverColor = '#ff4c49',
                                    borderColor = '#d71818')
        self.delete_button.place(x = 222, y = 485)

        # New Item Button
        self.new_button = self.newCtkButton(text='New Item',
                                onClickHandler=lambda:self.clear_form(True),
                                fgColor = '#ac8e68',
                                textcolor = '#FFF',
                                hoverColor = '#794300',
                                borderColor = '#ac8e68')
        self.new_button.place(x = 432, y = 430)

        # Update Item Button
        self.update_button = self.newCtkButton(text='Update Item',
                                    onClickHandler=self.update_entry,
                                    fgColor = '#ac8e68',
                                    textcolor = '#FFF',
                                    hoverColor = '#794300',
                                    borderColor = '#ac8e68')
        self.update_button.place(x = 614, y = 430)

        # Export to CSV Button
        self.export_csvbutton = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv,
                                    fgColor = '#ac8e68',
                                    textcolor = '#FFF',
                                    hoverColor = '#794300',
                                    borderColor = '#ac8e68')
        self.export_csvbutton.place(x = 432, y = 485)

        # Export to JSON Button
        self.export_jsonbutton = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_to_json,
                                    fgColor = '#ac8e68',
                                    textcolor = '#FFF',
                                    hoverColor = '#794300',
                                    borderColor = '#ac8e68')
        self.export_jsonbutton.place(x = 614, y = 485)

        # Import CSV File Button
        self.import_csvbutton = self.newCtkButton(text='Import Data',
                                    onClickHandler=self.import_from_csv ,
                                    fgColor = '#ac8e68',
                                    textcolor = '#FFF',
                                    hoverColor = '#794300',
                                    borderColor = '#ac8e68')
        self.import_csvbutton.place(x = 796, y = 457)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        self.style.configure('Treeview', 
                        font = self.font2, 
                        foreground = '#391e00',
                        background = '#FFF',
                        rowheight = 30)
        self.style.configure('Treeview.Heading', 
                        font = self.font4, 
                        foreground = '#391e00')

        self.style.map('Treeview', background=[('selected', '#794300')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Reference Code', 'Item', 'Category', 'Stock Availability', 'Unit Price')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Reference Code', anchor=tk.CENTER, width=100)
        self.tree.column('Item', anchor=tk.CENTER, width=150)
        self.tree.column('Category', anchor=tk.CENTER, width=150)
        self.tree.column('Stock Availability', anchor=tk.CENTER, width=50)
        self.tree.column('Unit Price', anchor=tk.CENTER, width=80)

        self.tree.heading('Reference Code', text='Code')
        self.tree.heading('Item', text='Item')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Stock Availability', text='Stock')
        self.tree.heading('Unit Price', text='Unit Price')

        self.tree.place(x=530, y=40, width=680, height=460)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()


    # Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget = customtkinter.CTkLabel(self, 
                                    text = text,
                                    font = self.font1, 
                                    text_color = '#391e00',
                                    bg_color = '#fff0d7')
        return widget

    # Reference Code Entry Widget
    def codeCtkEntry(self, text = 'CTK Label'):
        widget = customtkinter.CTkEntry(self,
                                    font = self.font3,
                                    placeholder_text = 'PDM0001',
                                    text_color = '#391e00',
                                    fg_color = '#FFF',
                                    bg_color = '#fff0d7',
                                    border_color = '#ac8e68',
                                    border_width = 2,
                                    width = 200)
        return widget

    # Item Entry Widget
    def itemCtkEntry(self, text = 'CTK Label'):
        widget = customtkinter.CTkEntry(self,
                                    font = self.font3,
                                    placeholder_text = 'Bread',
                                    text_color = '#391e00',
                                    fg_color = '#FFF',
                                    bg_color = '#fff0d7',
                                    border_color = '#ac8e68',
                                    border_width = 2,
                                    width = 200)
        return widget

    # Item Entry Widget
    def stockCtkEntry(self, text = 'CTK Label'):
        widget = customtkinter.CTkEntry(self,
                                    font = self.font3,
                                    placeholder_text = '0',
                                    text_color = '#391e00',
                                    fg_color = '#FFF',
                                    bg_color = '#fff0d7',
                                    border_color = '#ac8e68',
                                    border_width = 2,
                                    width = 200)
        return widget
    
    # Unit Price Entry Widget
    def priceCtkEntry(self, text = 'CTK Label'):
        widget = customtkinter.CTkEntry(self,
                                    font = self.font3,
                                    placeholder_text = '1.00',
                                    text_color = '#391e00',
                                    fg_color = '#FFF',
                                    bg_color = '#fff0d7',
                                    border_color = '#ac8e68',
                                    border_width = 2,
                                    width = 200)
        return widget

    # Dropdown Widget
    def newCtkComboBox(self, options = ['DEFAULT', 'OTHER'], entryVariable = None):
        widget = customtkinter.CTkComboBox(self,
                                        font = self.font3,
                                        text_color = '#391e00',
                                        fg_color = '#FFF',
                                        bg_color = '#fff0d7',
                                        dropdown_hover_color = '#ac8e68',
                                        dropdown_fg_color = '#FFF',
                                        dropdown_text_color = '#391e00',
                                        button_color = '#ac8e68',
                                        button_hover_color = '#ac8e68',
                                        border_color = '#ac8e68',
                                        border_width = 2,
                                        width = 200,
                                        variable = entryVariable,
                                        values = options,
                                        state = 'readonly')
        
        # set default value to 1st option
        widget.set('Choose one...')

        return widget

    # Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFF', hoverColor='#6B9773', bgColor='#fff0d7', borderColor='#6B9773', textcolor='#0C3A2D'):
        widget = customtkinter.CTkButton(self,
                                        text = text,
                                        command = onClickHandler,
                                        font = self.font1,
                                        text_color = textcolor,
                                        fg_color = fgColor,
                                        hover_color = hoverColor,
                                        bg_color = bgColor,
                                        border_color = borderColor,
                                        border_width = 0,
                                        cursor = 'hand2',
                                        corner_radius = 15,
                                        width = 160)
       
        return widget

    # Add to Treeview
    def add_to_treeview(self):
        inventory = self.db.fetch_inventory(code=None, item=None, category=None, stock=None, price=None)
        self.tree.delete(*self.tree.get_children())
        for inv in inventory:
            print(inv)
            self.tree.insert('', END, values = inv)

    # Clear Form
    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.code_entry.delete(0, END)
        self.item_entry.delete(0, END)
        self.category_cboxVar.set('Choose one...')
        self.stock_entry.delete(0, END)
        self.price_entry.delete(0, END)

    # Read and Display Data
    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.code_entry.insert(0, row[0])
            self.item_entry.insert(0, row[1])
            self.category_cboxVar.set(row[2])
            self.stock_entry.insert(0, row[3])
            self.price_entry.insert(0, row[4])
        else:
            pass

    # Add New Item
    def add_entry(self):
        code = self.code_entry.get()
        item = self.item_entry.get()
        category = self.category_cboxVar.get()
        stock = self.stock_entry.get()
        price = self.price_entry.get()

        if not (code and item and category and stock and price):
            messagebox.showerror('Error!', 'Complete all input fields.')
        elif self.db.code_exists(code):
            messagebox.showerror('Error!', 'Reference code already exists.')
        else:
            self.db.insert_item(code, item, category, stock, price)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success!', 'A new item has been added.')

    # Delete Item
    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error!', 'Choose an item to delete.')
        else:
            code = self.code_entry.get()
            self.db.delete_item(code)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success!', 'An item has been deleted.')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error!', 'Choose an item to update.')
        else:
            code = self.code_entry.get()
            item = self.item_entry.get()
            category = self.category_cboxVar.get()
            stock = self.stock_entry.get()
            price = self.price_entry.get()
            self.db.update_item(item, category, stock, price, code)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success!', 'An item has been updated.')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success!', f'Inventory exported to {self.db.csv_file}.')

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success!', f'Inventory exported to {self.db.json_file}.')

    def import_from_csv(self):
        csv_file = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if csv_file:
            self.db.import_csv(csv_file)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success!', f'Data imported from {csv_file}.')
        else:
            messagebox.showerror('Error!', f'Failed to import data.')
