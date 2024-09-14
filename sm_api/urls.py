from django.urls import path, include

from . import views
from .views import list_employees, get_employee, create_employee, update_employee, delete_employee, login_view, \
    logout_view

urlpatterns = [
    path('employees/', list_employees, name='list_employees'),
    path('employees/<int:pk>/', get_employee, name='get_employee'),
    path('employees/create/', create_employee, name='create_employee'),
    path('employees/<int:pk>/update/', update_employee, name='update_employee'),
    path('employees/<int:pk>/delete/', delete_employee, name='delete_employee'),

    path('users/', views.list_users, name='list_users'),  # List all users
    path('users/create/', views.create_user, name='create_user'),  # Create a new user
    path('users/<int:user_id>/', views.get_user, name='get_user'),  # Retrieve a single user
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),  # Update a user
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
