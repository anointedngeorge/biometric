from django.contrib import admin
from dashboard.models.courses import *





@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    list_display = COURSE_LIST_DISPLAY

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        qs = queryset.filter(lecturer_id=request.user.id)
        return qs