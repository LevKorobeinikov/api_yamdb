from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ProjectUser
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(ProjectUser)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'Поле не заполнено'
    list_editable = ('role',)
    list_filter = ('role', 'username',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = ('text',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date')
    search_fields = ('title', 'author', 'text')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'genres',
    )
    list_editable = ('year', 'category')
    filter_horizontal = ('genre',)

    @admin.display(
        description='Жанры',
    )
    def genres(self, obj):
        return ",\n".join([genres.name for genres in obj.genre.all()])
