# from . import models
from django.db.models import Count
# from forms import forms
from . import models
# from django.shortcuts import render


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    top_topics = models.Topic.objects.all() \
        .annotate(topics=Count('blog_posts')) \
        .values('name', 'topics', 'slug') \
        .order_by('-topics')[:10]

    latest_posts = models.Post.objects.published() \
                       .order_by('-published')[:3]

    return {'authors': authors,
            'top_topics': top_topics,
            'latest_posts': latest_posts,
            # 'top_comments': top_comments,
            # 'comment_form': comment_form,
            }
