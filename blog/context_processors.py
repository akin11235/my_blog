from . import models
from django.db.models import Count
# from forms import forms
from . import forms, models
from django.shortcuts import render


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    top_topics = models.Topic.objects.all() \
        .annotate(topics=Count('blog_posts')) \
        .values('name', 'topics', 'slug') \
        .order_by('-topics')[:10]

    # comment_form = forms.CommentForm

    # top_comments = models.Comment.objects.all().filter(text__icontains='WFH')

    # top_comments = models.Post.objects.Comment_comments.all()

    # top_comments = models.Post.objects.all.filter(comments__in=self)

    return {'authors': authors,
            'top_topics': top_topics,
            # 'top_comments': top_comments,
            # 'comment_form': comment_form,
            }


# def comment_form(request):
#     # Handle the POST
#     if request.method == 'POST':
#         # Pass the POST data into a new form instance for validation
#         form = forms.CommentForm(request.POST)
#
#         # If the form is valid, return a different template.
#         if form.is_valid():
#             # form.cleaned_data is a dict with valid form data
#             cleaned_data = form.cleaned_data
#
#             return render(
#                 request,
#                 'blog/form_example_success.html',
#                 context={'data': cleaned_data}
#             )
#     # If not a POST, return a blank form
#     else:
#         form = forms.CommentForm()
#
#     # Return if either an invalid POST or a GET
#     return render(request, 'blog/form_example.html', context={'comment_form': comment_form})

