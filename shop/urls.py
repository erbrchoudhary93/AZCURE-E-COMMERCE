
from . import views
from django.urls import path
from shop.views import index

urlpatterns = [
   path("", views.index, name="ShopHome"),
   path("about/", views.about, name="AboutUs"),
   path("contact/", views.contact, name="ContactUs"),
   path("tracker/", views.tracker, name="TrackingStatus"),
   path("search/", views.search, name="Search"),
   path("products/<int:myid>", views.productView, name="ProductView"),
   path("checkout/", views.checkout, name="Checkout"),
   path("handlepayment", views.handlepayment, name="handlepayment"),
   
]
