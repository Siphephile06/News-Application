from django.test import TestCase
from .models import Article
from django.urls import reverse


class ArticleModelTest(TestCase):
    """Test for the Artcle Model"""
    # Set up values for testing
    def setUp(self):
        self.headline = "Test Headline"
        self.byline = "Test Byline"
        self.body = "Test Body"
        self.conclusion = "Test Conclusion"

        Article.objects.create(headline=self.headline,
                               byline=self.byline,
                               body=self.body,
                               conclusion=self.conclusion)

    def test_article_creation(self):
        article = Article.objects.get(headline=self.headline)
        self.assertEqual(article.byline, self.byline)
        self.assertEqual(article.body, self.body)
        self.assertEqual(article.conclusion, self.conclusion)


class ArticleViewsTest(TestCase):
    """Test the different views concerning the article model"""
    # Set up values for testing
    def setUp(self):
        self.headline = "Test Headline"
        self.byline = "Test Byline"
        self.body = "Test Body"
        self.conclusion = "Test Conclusion"

    def test_article_list(self):
        # Get the url for the article list view
        url = reverse('news:article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles available.")

    def test_view_article(self):
        # Create an article to view
        article = Article.objects.create(headline=self.headline,
                                         byline=self.byline,
                                         body=self.body,
                                         conclusion=self.conclusion)
        url = reverse('news:view_article', args=[article.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.headline)
        self.assertContains(response, self.byline)

    def test_create_article_post(self):
        url = reverse('news:create_article')
        data = {
            'headline': 'New Headline',
            'byline': 'New Byline',
            'body': 'New Body',
            'conclusion': 'New Conclusion'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(headline='New Headline').exists())

    def test_update_article_post(self):
        # Create an article to update.
        article = Article.objects.create(headline=self.headline,
                                         byline=self.byline,
                                         body=self.body,
                                         conclusion=self.conclusion)
        url = reverse('news:update_article', args=[article.pk])
        updated_data = {
            'headline': 'Updated Headline',
            'bylline': 'Updated Byline',
            'body': 'Updated Body',
            'conclusion': 'Updated Conclusion'
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)

        article.refresh_from_db()
        self.assertEqual(article.headline, 'Updated Headline')
        self.assertEqual(article.byline, 'Updated Byline')
        self.assertEqual(article.body, 'Updated Body')
        self.assertEqual(article.conclusion, 'Updated Conclusion')

    def test_delete_article_post(self):
        # Create an article to delete.
        article = Article.objects.create(headline=self.headline,
                                         byline=self.byline,
                                         body=self.body,
                                         conclusion=self.conclusion)
        url = reverse('news:delete_article', args=[article.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())
