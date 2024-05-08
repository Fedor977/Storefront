from django.contrib import admin
from store.models import Product
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.


class TaggedItemInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItemInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
