from django.conf import settings  # Imports Django's loaded settings
from django.db import models


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # No duplicates!
        null=False,
    )
    slug = models.SlugField(unique=True, null=False,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Create your models here.
class Post(models.Model):
    """
    Represents a blog post
    """

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255, null=False,)
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False,
    )

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts',
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
        null=False,
    )

    content = models.TextField()

    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )

    created = models.DateTimeField(auto_now_add=True)  # Sets and create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    class Meta:
        #  Sort by the 'created' field. The '-' prefix
        #  specifies to order in descending/reverse order.
        #  Otherwise, it will be in ascending order.
        ordering = ['-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='blog_comments',
    )

    name = models.CharField(
        max_length=50,
        null=False,
    )

    email = models.EmailField(
        max_length=254,
        null=False,
    )

    text = models.TextField(null=False, max_length=400)

    approved = models.BooleanField()

    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
