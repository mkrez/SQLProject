import mysql.connector
from henryInterfaceClasses import Author
from henryInterfaceClasses import Book
from henryInterfaceClasses import Availability
from henryInterfaceClasses import Publisher
from henryInterfaceClasses import Category


class HenryDAO():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user='root',
            passwd='Justice1',
            database='comp3421',
            host='127.0.0.1') # local host

        self.mycur = self.mydb.cursor()

        self.authors_list = []
        self.auth_book_list = []
        self.publisher_list = []
        self.pub_book_list = []
        self.category_list = []
        self.cat_book_list = []
        self.book_availability = []


    def getAuthorData(self):
        self.authors_list = []
        # Perform the query
        # Only want authors who wrote books
        sql = "SELECT * FROM HENRY_AUTHOR WHERE AUTHOR_NUM IN (SELECT AUTHOR_NUM FROM HENRY_WROTE);"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Author objects
        for row in self.mycur:
            author = Author(row[0], row[1], row[2])
            self.authors_list.append(author)

    def getBooksByAuthor(self, id):
        self.auth_book_list = []
        author_num = str(id)
        sql = "SELECT * FROM HENRY_BOOK WHERE BOOK_CODE IN " \
              "(SELECT BOOK_CODE FROM HENRY_WROTE WHERE AUTHOR_NUM = " + author_num + ");"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Book objects
        for row in self.mycur:
            book = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            self.auth_book_list.append(book)


    def getPublisherData(self):
        self.publisher_list = []
        # Perform the query
        # Getting all the publishers
        sql = "SELECT PUBLISHER_CODE, PUBLISHER_NAME FROM HENRY_PUBLISHER" \
              " WHERE PUBLISHER_CODE IN (SELECT PUBLISHER_CODE FROM HENRY_BOOK);"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Publisher objects
        for row in self.mycur:
            publisher = Publisher(row[0], row[1])
            self.publisher_list.append(publisher)

    def getBooksByPublisher(self, pub_code):
        self.pub_book_list = []
        pub_code = str(pub_code)
        sql = "SELECT * FROM HENRY_BOOK WHERE PUBLISHER_CODE = '" + pub_code + "';"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Book objects
        for row in self.mycur:
            book = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            self.pub_book_list.append(book)


    def getCategoryData(self):
        self.category_list = []
        # Perform the query
        sql = "SELECT DISTINCT(TYPE) FROM HENRY_BOOK;"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Category objects
        for row in self.mycur:
            category = Category(row[0])
            self.category_list.append(category)

    def getBooksByCategory(self, category):
        self.cat_book_list = []
        cat = str(category)
        sql = "SELECT * FROM HENRY_BOOK WHERE TYPE = '" + cat + "';"
        print(sql)
        self.mycur.execute(sql)

        # Create a list of Book objects
        for row in self.mycur:
            book = Book(row[0], row[1], row[2], row[3], row[4], row[5])
            self.cat_book_list.append(book)

    def getBookAvailability(self, book_code):
        self.book_availability = []
        code = str(book_code)
        sql = "SELECT BRANCH_NAME, ON_HAND FROM HENRY_INVENTORY inv JOIN HENRY_BRANCH bra ON " \
              "inv.BRANCH_NUM = bra.BRANCH_NUM WHERE book_code = '" + code + "';"
        print(sql)
        self.mycur.execute(sql)
        for row in self.mycur:
            inStock = Availability(row[0], row[1])
            self.book_availability.append(inStock)

    def close(self):
        self.mydb.commit()
        self.mydb.close()
