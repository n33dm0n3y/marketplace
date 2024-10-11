from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import NewItemForm, EditItemForm, RatingForm
from .models import Item, Category, Rating

# Check if the user is a superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# View for listing items with search and filtering
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

# View to show item detail and its related items
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    ratings = item.ratings.all()  # Get all ratings for the item

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'ratings': ratings
    })

# View to create a new item
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

# View to edit an existing item
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

# View to delete an item (superuser required)
@superuser_required
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('core:index')





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Rating




@login_required
def rate_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    existing_rating = Rating.objects.filter(item=item, user=request.user).first()
    if existing_rating:
        return JsonResponse({"error": "You have already rated this item."}, status=400)

    if request.method == 'POST':
        data = request.POST
        rating_value = data.get('rating')
        comment = data.get('comment', '')

        if not rating_value or float(rating_value) < 1 or float(rating_value) > 5:
            return JsonResponse({"error": "Invalid rating value."}, status=400)

        
        Rating.objects.create(
            item=item,
            user=request.user,
            stars=float(rating_value),
            comment=comment
        )
        
        return JsonResponse({"message": "Rating submitted successfully."})

    return JsonResponse({"error": "Invalid request method."}, status=400)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Item, Rating

@login_required
def get_item_ratings(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user_rating = Rating.objects.filter(item=item, user=request.user).first()  # Get the user's existing rating

    # Prepare ratings data for the item
    ratings = Rating.objects.filter(item=item)
    ratings_data = [
        {
            'user': rating.user.username,
            'rating': rating.stars,
            'comment': rating.comment,
        }
        for rating in ratings
    ]

    # If no ratings are found, return a message
    if not ratings_data:
        return JsonResponse({"message": "No ratings found for this item."}, status=404)

    # Return the ratings data along with the user's existing rating for editing purposes
    return JsonResponse({
        "ratings": ratings_data,
        "user_rating": {
            'rating': user_rating.stars if user_rating else None,
            'comment': user_rating.comment if user_rating else ''
        }
    }, status=200)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Rating
from .forms import RatingForm

def RateEdit(request, pk):
    rating = get_object_or_404(Rating, item_id=pk, user=request.user)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        rating.rating = rating_value
        rating.comment = comment
        rating.save()
        
        return JsonResponse({"message": "Rating updated successfully"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
