from django.contrib import admin
from .models import *
# Register your models here

admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Reviews)
admin.site.register(Orders)