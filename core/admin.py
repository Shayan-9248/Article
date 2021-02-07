from django.contrib import admin
from .models import *
import admin_thumbnails


def make_published(modeladmin, request, queryset):
    queryset.update(status='Published')
make_published.short_description = "Mark selected stories as published"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='Draft')
make_published.short_description = "Mark selected stories as draft"


class ArticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish',
     'get_visit_count', 'created', 'updated', 'is_special',
      'status', 'category_to_str', 'brand', 'image_tag')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('publish',)
    date_hierarchy = ('publish')
    actions = (make_published, make_draft)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_category', 'is_sub')
    list_filter = ('is_sub',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(IPAddress)
admin.site.register(Brand)

