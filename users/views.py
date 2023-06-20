# users/views.py
#
# import users.forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import NewUserForm


def dashboard(request):
    return render(request, "dashboard.html")


def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    if request.method == 'POST':

        # Process the request if posted data are available
        username = request.POST['Username']
        password = request.POST['Password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to log in the user
            login(request, user)
            # Success, now let login the user.
            return render(request, 'dashboard.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login01.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login01.html')


# Create your views here.

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})
