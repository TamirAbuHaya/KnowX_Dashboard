from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "role", "rank", "course_num", "battalion", "platoon", "team", "is_staff", "is_active")
    list_filter = ("role", "rank", "course_num", "battalion", "platoon", "team", "is_staff", "is_active")
    search_fields = ("email", "full_name")
