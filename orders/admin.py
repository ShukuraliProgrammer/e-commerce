from django.contrib import admin

from orders.models import *
# Register your models here.

admin.site.register(CartItem)
admin.site.register(Card)
admin.site.register(Discount)
admin.site.register(Branch)
admin.site.register(DeliveryTariff)
admin.site.register(Order)