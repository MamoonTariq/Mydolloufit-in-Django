from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="ShopAbout"),
    path('products/<int:myid>', views.productView ,name="ProductView"),
    path('contact/', views.contactUs, name="contactUS"),
    path('checkout', views.checkout, name="ChecKOut"),
    path('tracker', views.tracker, name="Tracker"),
]
