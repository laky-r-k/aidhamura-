from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Import messages to show feedback
from .forms import SignUpForm ,ProfileUpdateForm# Import your new form
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
def login_view(request):
    # Handle GET request: Show the login page
    if request.method == 'GET':
        return render(request, 'login.html')

    # Handle POST request: Process the login attempt
    elif request.method == 'POST':
        # Use .get() for safety to avoid crashing
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("landing_page") # Redirect to your home page
        else:
            # Failed login: Re-render the page with an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login') # Redirect to the home page after logout


def signup_view(request):
    # If the request is a POST, process the form data
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # Save the new user to the database
            login(request, user) # Log the user in automatically
            messages.success(request, "Registration successful! Welcome.")
            return redirect('landing_page') # Redirect to your home page
        else:
            # If the form is invalid, show errors
            messages.error(request, "Please correct the errors below.")
    # If it's a GET request, just display a blank form
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form': form})




@login_required
def profile_view(request, username):
    # Use get_object_or_404 to handle cases where the user doesn't exist
    profile_user = get_object_or_404(User, username=username)
    
    context = {
        'profile_user': profile_user
    }
    return render(request, 'profile.html', context)
@login_required
def remove_friend(request, username):
    # Find the user profile to remove from the friends list
    other_user = get_object_or_404(User, username=username)
    
    # Remove the other user from the current user's friend list
    request.user.profile.friends.remove(other_user.profile)
    
    # Optional: If you want the friendship to be removed both ways
    other_user.profile.friends.remove(request.user.profile)
    
    messages.success(request, f"You are no longer friends with {username}.")
    
    return redirect('profile', username=username)


@login_required
def add_friend(request, username):
    # Find the user profile to add to the friends list
    other_user = get_object_or_404(User, username=username)

    # Prevent users from adding themselves
    if other_user == request.user:
        messages.warning(request, "You cannot add yourself as a friend.")
        return redirect('profile', username=username)

    # Add the other user to the current user's friend list
    request.user.profile.friends.add(other_user.profile)
    
    # Make the friendship symmetrical (they also add you)
    other_user.profile.friends.add(request.user.profile)
    
    messages.success(request, f"You are now friends with {username}!")
    
    return redirect('profile', username=username)

login_required
def edit_profile(request):
    if request.method == 'POST':
        # The form is pre-filled with the user's current profile data
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context)