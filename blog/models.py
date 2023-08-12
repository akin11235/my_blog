from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class TopicQuerySet(models.QuerySet):
    def get_topics(self):
        return Topic.objects.all().filter(blog_posts__in=self)


class Topic(models.Model):
    """
    Represents categories of blog posts topics
    """
    objects = models.Manager()

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

    def get_absolute_url(self):
        return reverse(
            'topic-detail',
            kwargs={
                'slug': self.slug
            }
        )


class PostQuerySet(models.QuerySet):
    """
    Extends the Post model base queryset with custom methods
    """
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()


# class PostManager(models.Manager):
#     """
#     Represents modified Post model base queryset
#     """
#     def get_queryset(self):
#         queryset = super().get_queryset()  # Get the initial queryset
#         return queryset.exclude(deleted=True)


class Post(models.Model):
    """
    Represents a blog post
    """
    objects = PostQuerySet.as_manager()

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

    # content = models.TextField()
    content = RichTextUploadingField()

    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )

    created = models.DateTimeField(auto_now_add=True)  # Sets and create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    # deleted = models.BooleanField()  # Filters base set of data for soft-delete behaviour

    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )

    class Meta:
        #  Sort by the 'created' field. The '-' prefix
        #  specifies to order in descending/reverse order.
        #  Otherwise, it will be in ascending order.
        ordering = ['-created']

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)


class CommentQuerySet(models.QuerySet):
    def get_comments(self):
        return Comment.objects.all().filter(comments__in=self)


class Comment(models.Model):
    """
    Represents visitors comments
    """

    objects = models.Manager()

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False
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

    likes = models.PositiveIntegerField(
        default=0,
    )

    dislikes = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'"{self.text}" by {self.name} posted {self.created}\n'


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'


class PhotoContestSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    submitted = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        blank=False,
        null=False,
        # help_text='Image submitted for the photo contest'
    )

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
