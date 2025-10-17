from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Article, Newsletter, ArticleSerializer, CustomUser
from .models import ResetToken, Publisher
from datetime import datetime, timedelta
from .forms import ArticleForm, NewsletterForm, UserRegistrationForm
from .forms import PublisherForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import EmailMessage
import secrets
from hashlib import sha1
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated as IsAuthentication
from django.http import JsonResponse
from .functions.tweet import Tweet


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    """ Signal receiver to create user roles and assign permissions
    after migrations are applied"""
    # Define roles and their permissions
    role_permissions = {
        'Reader': ['view_article', 'view_newsletter'],
        'Editor': ['view_article', 'view_newsletter', 'change_article',
                   'change_newsletter', 'delete_article', 'delete_newsletter',
                   'review_articles', 'approve_article'],
        'Journalist': ['view_article', 'view_newsletter', 'add_article',
                       'add_newsletter', 'change_article',
                       'change_newsletter', 'delete_article',
                       'delete_newsletter'],
    }

    for role, perms in role_permissions.items():
        # Create and assign permissions.
        group, _ = Group.objects.get_or_create(name=role)
        permissions = Permission.objects.filter(codename__in=perms)
        group.permissions.set(permissions)
        group.save()


def register_user(request):
    """View to register a user"""
    form = UserRegistrationForm()
    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.save()
                # Assign group based on role
                role = form.cleaned_data.get('role')
                if role:
                    try:
                        group = Group.objects.get(name=role)
                        user.groups.add(group)
                    except Group.DoesNotExist:
                        print(f"Group '{role}' does not exist.")
                return redirect('login')
        return render(request, 'news/register.html', {'form': form})
    except Exception as e:
        return render(request, 'news/register.html', {'form': form,
                                                      'error': str(e)})


def login_user(request):
    """View function to handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('article_list'))
        else:
            return render(request, 'news/login.html', {'error':
                                                       'Invalid credentials'})
    return render(request, 'news/login.html')


@login_required
def logout_user(request):
    """View to handleuser logout"""
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return render(request, 'news/logout.html')


@login_required
def become_publisher(request):
    user = request.user

    # Restrict who can become a publisher
    if user.role not in ['editor', 'journalist']:
        return HttpResponseForbidden("You don't have permission to become a"
                                     " publisher.")

    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.email = user.email
            publisher.password = user.password
            publisher.save()

            # Assign user to appropriate role
            if user.role == 'editor':
                publisher.editors.add(user)
            elif user.role == 'journalist':
                publisher.journalists.add(user)

            return redirect('publisher_dashboard')
    else:
        form = PublisherForm()
    return render(request, 'news/become_publisher.html', {'form': form})


def build_email(user, reset_url):
    """View funtion to build an email to reset the user's password"""
    subject = "Password Reset"
    user_email = user.email
    domain_email = "example@domain.com"
    body = f"Hi {user.username}, Here is the link to reset password"
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email


def generate_reset_url(user):
    """View function to generate the url for resetting the password"""
    domain = "http://127.0.0.1.8000/"
    app_name = "News"
    url = f"{domain}{app_name}/reset_password/"
    token = str(secrets.token_urlsafe(20))
    expiry_date = datetime.now() + timedelta(minutes=30)
    reset_token = ResetToken.objects.create(user=user,
                                            token=sha1(token.encode())
                                            .hexdigest(),
                                            expiry_date=expiry_date)
    url += f"{reset_token}/"
    return url


def send_password_reset(request):
    """View function to send email to reset the password"""
    user_email = request.POST.get('email')
    user = CustomUser.objects.get(email=user_email)
    url = generate_reset_url(user)
    email = build_email(user, url)
    email.send()
    return HttpResponseRedirect(reverse('login'))


def reset_user_password(request, token):
    """View function to show the password reset form"""
    try:
        hashed_token = sha1(token.encode()).hexdigest()
        user_token = ResetToken.objects.get(token=hashed_token)

        if user_token.expiry_date.replace(tzinfo=None) < datetime.now():
            user_token.delete()
            return render(request, 'news/reset_password.html', {'error':
                                                                'Token has'
                                                                'expired.'})

        return render(request, 'news/reset_password.html', {'token': token})

    except ResetToken.DoesNotExist:
        return render(request, 'news/reset_password.html', {'error':
                                                            'Invalid token.'})


def reset_password(request):
    """View function to complete resetting the user's password"""
    username = request.session.get('user')
    token = request.session.get('token')

    if not username or not token:
        return render(request, 'news/reset_password.html', {'error':
                                                            'Session expired '
                                                            'or invalid '
                                                            'access.'})

    password = request.POST.get('password')
    password_conf = request.POST.get('password_conf')

    if password == password_conf:
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.save()

        # Delete the token after use
        ResetToken.objects.filter(user=user,
                                  token=sha1(token.encode())
                                  .hexdigest()).delete()

        return redirect('login')
    return render(request, 'news/reset_password.html', {'error':
                                                        "Passwords don't "
                                                        "match"})


