from django.contrib import admin

from .models import Project, Position, Application

class PositionAdmin(admin.TabularInline):
    model = Position

    filter_horizontal = ('skills',)

class ProjectAdmin(admin.ModelAdmin):
   inlines = [PositionAdmin,]

admin.site.register(Project, ProjectAdmin)

admin.site.register(Position)
admin.site.register(Application)
