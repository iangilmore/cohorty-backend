
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # '' represents the "starts with" path
    path('', include('main_app.urls')),
]