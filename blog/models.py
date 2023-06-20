from django.conf import settings  # Imports Django's loaded settings
from django.db import models


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