from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    slug = models.SlugField(verbose_name='slug', unique=True)
    description = models.TextField(verbose_name='description')

    def __str__(self):
        return {self.title}


class Post(models.Model):
    text = models.TextField(
        verbose_name='text',
    )
    pub_date = models.DateTimeField(
        verbose_name='publication date',
        auto_now_add=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        blank=True, null=True,
        help_text='Выберите группу'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='author',
        null=True,
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='post',
        blank=True, null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='author',
        null=True,
    )
    text = models.TextField(
        verbose_name='text',
    )
    created = models.DateTimeField(
        verbose_name='create date',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='user',
        null=True,
    )
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='follow_user',
        null=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('following', 'user'), name='unique_following'),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
