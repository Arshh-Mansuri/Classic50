from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.createlisting,name="createlisting"),
    path("listing",views.listing,name="listing"),
    path("listing/<int:id>",views.viewdetails,name="viewdetails"),
    path("addComment/<int:id>",views.addComment,name="addComment"),
    path("saveComment/<int:id>",views.saveComment,name="saveComment"),
    path("bid/<int:id>",views.MakeBid,name="MakeBid"),
    path("listing/<int:id>/addtoWatchlist",views.addtoWatchlist,name="addtoWatchlist"),
    path("listing/<int:id>/removefromWatchlist",views.removefromWatchlist,name="removefromWatchlist"),
    path("watchlist",views.viewWatchlist,name="viewWatchlist"),
    path("CloseBid\<int:id>",views.Inactive,name="Inactive"),
    path("viewCategory",views.viewCategory,name="viewCategory")


]
