from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from core.models import ContactModel
from .forms import ConversationMessageForm
from .models import Conversation


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(item=item, members=request.user)

    if conversations.exists():
        return redirect('inbox:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            contact_message = ContactModel(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                message=form.cleaned_data['content'],
                user=request.user
            )
            contact_message.save()

            conversation = Conversation.objects.create(
                item=item,
                contact_message=contact_message
            )
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def delete_contact_message(request, contact_id):
    contact_message = get_object_or_404(ContactModel, id=contact_id)

    if request.user.is_superuser:
        contact_message.delete()
    else:
        return redirect('inbox:inbox')

    return redirect('inbox:inbox')

@login_required
def inbox(request):
    contact_conversations = Conversation.objects.filter(members=request.user)
    
    return render(request, 'conversation/inbox.html', {
        'contact_conversations': contact_conversations,
    })



@login_required
def detail(request, pk):
    # Retrieve the conversation, ensuring the user is a member
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Create a new message instance but do not save it yet
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()  # Save the message to the database

            return redirect('inbox:detail', pk=pk)  # Redirect to the same conversation detail page
    else:
        form = ConversationMessageForm()  # Create a new form instance for GET requests

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
        'is_contact': conversation.contact_message is not None,
    })
