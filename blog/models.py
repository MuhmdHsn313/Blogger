from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان التدوينة', help_text='الحد الاقصى 100 خانة')
    content = models.TextField(verbose_name='نص التدوينة')
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-post_date',)


class Command(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان التعليق", help_text='اجعل العنوان وصفاً لعموم للتعليق')
    body = models.TextField(verbose_name='التعليق')
    user_command = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_command', verbose_name='المعلق')
    date_command = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التعليق')
    active = models.BooleanField(default=True, verbose_name='الفعالية')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='command', verbose_name='التدوينة')

    def __str__(self):
        return self.title
