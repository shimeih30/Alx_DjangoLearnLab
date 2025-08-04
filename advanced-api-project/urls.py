from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 👈 Route all API calls through /api/
]
"books/update", "books/delete"
["from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated"]
["api.urls"]

from django.contrib import admin
from django.urls import path, include  # ✅ include is required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # ✅ This line is required to include api.urls
]