def home(request):
    """View function to display the home page"""
    return render(request, 'news/home.html')


def publisher_dashboard(request):
    """View function to display publisher dashboard"""
    return render(request, 'news/publisher_dashboard.html')


def about(request):
    """View function to display about page."""
    return render(request, 'news/about.html')


def article(request):
    """View function to display articles"""
    articles = Article.objects.all()
    return render(request, 'news/article.html', {'articles': articles})


def article_list(request):
    """View funtion to list all the articles"""
    articles = Article.objects.all()
    return render(request, 'news/article_list.html', {'articles': articles})


@api_view(['GET'])
def api_article_list(request):
    """API view to list all articles"""
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthentication])
def api_create_article(request):
    """View function to add articles via api."""
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required
@permission_required('News.view_article', raise_exception=True)
def view_article(request, pk):
    """View function to display article"""
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'news/article.html', {'article': article})


@login_required
def subscription_to_publishers(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscriptions_to_publishers.add(publisher)
    return redirect('news/subscription_success.html',
                    publisher_id=publisher.id)


@login_required
def subscription_to_journalists(request, journalist_id):
    """View function to handle subscription to journalists"""
    journalist = get_object_or_404(CustomUser, id=journalist_id,
                                   role='journalist')
    request.user.subscriptions_to_journalists.add(journalist)
    return redirect('news/subscription_success.html',
                    journalist_id=journalist.id)


def subscribe(request):
    """View function to render subscribe page."""
    return render(request, 'news/subscribe.html')


def subscription_success(request):
    """View function to render subscription success page."""
    return render(request, 'news/subscription_success.html')


@login_required
@permission_required('News.approve_article', raise_exception=True)
def approve_articles(request, pk):
    """View function to approve articles."""
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.approved = True
        article.save()
        return redirect('article_list')
    return HttpResponseForbidden("Invalid request method.")


@login_required
@permission_required('News.review_articles', raise_exception=True)
def review_articles(request):
    """View function to review articles pending approval."""
    articles = Article.objects.filter(approved=False)
    return render(request, 'news/review_articles.html', {'articles': articles})


@login_required
@permission_required('News.add_article', raise_exception=True)
def create_article(request):
    """View function to create a new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Set the author to the current user
            article.save()
            if article.approved:
                if hasattr(Tweet, '_instance') and Tweet._instance:
                    new_article_tweet = f"New article posted on NewsHub!\n{article.headline}\n" 
                    tweet = {'text': new_article_tweet} 
                    Tweet._instance.make_tweet(tweet)
                    return redirect('article_list')
                else:
                    print("Tweet client not initialized. Skipping tweet.")
    else:
        form = ArticleForm()
    return render(request, 'news/article_form.html', {'form': form})


@login_required
@permission_required('News.change_article', raise_exception=True)
def update_article(request, pk):
    """View function to update an existing article"""
    article = get_object_or_404(Article, pk=pk)
    # Add check for article ownership
    if article.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this"
                                     "article")
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('view_article', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news/article_form.html', {'form': form})


@login_required
@permission_required('News.delete_article', raise_exception=True)
def delete_article(request, pk):
    """View function to delete an article"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'news/article_confirm_delete.html', {'article':
                                                                article})


def newsletter_list(request):
    """View function to display newsletter options."""
    newsletters = Newsletter.objects.all()
    return render(request, 'news/newsletter_list.html',
                  {'newsletters': newsletters})


def newsletter(request):
    """View to display newsletters."""
    newsletters = Newsletter.objects.all()
    return render(request, 'news/newsletter_list.html', {'newsletters':
                                                    newsletters})


@login_required
@permission_required('News.view_newsletter', raise_exception=True)
def view_newsletter(request, pk):
    """View function to display a newsletter"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'news/newsletter.html', {'newsletter': newsletter})


@login_required
@permission_required('News.add_newsletter', raise_exception=True)
def add_newsletter(request):
    """View to add a newsletter"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()
    return render(request, 'news/newsletter_form.html', {'form': form})


@login_required
@permission_required('News.change_newsletter', raise_exception=True)
def update_newsletter(request, pk):
    """View to update a newsletter"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect('view_newsletter', pk=newsletter.pk)
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'news/newsletter_form.html', {'form': form})


@login_required
@permission_required('News.delete_newsletter', raise_exception=True)
def delete_newsletter(request, pk):
    """View to delete a newsletter"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        newsletter.delete()
        return redirect('newsletter_list')
    return render(request, 'news/newsletter_confirm_delete.html',
                  {'newsletter': newsletter})


def read_more(request):
    """View to display read more page."""
    return render(request, 'news/read_more.html', {})
