from django.contrib import admin

from products.admin import BasketAdmin
from users.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'is_staff', 'is_superuser']
    inlines = (BasketAdmin,)