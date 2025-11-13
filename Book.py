class Book:
    def __init__(self, isbn, title, author, year, copies, genre):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.available_copies = copies
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"