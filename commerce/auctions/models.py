from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    pass



class Category(models.Model):
    name=models.CharField(max_length=32,unique=True)

    def __str__(self) :
        return f"{self.name}"

class Listings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="lister")
    title = models.CharField(max_length=64)
    isActive=models.BooleanField(default=True)
    story = models.CharField(max_length=500)
    price  = models.IntegerField()
    imageurl=models.CharField(max_length=200)
    ytlink=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="listing_category")

    def __str__(self):
        return f"{self.title} by {self.user}"
    




class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="commentedBy")
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE, related_name="listing")
    comment=models.CharField(max_length=300)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
    

class Bid(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="BidBy")
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE, related_name="BidOn")
    bid=models.ImageField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing} "

    class Meta:
        unique_together = ('user', 'listing')