from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Channel, Membership, Message


class ChannelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(
            username='test_user',
            password='123',
        )
        cls.channel = Channel.objects.create(
            author=author,
            name='test_name',
            description='test_description',
        )
        cls.author_field = cls.channel._meta.get_field('author')
        cls.name_field = cls.channel._meta.get_field('name')
        cls.description_field = cls.channel._meta.get_field('description')
        cls.create_at_field = cls.channel._meta.get_field('create_at')

    def test_name_max_length(self):
        max_length = getattr(self.name_field, 'max_length')
        expected_max_length = 100
        self.assertEqual(max_length, expected_max_length)

    def test_name_unique(self):
        unique = getattr(self.name_field, 'unique')
        self.assertTrue(unique)

    def test_description_max_length(self):
        max_length = getattr(self.description_field, 'max_length')
        expected_max_length = 1000
        self.assertEqual(max_length, expected_max_length)

    def test_create_at_auto_now_add(self):
        auto_now_add = getattr(self.create_at_field, 'auto_now_add')
        self.assertTrue(auto_now_add)

    def test_string_representation(self):
        self.assertEqual(str(self.channel), str(self.channel.name))

    def test_get_absolute_url(self):
        expected_url = '/channels/' + str(self.channel.pk)
        self.assertEqual(self.channel.get_absolute_url(), expected_url)


class MembershipTest(TestCase):
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
        for i in range(25):
            Message.objects.create(
                author=user1,
                text=f'message_{i}',
                channel=channel,
            )
        cls.membership1 = Membership.objects.create(
            user=user1,
            channel=channel,
        )
        cls.membership2 = Membership.objects.create(
            user=user2,
            channel=channel,
            last_read_message_pk=21,
        )

    def test_last_read_message_pk_default(self):
        last_read_message_pk_field = self.membership1._meta.get_field('last_read_message_pk')
        default = getattr(last_read_message_pk_field, 'default')
        expected_default = 0
        self.assertEqual(default, expected_default)

    def test_string_representation(self):
        self.assertEqual(str(self.membership1), f'{self.membership1.user} -> {self.membership1.channel}')

    def test_read_message_count(self):
        expected_read_message_count = 21
        self.assertEqual(self.membership2.read_message_count(), expected_read_message_count)

    def test_unread_message_count(self):
        expected_unread_message_count = 4
        self.assertEqual(self.membership2.unread_message_count(), expected_unread_message_count)

    def test_read_message_count_for_new_member(self):
        expected_read_message_count = 0
        self.assertEqual(self.membership1.read_message_count(), expected_read_message_count)

    def test_unread_message_count_for_new_member(self):
        expected_unread_message_count = 25
        self.assertEqual(self.membership1.unread_message_count(), expected_unread_message_count)

    def test_get_number_page_with_last_read_message(self):
        expected_number_page = 1
        self.assertEqual(self.membership2.get_number_page_with_last_read_message(20), expected_number_page)

    def test_get_number_page_with_last_read_message_for_new_user(self):
        expected_number_page = 0
        self.assertEqual(self.membership1.get_number_page_with_last_read_message(20), expected_number_page)


class MessageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user',
            password='123',
        )
        channel = Channel.objects.create(
            author=user,
            name='test_name',
            description='test_description',
        )
        cls.message = Message.objects.create(
                author=user,
                text='test_message',
                channel=channel,
            )
        cls.text_field = cls.message._meta.get_field('text')
        cls.create_at_field = cls.message._meta.get_field('create_at')
        cls.update_at_field = cls.message._meta.get_field('update_at')

    def test_text_max_length(self):
        max_length = getattr(self.text_field, 'max_length')
        expected_max_length = 1000
        self.assertEqual(max_length, expected_max_length)

    def test_create_at_auto_now_add(self):
        auto_now_add = getattr(self.create_at_field, 'auto_now_add')
        self.assertTrue(auto_now_add)

    def test_update_at_auto_now(self):
        auto_now = getattr(self.update_at_field, 'auto_now')
        self.assertTrue(auto_now)

        
class CommentTest(TestCase):
    pass
