from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Import messages to show feedback
from .forms import SignUpForm # Import your new form
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