from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # show these columns in admin
    search_fields = ('title', 'author')                     # make title & author searchable
    list_filter = ('publication_year',)                     # allow filtering by year

["admin.site.register(CustomUser, CustomUserAdmin)"]
