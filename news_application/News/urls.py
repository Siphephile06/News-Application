from django.urls import path
from . import views


urlpatterns = [
     # URL pattern for displaying articles.
     path('', views.article_list, name='article_list'),
     # URL pattern for displaying home page.
     path('home/', views.home, name='home'),
     # URL pattern for displaying publisher dashboard.
     path('publisher_dashboard/', views.publisher_dashboard,
          name='publisher_dashboard'),
     # URL patter to become a publisher.
     path('become_publisher/', views.become_publisher,
          name='become_publisher'),
     # URL pattern for displaying about page.
     path('about/', views.about, name='about'),
     # URL pattern to display read more page.
     path('read_more/', views.read_more, name='read_more'),
     # URL to display subscribe page.
     path('subscribe/', views.subscribe, name='subscribe'),
     # URL pattern to display subscription success page.
     path('subscription_success/', views.subscription_success,
          name='subscription_success'),
     # URL pattern for editor dashboard.
     path('editor_dashboard/', views.editor_dashboard,
          name='editor_dashboard'),
     # URL for if they are an editor.
     path('is_editor/', views.is_editor, name='is_editor'),
     # URL pattern for subscribing to publishers.
     path('subscribe_publishers/', views.subscription_to_publishers,
          name='subscribe_publishers'),
     # URL pattern for subscribing to journalists.
     path('subscribe_journalists/', views.subscription_to_journalists,
          name='subscribe_journalists'),
     # URL pattern to get available editors.
     path('available_editors/', views.available_editors,
          name='available_editors'),
     # URL pattern to get available journalists.
     path('available_journalists/', views.available_journalists,
          name='available_journalists'),
     # URL patter to assign editor to publisher.
     path('assign_editor/<int:publisher_id>/', views.assign_editor,
          name='assign_editor'),
     # URL patter to assign journalist to publisher.
     path('assign_journalist/<int:publisher_id>/', views.assign_journalist,
          name='assign_journalist'),
     # URL pattern for viewing an article.
     path('article/<int:pk>/', views.view_article, name='view_article'),
     # URL pattern for creating an article.
     path('article/create/', views.create_article, name='create_article'),
     # URL pattern for updating an article.
     path('article/<int:pk>/update/', views.update_article,
          name='update_article'),
     # URL pattern for deleting an article.
     path('article/<int:pk>/delete/', views.delete_article,
          name='delete_article'),
     # URL pattern for displaying articles.
     path('article/', views.article, name='article'),
     # URL pattern for approving articles.
     path('approve_article/<int:pk>/', views.approve_articles,
          name='approve_article'),
     # URL pattern for a specific article.
     path('article/<int:id>/', views.article_detail,
          name='article_detail'),
     # URL pattern for reviewing articles.
     path('review_articles/', views.review_articles,
          name='review_articles'),
     # API endpoint for listing articles.
     path('api/articles/', views.api_article_list, name='api_article_list'),
     # API endpoint for creating articles.
     path('api/articles/create/', views.api_create_article,
          name='api_create_article'),
     # URL pattern for displaying newsletters.
     path('newsletters/', views.newsletter, name='newsletter'),
     # URL pattern for listing newsletters.
     path('newsletters/', views.newsletter_list, name='newsletter_list'),
     # URL pattern for adding a newsletter.
     path('newsletters/add/', views.add_newsletter, name='add_newsletter'),
     # URL pattern for updating a newsletter.
     path('newsletters/update/<int:pk>/', views.update_newsletter,
          name='update_newsletter'),
     # URL pattern for viewing a newsletter.
     path('newsletter/<int:pk>/', views.view_newsletter,
          name='view_newsletter'),
     # URL pattern for deleting a newsletter.
     path('newsletter/<int:pk>/delete/', views.delete_newsletter,
          name='delete_newsletter'),
     # URL pattern for login.
     path('login_user/', views.login_user, name='login'),
     # URL pattern for logout.
     path('logout_user/', views.logout_user, name='logout'),
     # URL pattern for user registration.
     path('register/', views.register_user, name='register'),
     # URL pattern for building an email.
     path('build_email/', views.build_email, name='build_email'),
     # URL pattern to generate reset password url.
     path('generate_reset_url', views.generate_reset_url,
          name='generate_reset_url'),
     # URL to send password reset.
     path('send_password_reset/', views.send_password_reset,
          name='send_password_reset'),
     # URL to reset user password.
     path('reset_user_password/', views.reset_user_password,
          name='reset_user_password'),
     # URL to reset password.
     path('reset_password/', views.reset_password,
          name='reset_password'),
]
