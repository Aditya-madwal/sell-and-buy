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
            
            role = request.POST['role']
            username = request.POST['username']
            user = User.objects.get(username = username)

            if role == "sell" :
                s = Seller.objects.create(user = user)
                s.save()
            else :
                b = Buyer.objects.create(user = user)
                b.save()


        return redirect(loginview)

    return render(request, 'register.html', context=context)

def loginview(request) :
    if request.user.is_authenticated :
        return redirect(homeview)

    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

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


@login_required(login_url=loginview)
def product_view(request, code) :
    product = Product.objects.get(code = code)
    added_to_cart = 0
    buyer = Buyer.objects.get(user = request.user)

    reviews = Reviews.objects.filter(product = product)


    cart = Cart.objects.filter(product = product,buyer = buyer)
    if len(cart) == 0 :
        # exists in the cart
        added_to_cart = 1
        pass
    else :
        # does not exists
        pass

    months_list = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
    ]

    context = {
        'product' : product,
        'added' : added_to_cart,
        'reviews' : reviews,
        'months' : months_list,
        'function' : monthname,
        'ratings' : analyse_ratings(product),
        'reviews_exists' : False,
        'avg_rating' : average_rating(product),
    }

    if request.method == 'POST' :
        review = request.POST['review-statement']
        stars = request.POST['rating']
        provider = Buyer.objects.get(user = request.user)
        Reviews.objects.create(product = product,review = review, stars = stars, provider = provider).save()

        return redirect(product_view, code = product.code)

    return render(request, 'product.html', context = context)
    


# -------------------- INVISIBLE CALLS -----------------------

@login_required(login_url=loginview)
def add_to_cart(request, code) :
    product = Product.objects.get(code = code)
    buyer = Buyer.objects.get(user = request.user)
    cart = Cart.objects.filter(buyer = buyer)

    for i in cart :
        if product.code == i.product.code :
            cart_obj = Cart.objects.get(product = product)
            cart_obj.quantity += 1
            cart_obj.save()
            return redirect(cartview)
        pass

    cart_obj = Cart.objects.create(product = product, buyer = buyer)
    cart_obj.quantity = 1
    cart_obj.save()

    return redirect(cartview)

@login_required(login_url=loginview)
def increase_cart_quantity(request, cart_id) :
    cart_product = Cart.objects.get(id = cart_id)
    cart_product.quantity += 1
    cart_product.save()
    return redirect(cartview)

@login_required(login_url=loginview)
def decrease_cart_quantity(request, cart_id) :
    cart_product = Cart.objects.get(id = cart_id)
    if cart_product.quantity == 1 :
        cart_product.delete()
    else :
        cart_product.quantity -= 1
        cart_product.save()
    return redirect(cartview)

@login_required(login_url=loginview)
def delete_from_cart(request, cart_id) :
    cart_product = Cart.objects.get(id = cart_id)
    cart_product.delete()
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

def monthname(month) :
    return f"this is {month}"

def analyse_ratings(product) :
    certain_reviews = Reviews.objects.filter(product = product)

    if len(certain_reviews) == 0 :
        return "no reviews yet"

    total_reviews = len(certain_reviews)

    five_stars = 0
    four_stars = 0
    three_stars = 0
    two_stars = 0
    one_stars = 0

    for i in certain_reviews :
        if i.stars == 5 :
            five_stars += 1
        elif i.stars == 4 :
            four_stars += 1
        elif i.stars == 3 :
            three_stars += 1
        elif i.stars == 2 :
            two_stars += 1
        elif i.stars == 1 :
            one_stars += 1
    
    five_stars = (five_stars/total_reviews)*100
    four_stars = (four_stars/total_reviews)*100
    three_stars = (three_stars/total_reviews)*100
    two_stars = (two_stars/total_reviews)*100
    one_stars = (one_stars/total_reviews)*100

    return [five_stars,four_stars,three_stars,two_stars,one_stars]

def average_rating(product) :
    certain_reviews = Reviews.objects.filter(product = product)

    if len(certain_reviews) == 0 :
        print(f"this is {certain_reviews}")
        return 0

    rating = 0
    for i in certain_reviews :
        rating += i.stars
    
    return int(rating/len(certain_reviews))