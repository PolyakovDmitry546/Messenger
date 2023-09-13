from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status

from ..models import Channel, Membership
from ..serializers import SearchResultSerializer


class ChannelViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='123',
        )
        cls.channel = Channel.objects.create(
            author=cls.user,
            name='test_name',
            description='test_description',
        )
        cls.membership = Membership.objects.create(
            user=cls.user,
            channel=cls.channel,
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(f'/channels/{self.channel.pk}')
        self.assertRedirects(resp, f'/user/login/?next=/channels/{self.channel.pk}')

    # def test_view_url_exists_at_desired_location(self):
    #     login = self.client.login(username=self.user.username, password=self.user.password)
    #     print(login)
    #     resp = self.client.get(f'/channels/{self.channel.pk}')
    #     print(resp.context['user'])
    #     self.assertEqual(resp.status_code, 200)

    # def test_view_url_accessible_by_name(self):
    #     resp = self.client.get(reverse('channel', kwargs={'pk': self.channel.pk}))
    #     self.assertEqual(resp.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     resp = self.client.get(reverse('channel', kwargs={'pk': self.channel.pk}))
    #     self.assertEqual(resp.status_code, 200)

    #     self.assertTemplateUsed(resp, 'channel.html')

    # def test_lists_all_authors(self):
    #     resp = self.client.get(reverse('channel', kwargs={'pk': self.channel.pk}))
    #     self.assertEqual(resp.status_code, 200)
    #     print(resp.context)


class SearchResultAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='123',
        )
        cls.channel = Channel.objects.create(
            author=cls.user,
            name='test_channel',
            description='test_description',
        )

    def test_forbidden_if_not_logged_in(self):
        resp = self.client.get('/api/v1/search')
        expected_data = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)
        self.assertEqual(expected_data, resp.data)

    def test_search_wihtout_q_param(self):
        self.client.force_login(user=self.user)
        resp = self.client.get('/api/v1/search')
        expected_data = {"users": [], "channels": []}
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(expected_data, resp.data)

    def test_search_wiht_empty_q_param(self):
        self.client.force_login(user=self.user)
        resp = self.client.get('/api/v1/search?q=')
        expected_data = {"users": [], "channels": []}
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(expected_data, resp.data)

    def test_search_wiht_q_param(self):
        self.client.force_login(user=self.user)
        q = 'test'
        resp = self.client.get(f'/api/v1/search?q={q}')
        users = User.objects.filter(username__icontains=q)
        channels = Channel.objects.filter(name__icontains=q)
        serializer = SearchResultSerializer(dict(users=users, channels=channels))
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(serializer.data, resp.data)
