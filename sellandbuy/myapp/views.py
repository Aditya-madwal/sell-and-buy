from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import user_registeration_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

from .models import *

from rest_framework_simplejwt.authentication import JWTAuthentication

# ---------- USER REGISTRATION/LOGIN/LOGOUT -------------

def register_view(request) :
    form = user_registeration_form(request.POST)

    context = {
        'form' :form,
    }

    if request.method == 'POST' :
        if form.is_valid() :
            form.save()
        return redirect(loginview)

    return render(request, 'register.html', context=context)

def loginview(request) :
    if request.user.is_authenticated :
        return redirect(homeview)

    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        # this user is a user object and authenticate function is checking if username and password are valid as credentials or not ... if not then user = none

        if user is not None :
            # login into the website
            login(request, user)
            return redirect(homeview)
        else :
            # authentication failed
            messages.error(request, "username or password is incorrect")
            pass
    return render(request, 'login.html', {})

@login_required(login_url=loginview)
def logoutview(request) : 
    logout(request)
    return redirect(loginview)

# -------------- VISIBLE PAGES TO THE USER ----------------

@login_required(login_url = loginview)
def homeview(request) :
    if request.method == 'GET' :
        # obj = Product.objects.get(id = 10)
        # img_url = get_image_file_name(obj.image_field.url)
        # print(obj.image_field.url)

        products = Product.objects.all()


        if len(request.GET) > 0 :
            # there is some query
            query = request.GET['search']
            products = Product.objects.filter(name__icontains=query)
            pass
        else :
            # there is no query
            pass
        
        context = {
            'user' : request.user,
            'products' : products,
        }

        return render(request, 'home.html', context = context)
    
    if request.method == 'POST' :
        query = request.POST['query']
        # query_params = {'search': query}
        return redirect(reverse('home') + f'?search={query}')

@login_required(login_url=loginview)
def cartview(request) :
    user = request.user
    buyer = Buyer.objects.get(user = user)
    cart = Cart.objects.filter(buyer = buyer)
    total_payable = total_payable_at_cart(cart)

    total_products = count_items_in_cart(cart)[0]
    total_items = count_items_in_cart(cart)[1]

    context = {
        'buyer':request.user,
        'cart' : cart,
        'total_payable' : total_payable,
        'total_products' : total_products,
        'total_items' : total_items,
    }

    return render(request, 'cart.html', context = context)

from .forms import Product_form

@login_required(login_url=loginview)
def upload_product(request):

    user = request.user
    
    try:
        Seller.objects.get(user = user)
        pass
    except :
        return HttpResponse("<b>this is not a seller account.</b>")

    if request.method == 'POST':
        form = Product_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) # saved the form as a product instance of the Product model
            product.code = generate_random_code()
            product.seller = Seller.objects.get(user = request.user)
            product.save()
            return HttpResponse('done')  # Redirect to product list page
        else :
            return HttpResponse('naah')
    else:
        form = Product_form()
    return render(request, 'upload_product.html', {'form': form})



# -------------------- INVISIBLE CALLS -----------------------

@login_required(login_url=loginview)
def add_to_cart(request, code) :
    product = Product.objects.get(code = code)
    buyer = Buyer.objects.get(user = request.user)
    cart_obj = Cart.objects.create(product = product, buyer = buyer)
    cart_obj.quantity += 1
    cart_obj.save()

    return redirect(cartview)

# ----------------- BRAIN --------------------
import random
import string

def generate_random_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(7))
    return code

def get_image_file_name(file_path):
    path_parts = file_path.split('/')
    image_file_name = f"{path_parts[-2]}/{path_parts[-1]}"
    return image_file_name

def total_payable_at_cart(cart) :
    total = 0
    for i in cart :
        total += i.product.price * i.quantity
    return total

def count_items_in_cart(cart) :
    total_products = 0
    total_items = 0

    for i in cart :
        total_products += 1
        total_items += i.quantity
    
    return [total_products, total_items]
