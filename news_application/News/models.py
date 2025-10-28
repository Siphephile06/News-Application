from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Model representing users with different roles.

    **Fields:**

    - **username**: The username of the user.
    - **email**: The email address of the user.
    - **role**: The role of the user, constrained to predefined choices.

    **Methods:**

    - ``__str__``: Returns the username of the user for easy identification.
    """

    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    ]
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.TextField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Fields for readers.
    subscriptions_to_publishers = models.ManyToManyField('Publisher',
                                                         blank=True,
                                                         related_name="subscribed")
    subscriptions_to_journalists = models.ManyToManyField('CustomUser',
                                                          related_name="journalist_followers",
                                                          blank=True)
    # Field  for journalists.
    published_articles = models.ManyToManyField('Article', blank=True,
                                                related_name='journalists')
    published_newsletters = models.ManyToManyField('Newsletter', blank=True,
                                                   related_name='journalists')

    def is_editor(user):
        return user.role == 'editor'

    def is_journalist(user):
        return user.role == 'journalist'

    def is_reader(user):
        return user.role == 'reader'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear irrelevant fields based on role
        if self.role == 'reader':
            self.published_articles.clear()
            self.published_newsletters.clear()
        elif self.role == 'journalist':
            self.subscriptions_to_publishers.clear()
            self.subscriptions_to_journalists.clear()

    def __str__(self):
        return self.username


class Publisher(models.Model):
    """
    Model representing a publisher.

    **Fields:**

    - **name**: The name of the publisher.
    - **email**: The contact email of the publisher.
    - **password**: The password for the publisher's account.
    - **editors**: A many-to-many relationship to CustomUser with role 'editor'.
    - **journalists**: A many-to-many relationship to CustomUser with role 'journalist'.

    **Methods:**

    - ``__str__``: Returns the name of the publisher for easy identification.
    """

    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    editors = models.ManyToManyField(CustomUser,
                                     limit_choices_to={'role': 'editor'},
                                     related_name='editor_publishers',
                                     blank=True)
    journalists = models.ManyToManyField(CustomUser,
                                         limit_choices_to={'role':
                                                           'journalist'},
                                         related_name='journalist_publishers',
                                         blank=True)

    def add_editor_to_publisher(self, user):
        if user.role == 'editor':
            self.editors.add(user)

    def add_journalist_to_publisher(self, user):
        if user.role == 'journalist':
            self.journalists.add(user)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Model representing a news article.

    **Fields:**

    - **Headline** The title of the article.
    - **Byline** The author of the article.
    - **Body** The main content of the article.
    - **conclusion** The concluding part of the article.

    **Methods:**

    - ``__str__``: Returns the headline of the article for easy identification.
    """
    class Meta:
        permissions = [
            ("review_articles", "Can review articles"),
            ("approve_article", "Can approve article"),
        ]
    headline = models.CharField(max_length=200)
    byline = models.CharField(max_length=100)
    body = models.TextField()
    conclusion = models.TextField()
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='articles', null=True)
    publisher = models.ForeignKey(Publisher, null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self.headline


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'headline', 'byline', 'body', 'conclusion', 'approved']


class Newsletter(models.Model):
    """
    Model representing a newsletter.

    **Fields:**

    - **Title** The title of the newsletter.
    - **Issue Date** The date the newsletter was issued.
    - **Articles** A many-to-many relationship with Article.

    **Methods:**

    -`` __str__``: Returns the title of the newsletter for easy identification.
    """
    title = models.CharField(max_length=200)
    issue_date = models.DateField()
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.title


class ResetToken(models.Model):
    """
    Model representing a password reset token.

    **Fields:**

    - **User** A foreign key linking to a CustomUser.
    - **Token** The unique token string.
    - **Created At** The timestamp when the token was created.
    - **Expires At** The timestamp when the token expires.
    - **Used** A boolean indicating whether the token has been used.

    **Methods**

    - ``__str__``: Returns a string representation of the token for easy
        identification.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
