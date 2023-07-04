from django.shortcuts import render
from . import models
from django.db.models import Count


# Create your views here.
def home(request):
    """
    The Blog homepage
    """
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    # Get the authors for published posts only
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    # Get list of topics
    number_of_posts = models.Topic.objects.all().annotate(topics=Count('blog_posts')).values('name', 'topics').order_by(
        "-topics")[:10]

    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'number_of_posts': number_of_posts
    }

    return render(request, 'blog/home.html', context)
