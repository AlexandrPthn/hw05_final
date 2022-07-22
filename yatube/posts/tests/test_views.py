import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image
from posts.models import Comment, Follow, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT, CACHES=settings.TEST_CACHES)
class ViewPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        img = Image.new('RGB', (10, 10), color=(10, 10, 10))
        img.save('test.png')
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
            image=SimpleUploadedFile(name=TEMP_MEDIA_ROOT + 'test.png',
                                     content=open('test.png', 'rb').read(),
                                     content_type='image/png'),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            '/': 'posts/index.html',
            (f'/group/{self.group.slug}/'): 'posts/group_list.html',
            (f'/profile/{self.user.username}/'): 'posts/profile.html',
            (f'/posts/{self.post.id}/'): 'posts/post_detail.html',
            (f'/posts/{self.post.id}/edit/'): 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_pages_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_pages_correct_context(self):
        """Шаблоны index, group_list, profile"""
        """сформированs с правильным контекстом."""
        context_pages_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username}),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        }
        for reverse_name in context_pages_names:
            response = self.authorized_client.get(reverse_name)
            self.assertEqual(response.context.get('post').text,
                             self.post.text)
            self.assertEqual(
                response.context.get('post').id,
                self.post.id)
            self.assertEqual(
                response.context.get('post').author,
                self.post.author)
            self.assertEqual(
                response.context.get('post').group,
                self.group)
            self.assertIn("<img", response.content.decode())

    def test_post_create_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        post = Post.objects.create(
            text='Текст поста2',
            author=User.objects.create_user(username='auth2'),
            group=Group.objects.create(title='Тестовая группа',
                                       slug='slug2',
                                       description='Тестовое описание',
                                       ),
            image=SimpleUploadedFile(name=TEMP_MEDIA_ROOT + 'test.png',
                                     content=open('test.png', 'rb').read(),
                                     content_type='image/png'),
        )
        post.save()
        self.assertEqual(post.id, Post.objects.count())
        context_pages_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': post.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': post.author.username}),
        }
        for reverse_name in context_pages_names:
            response = self.authorized_client.get(reverse_name)
            first_object = response.context['page_obj'][0]
            self.assertEqual(first_object.id, post.id)

    def test_auth_user_comment_post(self):
        self.authorized_client.post(reverse('posts:add_comment',
                                            kwargs={'post_id': self.post.id}),
                                    {'text': 'test_text'})
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertIn('test_text', response.content.decode())
        comment_obj = Comment.objects.filter(author=self.user,
                                             post=self.post.id).count()
        self.assertEqual(comment_obj, 1)

    def test_cache(self):
        """ Проверка работы кэширования главной страницы. """
        post = Post.objects.create(
            text='cache_test',
            author=self.user,
            group=self.group,
        )
        response = self.client.get(reverse('posts:index'))
        self.assertContains(response, 'cache_test')
        post.delete()
        self.assertContains(response, 'cache_test')
        cache.clear()
        response_no_cache = self.client.get(reverse('posts:index'))
        self.assertNotContains(response_no_cache, 'cache_test')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 13
        for posts_num in range(number_of_posts):
            Post.objects.create(
                text='Текст %s' %
                posts_num,
                author=User.objects.create_user(
                    username='auth %s' %
                    posts_num))

    def test_paginator(self):
        paginat = Paginator(Post.objects.all(), settings.PER_PAGE)
        page_two = paginat.count - settings.PER_PAGE
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), settings.PER_PAGE)
        response = self.client.get(
            reverse('posts:index')
            + f'?page={paginat.num_pages}')
        self.assertEqual(len(response.context['page_obj']), page_two)


@override_settings(CACHES=settings.TEST_CACHES)
class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_client = Client()
        cls.user1 = User.objects.create_user(username="user1")
        cls.user2 = User.objects.create_user(username="user2")
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user2,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

    def test_auth_user_can_subscribe(self):
        response_get_profile = self.authorized_client.get(
            reverse('posts:profile', args=(self.user2,)))
        self.assertIn("Подписаться", response_get_profile.content.decode())
        self.assertNotIn("Отписаться", response_get_profile.content.decode())

        response_subscribe = self.authorized_client.post(
            reverse('posts:profile_follow', args=(self.user2,)), follow=True)

        is_follow = Follow.objects.filter(user=self.user1,
                                          author=self.user2).count()
        self.assertEqual(is_follow, 1)

        self.assertIn("Отписаться", response_subscribe.content.decode())

    def test_auth_user_can_unsubscribe(self):
        Follow.objects.create(user=self.user1, author=self.user2)
        is_follow = Follow.objects.filter(user=self.user1,
                                          author=self.user2).count()
        self.assertEqual(is_follow, 1)
        response_unsubscribe = self.authorized_client.post(
            reverse('posts:profile_unfollow',
                    args=(self.user2,)), follow=True)
        self.assertIn("Подписаться", response_unsubscribe.content.decode())

        follow_obj = Follow.objects.filter(user=self.user1,
                                           author=self.user2).count()
        self.assertEqual(follow_obj, 0)

    def test_follow_index(self):
        follow_url = f'/profile/{self.user2.username}/follow/'
        self.authorized_client.get(follow_url)
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(response.context.get('page_obj')[0], self.post)
