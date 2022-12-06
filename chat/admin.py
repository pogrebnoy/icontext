from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ChatMessages)
class ChatAdmin(admin.ModelAdmin):
    ...
