from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *



def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
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


@login_required
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


# Create new auction listing
@login_required
def create(request):
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            new_listing = Listing()
            new_listing.poster = request.user
            new_listing.item = form.cleaned_data["item"]
            new_listing.category = form.cleaned_data["category"]
            new_listing.description = form.cleaned_data["description"]
            new_listing.image = form.cleaned_data["image"]
            new_listing.starting_price = form.cleaned_data["starting_bid"]
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

    # GET
    else:
        return render(request, "auctions/create.html", {
                "form": CreatePageForm()
            })


# Listing page
def listing(request, id):

    # Determining lowest possible bid
    listing = Listing.objects.get(id=id)
    if listing.current_bid == None:
        min = listing.starting_price
    else:
        min = listing.current_bid.amount+1

    bid_form = BidForm(min_value=min)
    bid_form.fields['bid'].widget.attrs['min'] = str(min)

    # POST method for bidding function
    if request.method == "POST":
        form = BidForm(request.POST,min_value=min)
        if form.is_valid():
            # Adding new bid
            new_bid = Bid(amount = form.cleaned_data["bid"], bidder = request.user)
            new_bid.save()
            # Updating current bid
            listing = Listing.objects.get(id=id)
            listing.current_bid = new_bid
            listing.save()

        return HttpResponseRedirect(reverse("listing", args=[id]))

    # Displaying Listing
    else:
        # Getting the watchlist of a specific person to know if the button is to add or remove
        watch_list = None
        if request.user.is_authenticated:
            saved = Watchlist.objects.filter(person=request.user)
            watch_list = [page.listing for page in saved]

        return render(request, "auctions/listing.html",
                    {"Listing": listing,
                    "comments" : Comment.objects.filter(listing=listing),
                    "comment_form" : CommentForm(),
                    "watchlist" : watch_list,
                    "bid_form" : bid_form,
                    "user" : request.user})


# Posting comments
@login_required
def comment(request,id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment()
            new_comment.author = request.user
            new_comment.content = form.cleaned_data["content"]
            new_comment.listing = Listing.objects.get(id=id)
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def close_auction(request,id):
    # Close auction
    listing = Listing.objects.get(id=id)
    listing.ongoing = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        action = request.POST['mod_watchlist']
        
        # Deleting from watchlist
        if action == "Remove From Watchlist":
            Watchlist.objects.get(listing__id=listing_id, person=request.user).delete()

        # Saving page to watchlist
        else:
            Watchlist(listing=Listing.objects.get(id=listing_id), person=request.user).save()

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        return render(request, "auctions/watchlist.html", {
            "list" : Watchlist.objects.filter(person=request.user)
        })



# Display all items in a specific category
def categories_specific(request, name):
    listings = Listing.objects.filter(category=name[0], ongoing=True)
    return render(request, "auctions/category.html", {
            "listings" : listings,
            "category" : name
        })

# Display all categories
def categories_page(request):
    category_list = [category[1] for category in categories_list]
    return render(request, "auctions/categories.html", {
            "categories" : category_list
        })