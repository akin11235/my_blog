from django import forms
from .models import Comment


class ExampleSignupForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(
        label='Gender',
        required=False,
        choices=[
            (None, '-------'),
            ('m', 'Male'),
            ('f', 'Female'),
            ('n', 'Non-binary'),
        ]
    )
    receive_newsletter = forms.BooleanField(
        required=False,
        label='Do you wish to receive our newsletter?'
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': "col-sm-12"}),
            'email': forms.TextInput(attrs={'class': "col-sm-12"}),
            'text': forms.Textarea(attrs={'class': "col-sm-12"}),
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
