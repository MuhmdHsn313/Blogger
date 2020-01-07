from django.urls import path
from user import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView # user with third login way

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('login/', views.login_user, name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('<str:username>', views.profile_user, name='profile'),
    path('<str:username>/edit', views.edit_profile, name='edit_profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
