#GPT5.5 assisted in the creation of this code
'''Photoapp admin registration.

Registering Photo in the admin gives administrators a second, audited path to
manage ANY content -- consistent with the "administrators may edit/delete all
content" requirement. Access to the admin site already requires is_staff, which
Django enforces, so no extra access-control code is needed here.

It is also the simplest place to assign an owner to any legacy/fixture photos
that were created before the authentication feature existed.
'''

from django.contrib import admin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')
    list_filter = ('user',)
    search_fields = ('title', 'description')
