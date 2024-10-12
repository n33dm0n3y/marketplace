from django.urls import path

from . import views

app_name = 'inbox'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('delete/<int:contact_id>/', views.delete_contact_message, name='delete_contact_message'),  # Add this line
]   