from django.contrib import admin

from .models import About, Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'published_date', 'read_time')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('read_time', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'category', 'location')}),
        ('Content', {'fields': ('body', 'excerpt', 'cover_image')}),
        ('Publishing', {'fields': ('is_featured', 'published_date', 'read_time', 'updated_at')}),
    )


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fields = ('body',)
