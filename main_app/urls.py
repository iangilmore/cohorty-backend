from django.urls import path # type: ignore
from .views import Home

urlpatterns = [
  path('', Home.as_view(), name='home'),
]

# Ian edit
# Addy edit 