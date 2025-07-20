from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view for listing all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prefetch related books with their authors
        context['library'].books.select_related('author').all()
        return context
    
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view for listing all books
def list_books(request):
    # Explicitly using Book.objects.all() as requested
    all_books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', 
                {'books': all_books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly fetching books for the library
        context['books'] = self.object.books.all().select_related('author')
        return context
    
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # Explicitly importing Library

# Function-based view for listing all books
def list_books(request):
    # Using Book.objects.all() as requested
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', 
                {'books': books})

# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library  # Now properly imported
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prefetch related books with their authors
        context['books'] = self.object.books.all().select_related('author')
        return context
    from .models import Library