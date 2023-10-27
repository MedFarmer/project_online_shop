from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'textile')
    fields = (('name', 'price'), 'textile')
    readonly_fields = ('textile',)
    search_fields = ('name', 'price')
    list_display_links = ('textile',)
    listl_editable = ('name', 'price')
    list_filter = ('textile',)    

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Stock)
admin.site.register(Textile)
admin.site.register(Size)
admin.site.register(Color)
