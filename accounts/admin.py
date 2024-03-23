from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import *

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number')


@admin.register(VerifictionOtp)
class VerificationOtp(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'expires_in']


@admin.register(UserAddress)
class UserAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'street']
