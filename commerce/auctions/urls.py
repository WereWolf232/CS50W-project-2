from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("categories",views.categories_page, name="categories_page"),
    path("categories/<str:name>",views.categories_specific, name="categories_specific")
]
