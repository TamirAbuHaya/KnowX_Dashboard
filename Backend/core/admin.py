from django.contrib import admin
from .models import CourseBattalion

@admin.register(CourseBattalion)
class CourseBattalionAdmin(admin.ModelAdmin):
    list_display = ("battalion", "course_num", "start_date", "end_date", "commander")
    list_filter = ("battalion", "course_num")
    search_fields = ("battalion", "course_num", "commander__email", "commander__full_name")
