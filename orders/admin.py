from django.contrib import admin

from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'created')
    list_filter = ('paid', 'created')
    search_fields = ('email', 'address')
    readonly_fields = ('created', 'updated')