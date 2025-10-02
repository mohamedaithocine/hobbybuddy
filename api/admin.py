from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user, hobbies, friends

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('hobbies', 'groups', 'user_permissions')

    # Custom fieldsets for the user detail view
    fieldsets = (
        ('Account Details', {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Hobbies', {'fields': ('hobbies',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )


admin.site.register(user, CustomUserAdmin)
admin.site.register(hobbies)
admin.site.register(friends)