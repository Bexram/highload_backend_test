from django.urls import path
from .views import *
urlpatterns = [
    path('<int:pk>/', get_groups),
    # path('update_db/', update_db_api)
]
