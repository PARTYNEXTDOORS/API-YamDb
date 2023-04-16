from django.contrib import admin

from .models import Comment, Review, Category, Genre, Title


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'pub_date',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
