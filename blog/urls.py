
from . import views
from django.urls import path

urlpatterns = [
   path("", views.index, name="ShopBlog"),
   path("blogpost/<int:id>",views.blogpost,name="blogpost")
   
]