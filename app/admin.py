from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'city', 'state')
    list_filter = ('user_type', 'state')
    search_fields = ('username', 'email', 'first_name', 'last_name')