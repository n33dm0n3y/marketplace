from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import ActivityLog
from .models import ContactModel
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from item.models import Category, Item
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Admin dashboard view

def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('core:index')
    
    if request.user.is_superuser and request.user.is_authenticated:
        users = User.objects.all()  
        total_users = users.count()
        total_categories = Category.objects.count()
        total_items = Item.objects.count()
        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]
        categories = Category.objects.all()  # Get all categories

        return render(request, 'core/admin_dashboard.html', {
            'total_users': total_users,
            'users': users,
            'total_categories': total_categories,
            'total_items': total_items,
            'recent_activities': recent_activities,
            'categories': categories,  # Pass the list of categories to the template
        })
    return redirect('core:login')


def add_category(request):
    if not request.user.is_superuser:
        return redirect('core:index')
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        # Create a new category instance and save it to the database
        new_category = Category(name=category_name)
        new_category.save()
        return redirect('core:admin_dashboard')  # Redirect back to the admin dashboard
    return redirect('core:admin_dashboard')  

def delete_user(request, user_id):

    if not request.user.is_superuser:
        return redirect('core:index')
    

    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete users.')
    
    return redirect('core:admin_dashboard') 


def delete_category(request, category_id):
    if not request.user.is_superuser:
        return redirect('core:index')

    if request.user.is_superuser:
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return redirect('core:admin_dashboard')

def update_user(request, user_id):

    if not request.user.is_superuser:
        return redirect('core:index')


    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        
        if request.user.is_superuser:
            user.username = new_username
            user.email = new_email
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('core:admin_dashboard')
        else:
            messages.error(request, 'You do not have permission to update users.')

    return render(request, 'core/update_user.html', {'user': user})  # Render template for GET requests


# Regular index view for all users
def index(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()

    if request.user.is_authenticated:
        return render(request, 'core/index.html', {
            'categories': categories,
            'items': items,
        })
    else:
        return redirect('core:login')

def logout_view(request):
    logout(request)
    return redirect('core:login')

def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the contact message in the database
        contact_message = ContactModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message,
            user=request.user if request.user.is_authenticated else None
        )

        # Send an email to the admins
        send_mail(
            subject=f"New Contact Us message from {first_name} {last_name}",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['angelite.online.marketplace.@gmail.com'],  # Replace with the admin email
            fail_silently=False,
        )

        return redirect('core:index')  # Redirect to homepage after form submission

    return render(request, 'core/contact.html')


def privacy(request):
    return render(request, 'core/privacy.html')

def term_use(request):
    return render(request, 'core/term_use.html')

def about(request):
    return render(request, 'core/about.html')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })
