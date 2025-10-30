from django import forms
from .models import Article, Newsletter, CustomUser, Publisher, Review
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    """Form for creating an article"""
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.none(),
        required=False,
        empty_label="Independent",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Article
        fields = ['headline', 'byline', 'body', 'conclusion']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'headline'}),
            'byline': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'byline'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'body'}),
            'conclusion': forms.Textarea(attrs={'class': 'form-control',
                                                'placeholder': 'conclusion'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user from view
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'profile') and user.profile.is_verified_contributor:
            self.fields['publisher'].queryset = Publisher.objects.all()
        else:
            self.fields['publisher'].queryset = Publisher.objects.filter(
                name="Independent")


class NewsletterForm(forms.ModelForm):
    """Form for creating a newsletter"""
    class Meta:
        model = Newsletter
        fields = ['title', 'issue_date', 'articles']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'title'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control',
                                                 'type': 'date',
                                                 'placeholder': 'issue_date'}),
            'articles': forms.SelectMultiple(attrs={'class': 'form-control',
                                                    'placeholder':
                                                    'articles'}),
        }


class UserRegistrationForm(UserCreationForm):
    """Form for registering a new user"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control',
                                                    'placeholder':
                                                    'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control',
                                                    'placeholder':
                                                    'Confirm Password'}),
            'role': forms.Select(attrs={'class': 'form-control',
                                        'placeholder': 'Role'}),
        }


class PublisherForm(forms.ModelForm):
    """Form for registering a new publisher"""
    editor = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='editor'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control',
                                           'placeholder':
                                    'Editor'})
    )
    journalist = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='journalist'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control',
                                           'placeholder':
                                    'Journalist'})
    )

    class Meta:
        model = Publisher
        fields = ['name', 'email', 'password', 'editor',
                  'journalist']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class':
                                                   'form-control',
                                                   'placeholder':
                                                   'Password'}),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting a review for an article"""
    class Meta:
        model = Review
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control',
                                              'placeholder': 'Comments'}),
        }
