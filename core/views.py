from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import ActivityLog
from .models import ContactModel
from item.models import Category, Item
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

# Admin dashboard view
def admin_dashboard(request):
    if request.user.is_superuser:
        total_users = User.objects.count()
        total_categories = Category.objects.count()
        total_items = Item.objects.count()

        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]

        return render(request, 'core/index.html', {
            'total_users': total_users,
            'total_categories': total_categories,
            'total_items': total_items,
            'recent_activities': recent_activities,
        })
    return redirect('core:login')
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

def contact(request):
    if request.method == 'POST':
        ContactModel.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], message=request.POST['message'])
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
