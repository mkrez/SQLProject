# Matt Krzewinski

# This file makes the GUI using tkinter

# Importing tkinter and the DAO
import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO


# Making the initial window, adds title, and makes size
root = tk.Tk()
root.option_add('*TCombobox*Listbox.foreground', 'blue') # change dropdown colors
root.title('Henry Bookstore')
root.geometry('900x400')


# Setting up the tab control
tabControl = ttk.Notebook(root) # Making a tab control
tabControl.pack(expand=1, fill="both") # Making the tabs show up
henryDB = HenryDAO() # Making a data access object class


# Search by Author tab class
class HenrySBA():
    def __init__(self):
        # Making the layout on the author tab
        self.author_tab = ttk.Frame(tabControl)
        tabControl.add(self.author_tab, text="Search by Author")

        # Adding the author combo box label
        self.author_lab = ttk.Label(self.author_tab)
        self.author_lab.grid(column=1, row=1)
        self.author_lab['text'] = "Author Selection"

        # Adding the book combo box label
        self.book_lab = ttk.Label(self.author_tab)
        self.book_lab.grid(column=2, row=1)
        self.book_lab['text'] = "Book Selection"

        # Getting the author names data
        henryDB.getAuthorData()  # Getting the initial author list to populate the GUI

        # Initial book list and prices for the first author
        first = henryDB.authors_list[0]
        henryDB.getBooksByAuthor(first.num)
        self.book_list = []
        self.book_prices = []
        self.book_codes = []

        for book in henryDB.auth_book_list:
            self.book_list.append(book.title)
            self.book_prices.append(book.price)
            self.book_codes.append(book.book_code)

        # Initial book code to fill in price and availability when GUI is launched
        henryDB.getBookAvailability(self.book_codes[0])

        # Adding the author combobox
        self.author_combo = ttk.Combobox(self.author_tab, width=20, state="readonly")
        self.author_combo.grid(column=1, row=2)
        self.author_combo['values'] = henryDB.authors_list # Putting values in the box
        self.author_combo.current(0) # Setting the first author as the initial value
        self.author_combo.bind("<<ComboboxSelected>>", HenrySBA.author_selection)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(self.author_tab, width=20, state="readonly")
        self.book_combo.grid(column=2, row=2)
        self.book_combo['values'] = self.book_list # Putting values in the box
        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", HenrySBA.book_selection)

        # Setting the initial price
        self.price = ttk.Label(self.author_tab)
        self.price.grid(column=4, row=5)
        self.price['text'] = "Price: $" + str(self.book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(self.author_tab, columns=('Branch', 'Copies'), show='headings')
        self.avlab = ttk.Label(self.author_tab)
        self.avlab.grid(column=4, row=2)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=3)
        for row in henryDB.book_availability: # Fills in the availability tree with the first book's info
            self.av.insert("", "end", values=[row.branch_name, row.on_hand])


    # Get info when the author is changed and autofill the first book information
    def author_selection(event):
        selIndex = event.widget.current()
        auth = henryDB.authors_list[selIndex]
        henryDB.getBooksByAuthor(auth.num) # Getting the correct author num

        # Emptying the lists
        henrySBA.book_list = []
        henrySBA.book_prices = []
        henrySBA.book_codes = []

        # Book info for the selected author
        for row in henryDB.auth_book_list:
            henrySBA.book_list.append(row.title)
            henrySBA.book_prices.append(row.price)
            henrySBA.book_codes.append(row.book_code)

        # Filling in the book combo box and correct price
        henrySBA.book_combo['values'] = henrySBA.book_list  # Book combobox is updated with author's work
        henrySBA.book_combo.current(0) # Puts the first book in the combobox
        henrySBA.price['text'] = ("Price: $" + str(henrySBA.book_prices[0])) # Puts the price of the first book

        # Filling in the availability for the first book
        henryDB.getBookAvailability(henrySBA.book_codes[0])

        for i in henrySBA.av.get_children():  # Remove any old values in tree list
            henrySBA.av.delete(i)
        for row in henryDB.book_availability:  # Fills in the availability tree
            henrySBA.av.insert("", "end", values=[row.branch_name, row.on_hand])



    # Get the info when a different book is selected
    def book_selection(event):
        selIndex = event.widget.current()
        henrySBA.price['text'] = ("Price: $" + str(henrySBA.book_prices[selIndex])) # Updates the price
        henryDB.getBookAvailability(str(henrySBA.book_codes[selIndex])) # Gets info from the new book code

        for i in henrySBA.av.get_children():  # Remove any old values in tree list
            henrySBA.av.delete(i)
        for row in henryDB.book_availability: # Fills in the availability tree
            henrySBA.av.insert("", "end", values=[row.branch_name, row.on_hand])


# Search by Publisher tab class
class HenrySBP():
    def __init__(self):
        # Making the layout on the publisher tab
        self.publisher_tab = ttk.Frame(tabControl)
        tabControl.add(self.publisher_tab, text="Search by Publisher")

        # Adding the publisher combo box label
        self.publisher_lab = ttk.Label(self.publisher_tab)
        self.publisher_lab.grid(column=1, row=1)
        self.publisher_lab['text'] = "Publisher Selection"

        # Adding the book combo box label
        self.book_lab = ttk.Label(self.publisher_tab)
        self.book_lab.grid(column=2, row=1)
        self.book_lab['text'] = "Book Selection"

        # Getting the Publisher names data
        henryDB.getPublisherData()  # Getting the initial publisher list to populate the GUI

        # Initial book list and prices for the first publisher
        first = henryDB.publisher_list[0]
        henryDB.getBooksByPublisher(first.pub_code)

        self.book_list = []
        self.book_prices = []
        self.book_codes = []

        for book in henryDB.pub_book_list:
            self.book_list.append(book.title)
            self.book_prices.append(book.price)
            self.book_codes.append(book.book_code)

        print(self.book_codes)
        # Initial book code to fill in price and availability when GUI is launched
        henryDB.getBookAvailability(self.book_codes[0])

        # Adding the publisher combobox
        self.publisher_combo = ttk.Combobox(self.publisher_tab, width=20, state="readonly")
        self.publisher_combo.grid(column=1, row=2)
        self.publisher_combo['values'] = henryDB.publisher_list # Putting values in the box
        self.publisher_combo.current(0) # Setting the first author as the initial value
        self.publisher_combo.bind("<<ComboboxSelected>>", HenrySBP.publisher_selection)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(self.publisher_tab, width=20, state="readonly")
        self.book_combo.grid(column=2, row=2)
        self.book_combo['values'] = self.book_list # Putting values in the box
        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", HenrySBP.book_selection)

        # Setting the initial price
        self.price = ttk.Label(self.publisher_tab)
        self.price.grid(column=4, row=5)
        self.price['text'] = "Price: $" + str(self.book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(self.publisher_tab, columns=('Branch', 'Copies'), show='headings')
        self.avlab = ttk.Label(self.publisher_tab)
        self.avlab.grid(column=4, row=2)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=3)
        for row in henryDB.book_availability: # Fills in the availability tree with the first book's info
            self.av.insert("", "end", values=[row.branch_name, row.on_hand])


    # Get info when the author is changed and autofill the first book information
    def publisher_selection(event):
        selIndex = event.widget.current()
        pub = henryDB.publisher_list[selIndex]
        henryDB.getBooksByPublisher(pub.pub_code) # Getting the correct author num

        print(henryDB.pub_book_list)
        # Emptying the lists
        henrySBP.book_list = []
        henrySBP.book_prices = []
        henrySBP.book_codes = []

        # Book info for the selected author
        for row in henryDB.pub_book_list:
            henrySBP.book_list.append(row.title)
            henrySBP.book_prices.append(row.price)
            henrySBP.book_codes.append(row.book_code)

        # Filling in the book combo box and correct price
        henrySBP.book_combo['values'] = henrySBP.book_list  # Book combobox is updated with author's work
        henrySBP.book_combo.current(0) # Puts the first book in the combobox
        henrySBP.price['text'] = ("Price: $" + str(henrySBP.book_prices[0])) # Puts the price of the first book

        # Filling in the availability for the first book
        henryDB.getBookAvailability(henrySBP.book_codes[0])

        for i in henrySBP.av.get_children():  # Remove any old values in tree list
            henrySBP.av.delete(i)
        for row in henryDB.book_availability:  # Fills in the availability tree
            henrySBP.av.insert("", "end", values=[row.branch_name, row.on_hand])


    # Get the info when a different book is selected
    def book_selection(event):
        selIndex = event.widget.current()
        henrySBP.price['text'] = ("Price: $" + str(henrySBP.book_prices[selIndex])) # Updates the price
        henryDB.getBookAvailability(str(henrySBP.book_codes[selIndex])) # Gets info from the new book code

        for i in henrySBP.av.get_children():  # Remove any old values in tree list
            henrySBP.av.delete(i)
        for row in henryDB.book_availability: # Fills in the availability tree
            henrySBP.av.insert("", "end", values=[row.branch_name, row.on_hand])


