from django.contrib import admin
from .models import *


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('corfirmed_order_id','product','user','quantity','price','ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','mobile_no','email','order_total','status','is_ordered','created_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','email','city','district']
    list_per_page = 20
    inlines = [OrderProductInline]


# Register your models here.

# admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Confirm_order)