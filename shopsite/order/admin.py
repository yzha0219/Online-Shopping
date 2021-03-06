from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display_links = ['status_order']
    list_display = ['owner', 'status_order',  'created', 'updated']
    list_filter = ['owner', 'status_order', 'created', 'updated']
    list_editable = ['status_order']
    inlines = [OrderItemInline]
#
#
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'status_delivery', 'price', 'quantity']
#     list_editable = ['status_delivery']




