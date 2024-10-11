from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=225)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=False)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        # Calculate the average rating from the associated ratings
        ratings = self.ratings.all()  # use related_name from Rating model
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class Rating(models.Model):
    item = models.ForeignKey(Item, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    stars = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text='Rating must be between 0.0 and 5.0, with half stars allowed.'
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stars} stars for {self.item.name} by {self.user.username}'
