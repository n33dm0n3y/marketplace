from django.contrib import admin

from .models import Category,Item,Rating

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Rating)

