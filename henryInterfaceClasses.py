# Matt Krzewinski

class Author():
    def __init__(self, num, last, first):
        self.num = num
        self.last = last
        self.first = first

    def __str__(self):
        return f'{self.first} {self.last}'


class Publisher():
    def __init__(self, pub_code, pub_name):
        self.pub_code = pub_code
        self.pub_name = pub_name

    def __str__(self):
        return f'{self.pub_name}'


class Category():
    def __init__(self, cat):
        self.cat = cat

    def __str__(self):
        return f'{self.cat}'


class Book():
    def __init__(self, book_code, title, publisher_code, book_type, price, paperback):
        self.book_code = book_code
        self.title = title
        self.publisher_code = publisher_code
        self.book_type = book_type
        self.price = price
        self.paperback = paperback

    def __str__(self):
        return f'Book code is {self.book_code} title {self.title} published by {self.publisher_code} ' \
               f'{self.book_type} {self.price} {self.paperback}'


class Availability():
    def __init__(self, branch_name, on_hand):
        self.branch_name = branch_name
        self.on_hand = on_hand

    def __str__(self):
        return f'Branch: {self.branch_name} has {self.on_hand} copies'
