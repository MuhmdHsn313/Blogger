from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>', views.post_details, name='post'),
    path('new_post/', views.new_post, name='new_post')
]
