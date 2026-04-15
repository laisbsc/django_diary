from django.contrib import admin

from .models import GeneratedImage


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ('prompt_preview', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('created_at',)

    def prompt_preview(self, obj):
        return obj.prompt[:60]
    prompt_preview.short_description = 'Prompt'
