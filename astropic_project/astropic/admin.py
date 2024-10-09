from django.contrib import admin
from .models import Photo, Comment, Like, AstronomicalEvent

# Configuración para el modelo Photo
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'event', 'like_count')
    list_filter = ('user', 'event', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'like_count')

    def like_count(self, obj):
        return obj.like_count()
    like_count.short_description = 'Likes'

# Configuración para el modelo Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'comment', 'created_at')
    list_filter = ('user', 'photo', 'created_at')
    search_fields = ('user__username', 'photo__title', 'comment')
    readonly_fields = ('created_at',)

# Configuración para el modelo Like
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    list_filter = ('user', 'photo', 'created_at')
    search_fields = ('user__username', 'photo__title')
    readonly_fields = ('created_at',)

# Configuración para el modelo AstronomicalEvent
@admin.register(AstronomicalEvent)
class AstronomicalEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date')
    list_filter = ('event_date',)
    search_fields = ('name', 'description')
