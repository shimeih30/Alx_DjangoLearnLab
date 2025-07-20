import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="A Game of Thrones", author=author2)
    
    # Create library
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2)
    
    # Assign librarian
    librarian = Librarian.objects.create(name="Ms. Smith", library=library)
    
    return author1, library

def run_queries():
    author, library = create_sample_data()
    
    print("\n1. All books by a specific author:")
    books_by_author = Book.objects.filter(author=author)
    for book in books_by_author:
        print(f"- {book.title}")
    
    print("\n2. All books in a library:")
    books_in_library = library.books.all()
    for book in books_in_library:
        print(f"- {book.title}")
    
    print("\n3. Librarian for a library:")
    librarian = Librarian.objects.get(library=library)
    print(f"- {librarian.name}")

if __name__ == "__main__":
    run_queries()