from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Модель групп пользователей
class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Наименование",
        help_text="Введите наименование группы")
    slug = models.SlugField(
        verbose_name="Ярлык",
        help_text="Адрес для страницы",
        unique=True)
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание группы")

    def __str__(self):
        return self.title


# Модель постов пользователей
class Post(models.Model):
    text = models.TextField(
        verbose_name="Текст поста",
        help_text="Введите текст поста")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата публикации")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
        help_text="Автор поста")
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
        help_text="Выберите группу",
        blank=True,
        null=True)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        # выводим текст поста
        return self.text


# Модель комментариев пользователей
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
        help_text="Пост")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
        help_text="Автор комментария")
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата публикации")

    def __str__(self):
        return self.text

# Модель подписок пользователей


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")
