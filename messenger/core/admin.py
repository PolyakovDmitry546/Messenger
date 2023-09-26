from django.contrib import admin
from django.contrib.admin.decorators import register

from . import models


class ChannelMembersInLine(admin.StackedInline):
    model = models.ChannelMembership


class ChannelMessageInLine(admin.StackedInline):
    model = models.ChannelMessage


class DialogMembersInLine(admin.StackedInline):
    model = models.DialogMembership


class DialogMessageInLine(admin.StackedInline):
    model = models.DialogMessage


@register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [ChannelMembersInLine, ChannelMessageInLine]


@register(models.Dialog)
class DialogAdmin(admin.ModelAdmin):
    inlines = [DialogMembersInLine, DialogMessageInLine]


admin.site.register(models.ChannelMembership)
admin.site.register(models.DialogMembership)
