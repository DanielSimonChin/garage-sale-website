
from django.contrib import admin
from .models import User,Item,Comment,Reply
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Reply)

class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('id', 'date_joined','last_login')

    filter_horizontal= ()
    list_filter =()
    fieldsets = ()



