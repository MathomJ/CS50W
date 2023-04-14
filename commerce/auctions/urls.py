from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("item_page", views.item_page, name="item_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist-rm", views.watchlist_rm, name="watchlist-rm"),
    path("new-bid", views.new_bid, name="new-bid")
]