# Search by Category tab class
class HenrySBC():
    def __init__(self):
        # Making the layout on the category tab
        self.category_tab = ttk.Frame(tabControl)
        tabControl.add(self.category_tab, text="Search by Category")

        # Adding the category combo box label
        self.category_lab = ttk.Label(self.category_tab)
        self.category_lab.grid(column=1, row=1)
        self.category_lab['text'] = "Category Selection"

        # Adding the book combo box label
        self.book_lab = ttk.Label(self.category_tab)
        self.book_lab.grid(column=2, row=1)
        self.book_lab['text'] = "Book Selection"

        # Getting the category names data
        henryDB.getCategoryData()  # Getting the initial category list to populate the GUI

        # Initial book list and prices for the first category
        first = henryDB.category_list[0]
        henryDB.getBooksByCategory(first.cat)
        self.book_list = []
        self.book_prices = []
        self.book_codes = []

        for book in henryDB.cat_book_list:
            self.book_list.append(book.title)
            self.book_prices.append(book.price)
            self.book_codes.append(book.book_code)

        # Initial book code to fill in price and availability when GUI is launched
        henryDB.getBookAvailability(self.book_codes[0])

        # Adding the category combobox
        self.category_combo = ttk.Combobox(self.category_tab, width=20, state="readonly")
        self.category_combo.grid(column=1, row=2)
        self.category_combo['values'] = henryDB.category_list # Putting values in the box
        self.category_combo.current(0) # Setting the first category as the initial value
        self.category_combo.bind("<<ComboboxSelected>>", HenrySBC.category_selection)  # Bind a callback

        # Adding the books combobox
        self.book_combo = ttk.Combobox(self.category_tab, width=20, state="readonly")
        self.book_combo.grid(column=2, row=2)
        self.book_combo['values'] = self.book_list # Putting values in the box
        self.book_combo.current(0) # Setting the first book as the initial value
        self.book_combo.bind("<<ComboboxSelected>>", HenrySBC.book_selection)

        # Setting the initial price
        self.price = ttk.Label(self.category_tab)
        self.price.grid(column=4, row=5)
        self.price['text'] = "Price: $" + str(self.book_prices[0])

        # Availability tree
        self.av = ttk.Treeview(self.category_tab, columns=('Branch', 'Copies'), show='headings')
        self.avlab = ttk.Label(self.category_tab)
        self.avlab.grid(column=4, row=2)
        self.avlab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(column=4, row=3)
        for row in henryDB.book_availability: # Fills in the availability tree with the first book's info
            self.av.insert("", "end", values=[row.branch_name, row.on_hand])


    # Get info when the category is changed and autofill the first book information
    def category_selection(event):
        selIndex = event.widget.current()
        cat = henryDB.category_list[selIndex]
        henryDB.getBooksByCategory(cat.cat) # Getting the correct category name

        # Emptying the lists
        henrySBC.book_list = []
        henrySBC.book_prices = []
        henrySBC.book_codes = []

        # Book info for the selected author
        for row in henryDB.cat_book_list:
            henrySBC.book_list.append(row.title)
            henrySBC.book_prices.append(row.price)
            henrySBC.book_codes.append(row.book_code)

        # Filling in the book combo box and correct price
        henrySBC.book_combo['values'] = henrySBC.book_list  # Book combobox is updated with category work
        henrySBC.book_combo.current(0) # Puts the first book in the combobox
        henrySBC.price['text'] = ("Price: $" + str(henrySBC.book_prices[0])) # Puts the price of the first book

        # Filling in the availability for the first book
        henryDB.getBookAvailability(henrySBC.book_codes[0])

        for i in henrySBC.av.get_children():  # Remove any old values in tree list
            henrySBC.av.delete(i)
        for row in henryDB.book_availability:  # Fills in the availability tree
            henrySBC.av.insert("", "end", values=[row.branch_name, row.on_hand])



    # Get the info when a different book is selected
    def book_selection(event):
        selIndex = event.widget.current()
        henrySBC.price['text'] = ("Price: $" + str(henrySBC.book_prices[selIndex])) # Updates the price
        henryDB.getBookAvailability(str(henrySBC.book_codes[selIndex])) # Gets info from the new book code

        for i in henrySBC.av.get_children():  # Remove any old values in tree list
            henrySBC.av.delete(i)
        for row in henryDB.book_availability: # Fills in the availability tree
            henrySBC.av.insert("", "end", values=[row.branch_name, row.on_hand])


henrySBA = HenrySBA()
henrySBP = HenrySBP()
henrySBC = HenrySBC()
root.mainloop()
