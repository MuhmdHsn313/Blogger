from django import template
from blog.models import Post, Command
import math

register = template.Library()


@register.inclusion_tag('blog/latest_posts.html')
def latest_posts():
    context = {
        'latest_posts': Post.objects.all()[0:5]
    }
    return context


@register.inclusion_tag('blog/latest_command.html')
def latest_commands():
    cmnds = Command.objects.order_by('-date_command', ).filter(active=True)
    context = {
        'latest_commands': cmnds[:5]
    }
    return context


# @register.inclusion_tag('blog/user_posts.html')
# def user_posts(user):
#     limit = 5
#     posts = Post.objects.filter(author=user).order_by('-post_date')
#     # posts_pages_number = math.ceil(posts.count() / limit)
#     return {'posts': posts}
