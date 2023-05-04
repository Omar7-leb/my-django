from django.shortcuts import render,redirect,  get_object_or_404
from django.http import HttpResponse
from django.forms import modelform_factory
from .models import *
from django.contrib.auth.models import User , auth
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
#from .models import FarmerRequest

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
       username = request.POST['username']
       email = request.POST['email']
       phone = request.POST['phone']
       password = request.POST['pass1']
       password2 = request.POST['pass2']
       if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return render(request,'index.html')
       else:
            messages.info(request, 'Password is not the same')
            return redirect('register')
    else:
          return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    return render(request, 'login.html')

def products(request):
    return render(request,'all_products.html')

def about(request):
    return render(request,'about.html')

def all_products(request):
    products =Product.objects.all()
    return render(request, 'all_products.html',{'products': products})

# @login_required
# def view_order(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         client = request.user.client  # Assuming client is related to User model using a one-to-one relationship
#         if order.client == client:
#             order_items = OrderDetail.objects.filter(order=order)
#             context = {
#                 'order': order,
#                 'order_items': order_items,
#             }
#             return render(request, 'orders/view_order.html', context)
#         else:
#             return HttpResponse("You are not authorized to view this order.")
#     except Order.DoesNotExist:
#         return HttpResponse("Order does not exist.")

def logout(request):
    auth.logout(request)
    print('Logout')
    return redirect('/login')

def search_product(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        products = Product.objects.filter(category__contains=request.GET['category'])
        context = {
            'products': products,
            'category': category
        }
        return render(request, 'searchproducts.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')
    return redirect('all_products')

def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.unit_price* quantity
        products.append({'product': product, 'quantity': quantity})
    return render(request, 'myorder.html', {'products': products, 'total_price': total_price})

def add_product(request):
    if request.method == 'POST':
        form = Product(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = Product()
    return render(request, 'add_product.html', {'form': form})

def update_products(request):
    products =Product.objects.all()
    return render(request, 'update.html',{'products': products})

def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    ProductForm = modelform_factory(Product, fields=('name', 'description', 'price', 'category', 'image'))
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product_id)

    return render(request, 'update.html', {'form': form, 'product': product})

def delete_product(request, id):
    # Get the product object with the given id
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        # Delete the product from the database
        product.delete()
        return redirect('product_list') # Redirect to product list page
    else:
        return render(request, 'delete_product.html', {'product': product})