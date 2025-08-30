from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max
from django.views.decorators.http import require_POST

@login_required
def chats(request):
    current_user = request.user
    
    # Get the conversation list for the left panel
    sent_to_ids = Message.objects.filter(sender=current_user).values_list('receiver_id', flat=True)
    received_from_ids = Message.objects.filter(receiver=current_user).values_list('sender_id', flat=True)
    user_ids = set(list(sent_to_ids) + list(received_from_ids))
    users_with_chats = User.objects.filter(id__in=user_ids)

    chat_previews = []
    for user in users_with_chats:
        try:
            latest_message = Message.objects.filter(
                (Q(sender=current_user, receiver=user) | Q(sender=user, receiver=current_user))
            ).latest('timestamp')
        except Message.DoesNotExist:
            continue
        unread_count = Message.objects.filter(sender=user, receiver=current_user, is_read=False).count()
        chat_previews.append({
            'user': user,
            'latest_message_time': latest_message.timestamp,
            'unread_count': unread_count
        })
    chat_previews.sort(key=lambda x: x['latest_message_time'], reverse=True)
    
    # Get all users for the "New Chat" modal
    all_users = current_user.profile.friends.all()

    context = {
        'chat_previews': chat_previews,
        'all_users': all_users
    }
    
    return render(request, 'inbox.html', context)


# View 2: Handles displaying a specific chat
@login_required
def chat_view(request, username):
    current_user = request.user
    
    # --- Get the same data as the 'chats' view for the left panel ---
    sent_to_ids = Message.objects.filter(sender=current_user).values_list('receiver_id', flat=True)
    received_from_ids = Message.objects.filter(receiver=current_user).values_list('sender_id', flat=True)
    user_ids = set(list(sent_to_ids) + list(received_from_ids))
    users_with_chats = User.objects.filter(id__in=user_ids)
    chat_previews = []
    for user in users_with_chats:
        try:
            latest_message = Message.objects.filter(
                (Q(sender=current_user, receiver=user) | Q(sender=user, receiver=current_user))
            ).latest('timestamp')
        except Message.DoesNotExist:
            continue
        unread_count = Message.objects.filter(sender=user, receiver=current_user, is_read=False).count()
        chat_previews.append({
            'user': user,
            'latest_message_time': latest_message.timestamp,
            'unread_count': unread_count
        })
    chat_previews.sort(key=lambda x: x['latest_message_time'], reverse=True)
    all_users = current_user.profile.friends.all()
    # --- End of left panel data ---

    # --- Get the data for the active chat window ---
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user))
    )
    messages.filter(receiver=request.user).update(is_read=True)

    context = {
        'chat_previews': chat_previews,
        'all_users': all_users,
        'messages': messages,
        'other_user': other_user
    }
    
    return render(request, 'inbox.html', context)


@login_required
@require_POST # This decorator ensures that only POST requests can access this view.
def send_message(request, username):
    """
    Handles the submission of a new message from the chat window.
    """
    # Find the user who will receive the message.
    receiver = get_object_or_404(User, username=username)
    
    # Get the message content from the submitted form.
    # .strip() removes any leading/trailing whitespace.
    content = request.POST.get('content', '').strip()

    # Create and save the message only if there is actual content.
    if content:
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )

    # Redirect the user back to the same chat page they were on.
    return redirect('chat', username=username)