from django.shortcuts import render
from . import forms, models
from django.db.models import Count, F
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect



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
#         context['comment_form'] = forms.CommentForm
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

        return context


# /////////////// ABOUT VIEW ////////////
class AboutView(TemplateView):
    """
    The about page
    """
    template_name = 'blog/about.html'


# ///////////////TERMS AND CONDITIONS ////////////
def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class PostDetailView(DetailView):
    model = models.Post
    comments = models.Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.CommentForm

        context.update({'form': form})

        return context

    def get(self, request, *args, **kwargs):

        if request.method == 'POST':
            # result = ''
            post_id = int(request.POST.get('pk'))
            comment = models.Post.objects.get(id=post_id)
            comment.likes = F(comment.likes) + 1
            result = comment.likes
            comment.save()
            # return HttpResponseRedirect(reverse)
            # context.update({'result':result})

        # if request.POST.get('dislike'):
        #     comment = models.Comment.objects.get(post='pk')
        #     comment.dislikes = F(comment.dislikes) + 1
        #     comment.save()
        # context = ({'likes': likes, 'dislikes': dislikes})
        # return render(request, 'blog/form_example.html', context)


# /////////////// TOPICS ////////////

class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')


class TopicDetailView(DetailView):
    model = models.Topic
    # context_object_name = 'topics'

    def get_object(self, queryset=None):
        return models.Topic.objects.get(slug=self.kwargs['slug'])

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()
        # topic = self.get_object()
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']

        requested_category = models.Topic.objects.get(slug=slug)

        topic_posts = requested_category.blog_posts.all().published().order_by('-published')

        topics = models.Topic.objects.all()\
            .annotate(topics=Count('blog_posts'))\
            .values('name', 'topics').order_by('-topics')[:10]

        context.update({'topics': topics,
                        'requested_category': requested_category,
                        'topic_posts': topic_posts},)

        return context


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


class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)


class PhotoContestSubmissionFormView(CreateView):
    model = models.PhotoContestSubmission
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your photo submission has been received.'
        )
        return super().form_valid(form)


def comments_likes_and_dislikes(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    likes = comment.likes
    dislikes = comment.dislikes

    #     # comment = request.POST.get('pk')
    #     # post = models.Post.objects.get(pk)
    #     # comment = post.comments

    if request.POST.get('like'):
        likes += 0
    if request.POST.get('dislike'):
        dislikes += 0
    comment.save()
    context = ({'likes': likes, 'dislikes': dislikes})
    return render(request, 'blog/form_example.html', context)


# def get_comments(request, post):
#     post = get_object_or_404(models.Post, pk=post)
#
#     comments = post.comments
#
#     new_comment = None
#
#     if request.method == 'POST':
#         # Pass the POST data into a new form instance for validation
#         comment_form = forms.CommentForm(request.POST)
#         # If the form is valid, return a different template.
#         if comment_form.is_valid():
#             # form.cleaned_data is a dict with valid form data
#             cleaned_data = comment_form.cleaned_data
#             new_comment = cleaned_data.save()
#
#             return render(
#                 request,
#                 'blog/post_detail.html',
#                 context={'data': cleaned_data}
#             )
#         # If not a POST, return a blank form
#         else:
#             comment_form = forms.CommentForm()
#
#         # Render if either an invalid POST or a GET
#         return render(request, 'blog/post_detail.html', context={'form': comment_form})
