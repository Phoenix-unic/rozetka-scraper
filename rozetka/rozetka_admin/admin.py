from django.contrib import admin
from .models import KeyWords, Links, ProductInfo

# Register your models here.



@admin.register(KeyWords)
class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_filter = ('status',)
    search_fields = ('name', )


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'status')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'current_price', 'link', 'reviews', 'features')
    search_fields = ('product_name', 'features')


