from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Listings
from .models import Category
from .models import Bids

def index(request):
    list_of_listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "list_of_listings": list_of_listings
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

def add_listing(request):
    if request.method == "GET":
        c = Category.objects.all()
        return render(request, "auctions/add_listing.html", {
            "categories": c
        })
    if request.method == "POST":
        category = request.POST['category']
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        url = request.POST['img_url']

        l = Listings(title=title, description=description, price=price, imageUrl=url)
        c = Category(cat_name=category)
        l.save()
        c.save()

        return HttpResponseRedirect(reverse("index"))
    
def item_page(request):
    if request.method == "POST":
        title = request.POST['item_name']
        list = find_list(title)
        current_user = request.user

        if request.user.is_authenticated:
            listings = current_user.watchlistListing.all()
            isListingInWatchlist = list in listings
        else:
            isListingInWatchlist = None
        return render(request, "auctions/item_page.html", {
            "list": list,
            "isListingInWatchlist":isListingInWatchlist,
            "user":current_user
        })

    if request.method == "GET":
        list = find_list(title)
        current_user = request.user
        listings = current_user.watchlistListing.all()
        isListingInWatchlist = list in listings
        return render(request, "auctions/item_page.html", {
            "list": list,
            "isListingInWatchlist":isListingInWatchlist
        })
        

def find_list(title):
    for listing in Listings.objects.all():
            if listing.title == title:
                return listing

def watchlist(request):
    if request.method == "POST":
        title = request.POST['post_title']
        current_user = request.user
        #list = Listings.objects.filter(title=title)
        list = find_list(title)
        list.watchlist.add(current_user)
        listings = current_user.watchlistListing.all()
        isListingInWatchlist = list in listings
        return render(request, "auctions/item_page.html", {
            "list": list,
            "isListingInWatchlist":isListingInWatchlist
        })
        
    if request.method == "GET":
        list = Listings.objects.all()
        current_user = request.user
        listings = current_user.watchlistListing.all()
        return render(request, "auctions/watchlist.html", {
            "list":listings,
            "current_user":current_user
        })
    
def watchlist_rm(request):
    if request.method == "POST":
        title = request.POST["post_title"]
        list = find_list(title)
        current_user = request.user
        list.watchlist.remove(current_user)
        listings = current_user.watchlistListing.all()
        isListingInWatchlist = list in listings
        return render(request, "auctions/item_page.html", {
            "list": list,
            "isListingInWatchlist":isListingInWatchlist
        })

def new_bid(request):
    if request.method == "POST":
        title = request.POST['title']
        newBid = request.POST['new_bid']
        listing = find_list(title)
        og_bid = listing.price
        if float(newBid) > float(og_bid):
            Bids(bid=newBid).save()
            return render(request, "auctions/item_page.html", {
                "list":listing
            })
        else:
            error_message = "New bid must be more than the current bid."
            return render(request, "auctions/error.html", {
                "error_message":error_message
            })
        

