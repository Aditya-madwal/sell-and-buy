from django.urls import path, include
from myapp import views

urlpatterns = [
    path('register/', views.register_view, name = 'register'),
    path('login/', views.loginview, name = 'login'),
    path('', views.homeview, name = 'home'),
    path('cart/', views.cartview, name = 'cart'),
    path('upload/', views.upload_product, name = 'upload product'),
    path('product/<slug:code>', views.product_view, name = 'product'),
]

# invisible apis

urlpatterns += [
    path('logout/', views.logoutview, name = 'logout'),
    path('add_to_cart/<slug:code>', views.add_to_cart, name = 'add_product_to_cart'),
    path('increase_cart_quantity/<slug:cart_id>', views.increase_cart_quantity, name="increase_cart"),
    path('decrease_cart_quantity/<slug:cart_id>', views.decrease_cart_quantity, name="decrease_cart"),
    path('delete_from_cart/<slug:cart_id>', views.delete_from_cart, name="delete_from_cart")
]