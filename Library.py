from Author import Author
from Book import Book
from Customer import Customer
from datetime import datetime
import time
import csv

class LibraryManagementSystem:
    def __init__(self):
        self.books = {}  # Dictionary: ISBN -> Book object
        self.authors = {}  # Dictionary: name -> Author object
        self.customers = {}  # Dictionary: customerID -> Customer object
        self.genre_classification = {}  # Dictionary: Genre -> {set of ISBNs}
        self.waitlist = {}  # Dictionary: ISBN -> [list of customerIDs]

    def add_book(self, isbn, title, author_name, author_birth_year, year, copies, genre):
        
        book = Book(isbn,title,author_name,year,copies,genre)
        self.books[isbn] = book

        if author_name not in self.authors:
            author = Author(author_name,author_birth_year)
            self.authors[author_name] = author
        
        self.authors[author_name].add_book(book)

        if genre not in self.genre_classification:
            self.genre_classification[genre] = set()

        self.genre_classification[genre].add(isbn)

        print(f"\n{book} has been added to the system\n")

    def register_customer(self, name, email):
        id = 1
        if len(self.customers) > 1:
            id = len(self.customers) + 1

        customer = Customer(id, name, email)
        self.customers[id] = customer

        print(f"\nCustomer {self.customers[id]} has been added to the system\n")
        return id

    def borrow_book(self, isbn, customer_id):
        if customer_id not in self.customers:
            print("\nThis customer is not registered\n")
            return
        if isbn not in self.books:
            print("\nThis books is not registered\n") 
            return
        if self.books[isbn].available_copies == 0:
            print("\nThis book is unavailable\n")
        else:
            self.books[isbn].available_copies -= 1
            self.customers[customer_id].borrow_book(self.books[isbn])
            print(f"\nThe customer: {customer_id} borrowed {self.books[isbn]}\n")

    def return_book(self, isbn, customer_id):
        if customer_id not in self.customers:
            print("\nThis customer is not registered\n")
            return
        if isbn not in self.books:
            print("\nThis book is not registered\n")
            return
        if self.books[isbn] in self.customers[customer_id].borrowed_books:
            self.books[isbn].available_copies += 1
            self.customers[customer_id].return_book(self.books[isbn])
            print(f"\nThe customer {customer_id} returned {self.books[isbn]}\n")

    def search_books(self, query):
        # ISBN
        for isbn in self.books:
            if str(query) == str(isbn):
                print()
                print(self.books[isbn],"\n")
        
        # Title
        for book in self.books.values():
            if query == book.title:
                print()
                print(book,"\n")
        
        # Author
        for book in self.books.values():
            if query == book.author:
                print()
                print(book,"\n")


    def display_available_books(self): 
        available_books = []
        for book in self.books.values():
            if book.available_copies > 0:
                available_books.append(book)
        
        return available_books
    
    def display_customer_books(self, customer_id):
        customer_books = []
        for book in self.customers[customer_id].borrowed_books.keys():
            customer_books.append(book)

        print()
        return customer_books

    def recommend_books(self, customer_id):
        if customer_id not in self.customers:
            print("\nThis customer is not registered.\n")
            return []

        genres = {}
        customer = self.customers[customer_id]  # Get the Customer object directly

        for book in customer.borrowed_books.keys():
            if book.genre not in genres:
                genres[book.genre] = 1
            else:
                genres[book.genre] += 1

        if not genres:
            print(f"\nCustomer {customer_id} has not borrowed any books for recommendations.\n")
            return []

        favorite_genre = max(genres, key=genres.get)

        candidates = []
        for book in self.books.values():
            if book.genre == favorite_genre:
                candidates.append(book)
            if len(candidates) == 5:
                break

        return candidates

    def add_to_waitlist(self, isbn, customer_id):
        if isbn not in self.waitlist:
            self.waitlist[isbn] = []
        if customer_id in self.waitlist[isbn]:
            print("\nThis customer is already in the waitlist\n")
        else:
            self.waitlist[isbn].append(customer_id)

    def check_late_returns(self, days_threshold=14):
        late_returns = []
        current_date = datetime.now()

        for customer in self.customers.values():
            for book, borrow_date in customer.borrowed_books.items():
                days_borrowed = (current_date - borrow_date).days

                if days_borrowed > days_threshold:
                    late_returns.append((book, days_borrowed))

        if len(late_returns) == 0:
            print("\nThere are no late returns at this time\n")
        else:
            return late_returns
        
    def load_books_from_csv(self, filename):
        try:
            with open(filename, mode = 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    isbn = int(row[0])
                    title = row[1]
                    author_name = row[2]
                    author_birth_year = int(row[3])
                    year = int(row[4])
                    copies = int(row[5])
                    genre = row[6]

                    # Add the book using the add_book method
                    self.add_book(isbn, title, author_name, author_birth_year, year, copies, genre)

            print(f"\nBooks from {filename} have been successfully loaded into the system.\n")
        
        except FileNotFoundError:
            print(f"\nError: File {filename} not found.\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
                    

    def run(self):
        self.load_books_from_csv("Books.csv")

        print("Welcome to the library!\n")
        while True:
            print("1. Add book")
            print("2. Register Customer")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Search Books")
            print("6. Display Available Books")
            print("7. Display Customer's Borrowed Books")
            print("8. Recommend Books")
            print("9. Check Late Returns")
            print("10. Exit\n")

            selection = int(input("What would you like to do? "))

            if selection == 1:
                book = input("Type the book info with the following format: Isbn, Title, Author name, Author birth year, Year, Copies, Genre:\n")
                L = book.split(", ")
                self.add_book(int(L[0]), L[1], L[2], int(L[3]), int(L[4]), int(L[5]), L[6])
                time.sleep(3)

            if selection == 2:
                customer = input("Type the customer info with the following format: Name, E-mail: ")
                L = customer.split(", ")
                self.register_customer(L[0],L[1])
                time.sleep(3)

            if selection == 3:
                book = input("Type the book's isbn and customer's id with the following format: Isbn, Customer ID: ")
                L = book.split(", ")
                self.borrow_book(int(L[0]),int(L[1]))
                time.sleep(3)

            if selection == 4:
                book = input("Type the book's isbn you want to return and the customer's id with the following format: Isbn, Customer ID: ")
                L = book.split(", ")
                self.return_book(int(L[0]),int(L[1]))
                time.sleep(3)

            if selection == 5:
                query = input("Type the title, author name, or ISBN: ")
                self.search_books(query)
                time.sleep(3)

            if selection == 6:
                books = self.display_available_books()
                for book in books:
                    print(book)
                time.sleep(3)

            if selection == 7:
                customer = int(input("Type Customer ID: "))
                for book in self.display_customer_books(customer):
                    print(book)
                time.sleep(3)

            if selection == 8:
                customer = int(input("Type Customer ID: "))
                print("This are some of our recommendations for you:")
                for book in self.recommend_books(customer):
                    print(book)
                time.sleep(3)

            if selection == 9:
                self.check_late_returns()
                time.sleep(3)
            
            if selection == 10:
                print("See you soon!")
                break

if __name__ == "__main__":
    library_system = LibraryManagementSystem()  # Create an instance of the library system
    library_system.run()