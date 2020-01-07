from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Command
from .forms import NewCommand, NewPost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

posts = Post.objects.all()


def updatePosts():
    global posts
    posts = Post.objects.all()


def home(request):
    global posts
    posts_sub = posts
    page = request.GET.get('page')
    paginator = Paginator(posts_sub, 10)
    try:
        posts_sub = paginator.page(page)
        if int(page) > int(paginator.num_pages):
            return render(request, 'blog/index.html', {
                'title': 'الرئيسية',
                'posts': posts_sub,
            },
                          )
    except PageNotAnInteger:
        posts_sub = paginator.page(1)
    except EmptyPage:
        posts_sub = paginator.page(paginator.num_pages)
    context = {
        'title': 'الرئيسية',
        'posts': posts_sub,
    }
    return render(request, 'blog/index.html', context, )


def about(request):
    context = {
        'title': 'من نحن',
    }
    return render(request, 'blog/about.html', context)


def post_details(request, post_id):
    post_select = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        command_form = NewCommand(data=request.POST)
        if command_form.is_valid():
            new_cmd = command_form.save(commit=False)
            # if request.user.is_superuser or request.user.is_staff:
            #     new_cmd.active = True
            new_cmd.post = post_select
            new_cmd.user_command = request.user
            new_cmd.save()
            command_form = NewCommand()
    else:
        command_form = NewCommand()
    post_commands = post_select.command.filter(active=True)
    context = {
        'title': post_select.title,
        'post': post_select,
        'post_commands': post_commands,
        'commands_form': command_form
    }
    return render(request, 'blog/post.html', context)


def new_post(request):
    if request.user.is_anonymous:
        messages.error(request, 'قم بـتسجيل الدخول لتتمكن من النشر')
        return redirect('home')
    elif request.method == 'POST':
        post_form = NewPost(data=request.POST)
        if post_form.is_valid():
            np = post_form.save(commit=False)
            np.author = request.user
            np.save()
            updatePosts()
            messages.success(request, 'تم نشر تدوينتك بنجاح!')
            return redirect('home')
    post_form = NewPost()
    return render(request, 'blog/create_new_post.html', {'title': 'تدوينة جديدة', 'form': post_form})
