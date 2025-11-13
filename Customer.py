from datetime import datetime

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.borrowed_books = {} #key is the book and value is the date they borrowed it

    def borrow_book(self, book):
        if book in self.borrowed_books:
            print("You have already borrowed this book")
        else:
            self.borrowed_books[book] = datetime.now()

    def return_book(self, book):
        if book not in self.borrowed_books:
            print("You have not borrowed this book")
        else:
            del self.borrowed_books[book]

    def get_borrowed_books(self):
        return list(self.borrowed_books.keys())
    
    def __str__(self): 
        return f"ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"