from django.contrib import admin
from store.models import Store, Order, OrderItem

# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'created_at']

    class Meta:
        model = Store


admin.site.register(Store, StoreAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_no']

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order', 'selling_price']

    class Meta:
        model = OrderItem


admin.site.register(OrderItem, OrderItemAdmin)

