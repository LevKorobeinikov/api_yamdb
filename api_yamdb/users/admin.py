from django.contrib import admin

from .models import ProjectUser


@admin.register(ProjectUser)
class UserAdmin(admin.ModelAdmin):
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
    list_filter = ('username',)
