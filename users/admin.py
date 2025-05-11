from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'full_name', 'is_school', 'school_name',
        'university_name', 'is_staff', 'is_superuser'
    )
    list_filter = ('is_school', 'is_staff', 'is_superuser', 'gender')
    search_fields = ('email', 'full_name', 'school_name', 'university_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': (
            'full_name', 'date_of_birth', 'gender', 'is_school',
            'school_name', 'grade', 'college_year', 'university_name'
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'full_name', 'date_of_birth', 'gender', 'is_school',
                'school_name', 'grade', 'college_year', 'university_name',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )

    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
