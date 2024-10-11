from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('add-category/', views.add_category, name='add_category'), 
    path('contact/', views.contact, name='contact'),
    path('admin/delete_category/<int:category_id>/', views.delete_category, name='delete_category'),  # Add this line
    path('privacy/', views.privacy, name='privacy'),
    path('term_use/', views.term_use, name='term_use'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
