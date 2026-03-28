from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Listing

# function to  load the main page

def index(request):
    if "listing" not in request.session: # wraps the reuest in sessions
        request.session["listing"] = []
     # passess the model to the main page
    return render(request, "auctions/index.html",{ 
        "listings":Listing.objects.all()
    })
# The request passes listing id to view everysingle listing
def listing(request,listing_id):
    listing =Listing.objects.get(id = listing_id)
    return render(request,"auctions/listing.html",{
        "listing":listing
    })

# form to add New Listings to the site
class NewListingForm(forms.Form):
    Name = forms.CharField(label="Product Name")
    cover =forms.FileField(label="Add Product Image")
    Starting_Bid = forms.IntegerField(label="Place Bid")
    Description = forms.CharField(label="Product Description")
    category =forms.CharField(label="Category")
    isActive =forms.BooleanField()
# function to add New Listing, request method is post
def add(request):
    if request.method =="POST":
        form =NewListingForm(request.POST,request.FILES)
        if form.is_valid():

            listing = Listing(
                Name =form.cleaned_data["Name"],
                Description =form.cleaned_data["Description"],
                Starting_Bid =form.cleaned_data["Starting_Bid"],
                cover=form.cleaned_data["cover"],
                Lister =request.user,
                category= form.cleaned_data["category"],
                isActive =True

            )
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))

    else:
        form=NewListingForm()
    return render(request,"auctions/add.html",{
        "form":form
    })

  




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
