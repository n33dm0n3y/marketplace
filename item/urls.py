from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('item/<int:item_id>/rate/', views.rate_item, name='rate_item'),
    path('item/<int:item_id>/ratings/', views.get_item_ratings, name='get_item_ratings'),
    path('rate/edit/<int:pk>/', views.RateEdit, name='rate_edit'),

    


    
]
