from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
# Contact model
class ContactModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages_sent")  # Sender
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.first_name} {self.last_name} - {self.email}'

# ActivityLog model (standalone)
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.action} at {self.timestamp}'
    
