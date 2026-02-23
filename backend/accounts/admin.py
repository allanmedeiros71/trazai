from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FamilyGroup

@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('family_group',)
    list_filter = UserAdmin.list_filter + ('family_group',)
    fieldsets = UserAdmin.fieldsets + (
        ('Family', {'fields': ('family_group',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Family', {'fields': ('family_group',)}),
    )