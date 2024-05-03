from django.urls import path, include
from myapp import views

urlpatterns = [
    path('register/', views.register_view, name = 'register'),
    path('login/', views.loginview, name = 'login'),
    path('logout/', views.logoutview, name = 'logout'),
    path('', views.homeview, name = 'home'),
    path('cart/', views.cartview, name = 'cart'),
    path('upload/', views.upload_product, name = 'upload product'),
    path('add_to_cart/<slug:code>', views.add_to_cart, name = 'add product to cart'),
]

# invisible apis

urlpatterns += [
    # path('search/<slug:queryparam>', views.searchview, name = 'search'),
]