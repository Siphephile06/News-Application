from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter, ResetToken


# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups',
                                    'user_permissions')}),
        ('Subscriptions', {'fields': ('subscriptions_to_publishers',
                                      'subscriptions_to_journalists')}),
        ('Publishing', {'fields': ('published_articles',
                                   'published_newsletters')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role',
                       'is_staff', 'is_active')}
    ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


# Register other models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)
admin.site.register(ResetToken)
