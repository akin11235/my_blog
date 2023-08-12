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
