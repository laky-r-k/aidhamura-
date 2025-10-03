from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Import messages to show feedback
from .forms import SignUpForm ,UserEditForm, ProfileEditForm # Import your new form
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q 
import cloudinary
import cloudinary.uploader
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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Instantiate the form for User model fields (username, email, etc.)
        user_form = UserEditForm(request.POST, instance=request.user)
        
        # Instantiate the form for Profile model fields (bio, location)
        # We do NOT pass request.FILES here because we are handling the upload manually.
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)

        # Check if the data for both forms is valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user and profile form data (but not the image yet)
            user_form.save()
            profile = profile_form.save(commit=False)

            # --- CUSTOM CLOUDINARY UPLOAD LOGIC ---
            # Check if a new image file was included in the form submission
            if 'profile_picture' in request.FILES:
                image_file = request.FILES['profile_picture']
                
                try:
                    # Use the cloudinary.uploader to send the file directly to your account
                    print("Uploading image to Cloudinary...")
                    upload_result = cloudinary.uploader.upload(image_file)
                    
                    # The 'secure_url' is the permanent https:// address of the uploaded image
                    image_url = upload_result.get('secure_url')
                    
                    # Save that URL string to the profile_picture field in our model
                    profile.profile_picture = image_url
                    print("Image uploaded successfully. URL:", image_url)
                    
                except Exception as e:
                    # If the upload fails for any reason, show an error and stop.
                    messages.error(request, f"Error uploading image: {e}")
                    return redirect('edit_profile')
            # --- END OF CUSTOM LOGIC ---

            # Now, save the profile instance to the database with the new image URL (if any)
            profile.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        # For a GET request, create the forms pre-filled with the user's current data
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    # Pass both forms to the template so they can be displayed
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', context)





def search_results_view(request):
    """
    Handles the user search functionality.
    """
    # Get the search term from the URL's query parameters (e.g., /search/?q=laky)
    query = request.GET.get('q')
    
    if query:
        # If a query was provided, filter the User model.
        # This looks for the query in the username, first_name, OR last_name fields.
        # The 'icontains' makes the search case-insensitive.
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    else:
        # If no query is provided, return an empty list of results.
        results = User.objects.none()

    context = {
        'query': query,
        'results': results,
    }
    # Render the page that will display the results.
    return render(request, 'results.html', context)
