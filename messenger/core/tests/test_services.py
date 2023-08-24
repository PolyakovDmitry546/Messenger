from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Channel, Membership, Message
from ..services import ChannelMessagesPageService, ChannelService


class ChannelServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='test_user1',
            password='123',
        )
        channel = Channel.objects.create(
            author=user1,
            name='test_name',
            description='test_description',
        )
        cls.messages = []
        for i in range(25):
            cls.messages.append(Message.objects.create(
                author=user1,
                text=f'message_{i}',
                channel=channel,
            ))
        Membership.objects.create(
            user=user1,
            channel=channel,
        )
        cls.channel_service = ChannelService(
            user=user1,
            channel_pk=channel.pk,
        )

    def test_get_message_count(self):
        expected_message_count = 25
        message_count = self.channel_service.get_message_count()
        self.assertEqual(message_count, expected_message_count)

    def test_get_messages_all(self):
        expected_messages = self.messages
        messages = list(self.channel_service.get_messages())
        self.assertEqual(expected_messages, messages)


class ChannelMessagesPageServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='test_user1',
            password='123',
        )
        user2 = User.objects.create(
            username='test_user2',
            password='123',
        )
        channel = Channel.objects.create(
            author=user1,
            name='test_name',
            description='test_description',
        )
        cls.messages = []
        for i in range(25):
            cls.messages.append(Message.objects.create(
                author=user1,
                text=f'message_{i}',
                channel=channel,
            ))
        Membership.objects.create(
            user=user1,
            channel=channel,
        )
        Membership.objects.create(
            user=user2,
            channel=channel,
            last_read_message_pk=cls.messages[22].pk,
        )
        cls.channel_messages_page_service1 = ChannelMessagesPageService(
            user=user1,
            channel_pk=channel.pk,
            page=0,
            per_page=None,
        )
        cls.channel_messages_page_service2 = ChannelMessagesPageService(
            user=user2,
            channel_pk=channel.pk,
            page=None,
            per_page=20,
        )

    def test_get_page_if_set(self):
        expected_page = 0
        page = self.channel_messages_page_service1.get_page()
        self.assertEqual(page, expected_page)

    def test_get_page_if_not_set(self):
        expected_page = 1
        page = self.channel_messages_page_service2.get_page()
        self.assertEqual(page, expected_page)

    def test_get_next_page(self):
        expected_next_page = 1
        next_page = self.channel_messages_page_service1.get_next_page()
        self.assertEqual(next_page, expected_next_page)

    def test_get_next_page_is_none(self):
        expected_next_page = None
        next_page = self.channel_messages_page_service2.get_next_page()
        self.assertEqual(next_page, expected_next_page)

    def test_get_messages(self):
        expected_messages = self.messages[20:]
        messages = list(self.channel_messages_page_service2.get_messages())
        self.assertEqual(expected_messages, messages)
