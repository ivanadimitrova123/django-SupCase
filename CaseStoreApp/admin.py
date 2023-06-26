from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['color', 'phone_type', 'material', ]
    search_fields = ['name', 'type']

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'created_at']


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', ]


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]


admin.site.register(CartItem, CartItemAdmin)
