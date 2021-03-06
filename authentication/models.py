import hashlib
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .choices import GENDER_CHOICES, ROLE_CHOICES
from core.choices import EDUCATION_CHOICES, MENTORSHIP_AREAS_CHOICES
from activities.models import Notification

from multiselectfield import MultiSelectField

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

DEFAULT = 'profiles/default.jpg'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, default='')
    bio = models.TextField(default='')
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default=''
    )
    role = models.CharField(
        max_length=6,
        blank=False,
        default='mentee',
        choices=ROLE_CHOICES
    )
    phone_number = models.CharField(max_length=32, default='')
    mentorship_areas = MultiSelectField(
        choices=MENTORSHIP_AREAS_CHOICES,
        max_choices=3,
        default=''
    )
    highest_level_of_study = models.CharField(
        max_length=255,
        choices=EDUCATION_CHOICES,
        default=''
    )
    is_previously_logged_in = models.CharField(max_length=5, default=False)
    email_confirmed = models.BooleanField(default=False)
    profile_picture = ProcessedImageField(
        upload_to='profiles',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 99},
        default=DEFAULT,
    )

    def is_mentor(self):
        return self.role == 'mentor'

    def is_mentee(self):
        return self.role == 'mentee'

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username

    def get_gravatar(self):
        gravatar_url = 'https://www.gravatar.com/avatar/{0}?{1}'.format(
            hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest(),
            urlencode({'s': '256'})
        )
        return gravatar_url

    def get_screen_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_also_answered(self, question):
        answers = question.get_answers()
        users = []
        for answer in answers:
            if answer.user != self.user and answer.user != question.user:
                users.append(answer.user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_ANSWERED,
                         from_user=self.user, to_user=User(id=user),
                         question=question).save()

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()

    def notify_article_commented(self, article):
        if self.user != article.create_user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user,
                         to_user=article.create_user,
                         article=article).save()

    def also_article_commented(self, article):
        comments = article.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != article.create_user:
                users.append(article.create_user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user, to_user=User(id=user),
                         article=article).save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)


class Interest(models.Model):
    user = models.OneToOneField(
        User,
        blank=True, on_delete=models.CASCADE)
    stem = models.BooleanField(blank=True, default=False)
    entrepreneurship = models.BooleanField(blank=True, default=False)
    career_counseling = models.BooleanField(blank=True, default=False)
    career_readiness = models.BooleanField(
        db_column="career_readiness",
        verbose_name='career_readiness',
        blank=True, default=False)
    addictions = models.BooleanField(blank=True, default=False)

    class Meta:
        db_table = "interests"

    def __unicode__(self):
        return unicode(self.user.username)


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.IntegerField(null=False)
    status = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return unicode(self.user)
