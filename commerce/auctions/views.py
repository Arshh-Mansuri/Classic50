from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Listings,Comment,Watchlist,Category


def index(request):
    listings=Listings.objects.all()
    categories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":listings,
        "categories":categories
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


def createlisting(request):
    categories=Category.objects.all()
    return render(request,"auctions/createlisting.html",{
        "categories":categories
    })

def listing(request):
    if request.method=="POST":
         title = request.POST["title"]
         price = request.POST["price"]
         story = request.POST["story"]
         imageurl = request.POST["imageurl"]
         ytlink=request.POST["ytlink"]
         selected_category_id = request.POST.get('category')

    category=Category.objects.get(id=selected_category_id) if selected_category_id else None
    current_user = request.user
    newlisting=Listings(user=current_user,title=title,price=price,story=story,imageurl=imageurl,ytlink=ytlink,category=category)
    newlisting.save()

    return HttpResponseRedirect(reverse('index'))

def viewdetails(request,id):
    listing=Listings.objects.get(id=id)
    category=listing.category.name
    title=listing.title
    user=listing.user
    imageurl=listing.imageurl
    ytlink=listing.ytlink
    story=listing.story
    price=listing.price
    is_in_watchlist=Watchlist.objects.filter(user=request.user, listing=listing).exists()

    check=(listing.user)==request.user

    # if(check):
    #     listing.isActive=not(listing.isActive)
    #     listing.save()

    comments=Comment.objects.filter(listing=listing)
    return render(request,"auctions/details.html",{
        "title":title,
        "user":user,
        "imageurl":imageurl,
        "ytlink":ytlink,
        "story":story,
        "id":id,
        "comments":comments,
        "price":price,
        "is_in_watchlist":is_in_watchlist,
        "check":check,
        "category":category

    })

def addComment(request,id):
    return render(request,"auctions/comment.html",{
        "id":id
    })

@login_required
def saveComment(request,id):
    if request.method=="POST":
         comment = request.POST["comment"]
    current_user = request.user
    listing=Listings.objects.get(id=id)
    newComment=Comment(user=current_user,listing=listing,comment=comment)
    newComment.save()


    title=listing.title
    price=listing.price
    imageurl=listing.imageurl
    ytlink=listing.ytlink
    story=listing.story
    comments=Comment.objects.filter(listing=listing)
    return render(request,"auctions/details.html",{
        "title":title,
        "user":current_user,
        "imageurl":imageurl,
        "ytlink":ytlink,
        "story":story,
        "id":id,
        "price":price,
        "comments":comments,
    })

def MakeBid(request,id):
    if request.method=="POST":
        newBid=request.POST["newBid"]
    f=Listings.objects.get(pk=id)
    if(int(newBid)<=int(f.price)):
        return HttpResponseRedirect(reverse("viewdetails",args=[id]))
    else:
        f.price=int(newBid)
        f.save()
        return HttpResponseRedirect(reverse("viewdetails",args=[id]))
    
@login_required
def addtoWatchlist(request,id):
    listing = get_object_or_404(Listings, pk=id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    return HttpResponseRedirect(reverse('index'))
@login_required  
def removefromWatchlist(request,id):
    listing = get_object_or_404(Listings, pk=id)
    watchlist_item=Watchlist.objects.get(user=request.user, listing=listing)
    watchlist_item.delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
def viewWatchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('listing')
    return render(request, 'auctions/Watchlist.html', {'watchlist_items': watchlist_items})


@login_required
def Inactive(request,id):
    listing=get_object_or_404(Listings, pk=id)
    check=(listing.user)==request.user
    if check:
        listing.isActive=False
        listing.save()
    return HttpResponseRedirect(reverse('index'))



def viewCategory(request):
    if request.method=="POST":
        category=request.POST["category"]

    category=Category.objects.get(pk=category)
    
    
    items=(Listings.objects.filter(category=category))
    
    return render(request,"auctions/viewCategory.html",{
        "category":category,
        "items":items
    })