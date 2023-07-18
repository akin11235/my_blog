from . import models
from django.db.models import Count


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    top_topics = models.Topic.objects.all() \
        .annotate(topics=Count('blog_posts')) \
        .values('name', 'topics') \
        .order_by('-topics')[:10]

    return {'authors': authors,
            'top_topics': top_topics,
            }
