from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Bio, Account, Blog

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','created')
    list_filter = ()
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Bio)