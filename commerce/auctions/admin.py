from django.contrib import admin
from .models import User,Listings,Comment,Bid,Watchlist,Category
# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Category)
