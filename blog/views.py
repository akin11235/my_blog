from django.shortcuts import render
from . import models
from django.db.models import Count
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView


# Create your views here.
# ContextMixin deleted from views.py amd moved to context_processors.py
# class ContextMixin:
#     """
#     Provides common context variables for blog views
#     """
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['authors'] = models.Post.objects.published() \
#             .get_authors() \
#             .order_by('first_name')
#
#         context['number_of_posts'] = models.Topic.objects.all()\
#             .annotate(topics=Count('blog_posts')).values('name', 'topics').order_by('-topics')[:10]
#
#         return context


# /////////////// HOME VIEW ////////////

# 1st implementation of home view using a function
# def home(request):
#     """
#     The Blog homepage
#     """
#     # Get last 3 posts
#     latest_posts = models.Post.objects.published().order_by('-published')[:3]
#     # Get the authors for published posts only
#     authors = models.Post.objects.published().get_authors().order_by('first_name')
#     # Get list of topics
#     number_of_posts = models.Topic.objects.all().annotate(topics=Count('blog_posts')) \
#       .values('name', 'topics').order_by("-topics")[:10]
#
#     context = {
#         'authors': authors,
#         'latest_posts': latest_posts,
#         'number_of_posts': number_of_posts
#     }
#
#     return render(request, 'blog/home.html', context)


# 2nd implementation of home view using a class based views
class HomeView(TemplateView):
    """
    The blog homepage
    """
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        context.update({'latest_posts': latest_posts})

        # authors = models.Post.objects.published() \
        #     .get_authors() \
        #     .order_by('first_name')
        #
        # number_of_posts = models.Topic.objects.all() \
        #     .annotate(topics=Count('blog_posts')) \
        #     .values('name', 'topics') \
        #     .order_by('-topics')[:10]

        # Update the context with our context variables
        # context.update({
        #     'authors': authors,
        #     'latest_posts': latest_posts
        #     'number_of_posts': number_of_posts
        # })
        return context


# /////////////// ABOUT VIEW ////////////
"""  
# 1st implementation of about view using class based view for the About page
class AboutView(View):
    def get(self, request):
        return render(request, 'blog/about.html')


2nd implementation of about view using a Template view
class AboutView(TemplateView):
    template_name = 'blog/about.html' 
    """


class AboutView(TemplateView):
    """
    The about page
    """
    template_name = 'blog/about.html'

    # Code below manipulates the context data by overriding get_context_data() method
    # The code below has been moved to the ContextMixin class, so essentially back to 2nd implementation

    # def get_context_data(self, **kwargs):
    #     # Get the context data from the parent class
    #     context = super().get_context_data(**kwargs)
    #
    #     # Define the "authors" context variable
    #     context['authors'] = models.Post.objects.published() \
    #         .get_authors() \
    #         .order_by('first_name')
    #
    #     return context


# ///////////////TERMS AND CONDITIONS ////////////
def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset().published()

        # If this is a 'pk' lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )


# /////////////// TOPICS ////////////
# class TopicView(TemplateView):
#     template_name = 'blog/topics.html'
    #
    # def get(self, request):
    #     return render(request, 'blog/topic.html')


class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')


class TopicDetailView(DetailView):
    model = models.Topic

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()

        # if 'pk' in self.kwargs:
        #     return queryset
        #
        # return queryset.filter(
            # post__title=self.kwargs['name']
        # )

