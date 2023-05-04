from django.contrib import admin
from .models import Farmer,Client,Product,Order,OrderDetail
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'dob', 'nationality', 'user')
    list_filter = ('nationality',)
    search_fields = ('name', 'phone', 'nationality')
    ordering = ('name',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'user')
    search_fields = ('name', 'phone', 'address')
    ordering = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'quantity_in_stock', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    ordering = ('name',)

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_ordered', 'payment_method')
    list_filter = ('payment_method',)
    search_fields = ('client__name',)
    ordering = ('-date_ordered',)
    inlines = (OrderDetailInline,)

admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
