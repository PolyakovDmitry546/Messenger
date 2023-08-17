from django.contrib import admin
from django.contrib.admin.decorators import register

from . import models


class ChannelMembersInLine(admin.StackedInline):
    model = models.Membership


class ChannelMessageInLine(admin.StackedInline):
    model = models.Message


@register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [ChannelMembersInLine, ChannelMessageInLine]


admin.site.register(models.Membership)
