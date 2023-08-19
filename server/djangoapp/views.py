from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_template_view(request):
    return render(request, 'djangoapp/static_template.html')

# Create an `about` view to render a static about page
# def about(request):
# ...
def about_view(request):
    return render(request, 'djangoapp/about.html') 


# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')  # Redirect to the index page after login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return redirect('djangoapp:index')  # Redirect to the index page in case of GET request


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
from django.contrib.auth import logout

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')  # Redirect to the index page after logout


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    return render(request, 'djangoapp/registration.html')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        
        # Create user
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        
        # Log the user in
        login(request, user)
        
        # Redirect to the desired page (replace 'djangoapp:index' with your actual index page URL)
        return redirect('djangoapp:index')
    
    return render(request, 'djangoapp:index')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/e2697c10-fad8-4932-ace9-4b378f6ff2ab/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"https://eu-de.functions.appdomain.cloud/api/v1/web/e2697c10-fad8-4932-ace9-4b378f6ff2ab/dealership-package/get-review/{dealer_id}"
        # Get reviews for the dealer from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        # Create a string with formatted review information
        review_info = "\n".join([f"Review: {review.review}, Sentiment: {review.sentiment}" for review in reviews])
        
        # Return the review information as an HttpResponse
        return HttpResponse(review_info)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

