from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Profile(models.Model):
    image = models.ImageField(default='img.jpg', upload_to='image', verbose_name='الصورة الشخصية', )
    phone_number = models.CharField(verbose_name='رقم الهاتف', max_length=15)
    small_info = models.TextField(verbose_name='تفاصيل صغيرة', max_length=1000, help_text='تفاصيل صغيرة عن نفسك')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم')
    city = models.CharField(verbose_name='المدينة', max_length=15)
    country = models.CharField(verbose_name='الدولة', max_length=15)

    def __str__(self):
        return self.user.username


# def create_profile(sender, **kwarg):
#     if kwarg['created']:
#         user_profile = Profile.objects.create(user=kwarg['instance'])

# post_save.connect( create_profile , sender = User)