from django.shortcuts import render, get_object_or_404, redirect
from . import forms, models
from django.db.models import Count
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages


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


# ****************** ABOUT VIEW ***********************
class AboutView(TemplateView):
    """
    The about page
    """
    template_name = 'blog/about.html'


# ****************** TERMS AND CONDITIONS ***********************
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


# ****************** TOPICS ***********************

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


# ****************** FORM EXAMPLES ***********************
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


# ****************** CONTACT FORM ***********************
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


# ****************** PHOTO COMPETITION ***********************
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


# ****************** LIKES AND DISLIKES ***********************
def like(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.likes += 1
    comment.save()
    if comment:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Thank you for your comment!'
        )
        # return HttpResponse({'likes': comment.likes})
        return redirect('home')

    else:
        return render(request, 'blog/home.html')


def dislike(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.dislikes += 1
    comment.save()
    if comment:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Thank you for your comment!'
        )
        return redirect('home')
    # return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
    else:
        return render(request, 'blog/home.html')
    # return JsonResponse({'dislikes': comment.dislikes})
