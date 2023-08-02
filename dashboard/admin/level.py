from django.contrib import admin

from dashboard.models.level import *

@admin.register(Levels)
class LevelAdmin(admin.ModelAdmin):
    list_display = LEVELS_LIST_DISPLAY
