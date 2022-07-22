from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = User.objects.create_user(username='auth')
        cls.user_no_name = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.client,
        )
        cls.url_names_auth = {
            '/': 'posts/index.html',
            (f'/group/{cls.group.slug}/'): 'posts/group_list.html',
            (f'/profile/{cls.client}/'): 'posts/profile.html',
            (f'/posts/{cls.post.id}/'): 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            (f'/posts/{cls.post.id}/edit/'): 'posts/create_post.html',
        }
        cls.url_names_auth_user = {
            '/': 'posts/index.html',
            (f'/group/{cls.group.slug}/'): 'posts/group_list.html',
            (f'/profile/{cls.user_no_name}/'): 'posts/profile.html',
            (f'/posts/{cls.post.id}/'): 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
        }
        cls.url_names_not_auth = {
            '/': 'posts/index.html',
            (f'/group/{cls.group.slug}/'): 'posts/group_list.html',
            (f'/profile/{cls.user_no_name}/'): 'posts/profile.html',
            (f'/posts/{cls.post.id}/'): 'posts/post_detail.html',
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_no_name)
        self.author = User.objects.create_user(username='author')
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_pages_url_exists_at_desired_location_not_auth(self):
        for address, template in StaticURLTests.url_names_not_auth.items():
            with self.subTest(address=address,
                              template=template):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_url_exists_at_desired_location_auth(self):
        for address, template in StaticURLTests.url_names_auth_user.items():
            with self.subTest(address=address, template=template):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_detail_url_exists_at_desired_location_authorized(self):
        if self.authorized_author == self.user_no_name:
            response = self.author.get((f'/posts/{self.post.id}/edit/'))
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_list_url_redirect_anonymous(self):
        response = self.client.get(
            (f'/posts/{self.post.id}/edit/'), follow=True)
        self.assertRedirects(
            response,
            (f'/auth/login/?next=/posts/{self.post.id}/edit/'))

    def test_create_url_redirect_anonymous(self):
        print(f'self.client={self.client}=')
        response = self.client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_urls_uses_correct_template_auth(self):
        if self.authorized_author == self.user_no_name:
            for address, template in StaticURLTests.url_names_auth.items():
                with self.subTest(address=address):
                    response = self.authorized_author.get(address)
                    self.assertTemplateUsed(response, template)
        for address, template in StaticURLTests.url_names_auth_user.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_not_auth(self):
        for address, template in StaticURLTests.url_names_not_auth.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page_added_url_exists_at_desired_location(self):
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
