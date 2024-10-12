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

        return redirect('success')  # Redirect to a success page after form submission

    return render(request, 'core/contact.html')
