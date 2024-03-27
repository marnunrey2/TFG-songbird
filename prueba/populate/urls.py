from django.urls import path
from .views import populate_view

urlpatterns = [
    path("", populate_view, name="populate"),
]
