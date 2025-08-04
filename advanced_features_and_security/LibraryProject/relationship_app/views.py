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
    from django.views.generic.detail import DetailView
    
    from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile

def check_role(user, allowed_roles):
    try:
        return user.userprofile.role in allowed_roles
    except UserProfile.DoesNotExist:
        return False

def admin_check(user):
    return check_role(user, ['ADMIN'])

def librarian_check(user):
    return check_role(user, ['LIBRARIAN', 'ADMIN'])  # Admins can access librarian views

def member_check(user):
    return check_role(user, ['MEMBER', 'LIBRARIAN', 'ADMIN'])  # All roles can access member views

@login_required
@user_passes_test(admin_check, login_url='/accounts/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(librarian_check, login_url='/accounts/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(member_check, login_url='/accounts/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set default role (or you can add a role field to the form)
            UserProfile.objects.create(user=user, role='MEMBER')
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import permission_required 
relationship_app.can_add_book
relationship_app.can_change_book
relationship_app.can_delete_book