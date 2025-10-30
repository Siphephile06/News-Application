from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Publisher
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=CustomUser)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")
        if instance.role:
            try:
                group = Group.objects.get(name=instance.role)
                instance.groups.add(group)
                print(f"Assigned {instance.username} to group {instance.role}")
            except Group.DoesNotExist:
                print(f"Group {instance.role} does not exist")


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    role_permissions = {
        'reader': ['view_article', 'view_newsletter'],
        'editor': ['view_article', 'view_newsletter', 'change_article',
                   'change_newsletter', 'delete_article', 'delete_newsletter',
                   'review_articles', 'approve_article'],
        'journalist': ['view_article', 'view_newsletter', 'add_article',
                       'add_newsletter', 'change_article',
                       'change_newsletter', 'delete_article',
                       'delete_newsletter'],
    }

    for role, perms in role_permissions.items():
        group, _ = Group.objects.get_or_create(name=role)
        permissions = Permission.objects.filter(codename__in=perms)
        group.permissions.set(permissions)
        group.save()


def notify_subscribers_and_tweet(article):
    if not article.approved:
        return

    journalist = article.author
    publisher_qs = Publisher.objects.filter(journalists=journalist)

    publisher_subs = CustomUser.objects.filter(
        subscriptions_to_publishers__in=publisher_qs
    ).distinct()

    journalist_subs = CustomUser.objects.filter(
        subscriptions_to_journalists=journalist
    ).distinct()

    emails = set(publisher_subs.values_list('email', flat=True)) | set(
        journalist_subs.values_list('email', flat=True))

    if emails:
        send_mail(
            subject=f"New Article: {article.headline}",
            message=f"{article.body}\n\n{article.conclusion}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(emails),
            fail_silently=False,
        )
