from django.contrib import admin
from .models import Category, ShoppingList, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'family_group', 'created_by', 'created_at')
    list_filter = ('family_group', 'created_at')
    search_fields = ('name', 'family_group__name')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopping_list', 'category', 'is_checked', 'added_by', 'created_at')
    list_filter = ('shopping_list', 'category', 'is_checked', 'created_at')
    search_fields = ('name', 'shopping_list__name')