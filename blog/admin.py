from django.contrib import admin
from . import models


# Register your models here.

class CommentInline(admin.StackedInline):
    model = models.Comment

    readonly_fields = (
        'name',
        'text',
        'email',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created',
        'updated',
    )

    list_filter = (
        'status',
        'topics',
    )

    prepopulated_fields = {'slug': ('title',)}

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    inlines = [
        CommentInline,
    ]


admin.site.register(models.Post, PostAdmin)


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'name',
        'email',
        'created',
        'updated',
    )

    list_filter = (
        'approved',
    )

    search_fields = (
        'name',
        'post__topics',
    )


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted'
    )
    # Make these fields read-only in the admin
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'message',
        'submitted'
    )