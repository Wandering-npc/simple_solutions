from django.contrib import admin
from .models import Item, Order, Discount, Tax, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'is_paid', 'created', 'updated')
    list_filter = ('is_paid', 'created')
    search_fields = ('id', 'customer__username')

    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)