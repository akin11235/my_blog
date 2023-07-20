from django.shortcuts import render
from . import forms, models
from django.db.models import Count
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages


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
    # context_object_name = 'topics'

    def get_object(self, queryset=None):
        return models.Topic.objects.get(slug=self.kwargs['slug'])


    # def get_slug_field(self):
    #
    #
    # def get_context_object_name(self, obj):




    # topic.blog_posts.all()
    # post.topics.all()

    # context.update({'topics': topics})



    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()
        # topic = self.get_object()
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        # topic_posts = models.Topic.objects.filter(name='Life')

        requested_category = models.Topic.objects.get(slug=slug)

        # topic_posts = requested_category.blog_posts.all()


        topics = models.Topic.objects.all()\
            .annotate(topics=Count('blog_posts'))\
            .values('name', 'topics').order_by('-topics')[:10]

        # topic_count = models.Topic.objects.all().annotate(topics=Count('blog_posts')).values('name', 'topics')

        topic_count = models.Topic.objects.count()

        context.update({'latest_posts': latest_posts,
                       'topics': topics,
                        'topic_count': topic_count,
                        'requested_category': requested_category},)


        # Update the context with our context variables
        # context.update({
        #     'authors': authors,
        #     'latest_posts': latest_posts
        #     'number_of_posts': number_of_posts
        # })
        return context

        # context['topics'] = models.Topic.objects.all()
        # context['topics'] = models.Topic.objects.all().annotate(topics=Count('blog_posts')).values('name', 'topics').order_by('-topics')[:10]

    # top_topics = models.Topic.objects.all() \
    #     .annotate(topics=Count('blog_posts')) \
    #     .values('name', 'topics') \
    #     .order_by('-topics')[:10]


def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Render if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})


class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

