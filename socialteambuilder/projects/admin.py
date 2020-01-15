from django.contrib import admin

from .models import Project, Position, Application

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status')
    list_filter = ('status',)
    search_fields = ('title',)
    

class InlinePositionAdmin(admin.TabularInline):
    model = Position
    filter_horizontal = ('skills',)


class ProjectAdmin(admin.ModelAdmin):
   inlines = [InlinePositionAdmin,]


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'status', 'unread']
    list_editable = ['status', 'unread']

admin.site.register(Project, ProjectAdmin)

admin.site.register(Position, PositionAdmin)
admin.site.register(Application, ApplicationAdmin)
