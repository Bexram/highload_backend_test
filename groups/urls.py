from django.urls import path
from .views import *
urlpatterns = [
    path('<int:pk>/', get_groups)
]
