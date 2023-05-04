from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register',views.register, name='register'),
    path('login',views.login, name='login'),
    path('all_products',views.all_products,name='all_products'),
    path('about',views.about, name='about'),
    path('logout', views.logout, name='logout'),
    path('searchproduct',views.search_product,name='search_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('myorder',views.cart, name='order'),
    path('add_product/', views.add_product, name='add_product'),
    path('update', views.update_products, name='update_products'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),



    ]