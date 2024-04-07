from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Customer, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name', 'description')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'employee', 'total_amount', 'created_at')
    search_fields = ('customer__name', 'employee__username')
    inlines = [OrderItemInline]