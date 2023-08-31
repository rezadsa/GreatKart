from typing import Any, Optional
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from store.models import Product,Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display=('name','price','stock','category','created_date','modified_date','is_available')

    ordering=('-modified_date','-created_date')

admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','created_date','is_active')
    list_filter=('product__category','product__name')
    ordering=('product__category','product__name')
    list_editable=('is_active',)
    search_fields=('product__name',)
    filter_horizontal=()
    fieldsets=()


admin.site.register(Variation,VariationAdmin)