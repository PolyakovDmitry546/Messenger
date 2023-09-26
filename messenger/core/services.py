from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Channel, ChannelMembership, Dialog, DialogMembership, Message


class ChannelService:
    def __init__(self, user: User, channel_pk: int) -> None:
        self.user = user
        self.channel = Channel.objects.get(pk=channel_pk)

    def get_message_count(self) -> int:
        return self.channel.messages.count()

    def get_messages(self, page: int = None, per_page: int = None) -> QuerySet[Message]:
        if page is None or per_page is None:
            return self.channel.messages.all()

        bottom = page * per_page
        top = (page + 1) * per_page
        return self.channel.messages.all()[bottom:top]


class ChannelMessagesPageService:
    def __init__(self, user: User, channel_pk: int, page: int | None, per_page: int | None) -> None:
        self._channel_service = ChannelService(user, channel_pk)
        self._per_page = per_page if per_page else 20
        if page is None:
            membership = ChannelMembership.objects.get(user=self._channel_service.user,
                                                       chat=self._channel_service.channel)
            self._page = membership.get_number_page_with_last_read_message(self._per_page)
        else:
            self._page = page

    def get_page(self) -> int:
        return self._page

    def get_next_page(self) -> int | None:
        if (self._page + 1) * self._per_page < self._channel_service.get_message_count():
            return self._page + 1
        return None

    def get_messages(self) -> QuerySet[Message]:
        return self._channel_service.get_messages(self._page, self._per_page)


class DialogService:
    def __init__(self, user: User, dialog_pk: int) -> None:
        self.user = user
        self.dialog = Dialog.objects.get(pk=dialog_pk)

    def get_message_count(self) -> int:
        return self.dialog.messages.count()

    def get_messages(self, page: int = None, per_page: int = None) -> QuerySet[Message]:
        if page is None or per_page is None:
            return self.dialog.messages.all()

        bottom = page * per_page
        top = (page + 1) * per_page
        return self.dialog.messages.all()[bottom:top]


class DialogMessagesPageService:
    def __init__(self, user: User, dialog_pk: int, page: int | None, per_page: int | None) -> None:
        self._dialog_service = DialogService(user, dialog_pk)
        self._per_page = per_page if per_page else 20
        if page is None:
            membership = DialogMembership.objects.get(user=self._dialog_service.user,
                                                      chat=self._dialog_service.dialog)
            self._page = membership.get_number_page_with_last_read_message(self._per_page)
        else:
            self._page = page

    def get_page(self) -> int:
        return self._page

    def get_next_page(self) -> int | None:
        if (self._page + 1) * self._per_page < self._dialog_service.get_message_count():
            return self._page + 1
        return None

    def get_messages(self) -> QuerySet[Message]:
        return self._dialog_service.get_messages(self._page, self._per_page)
