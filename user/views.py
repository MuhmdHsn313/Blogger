from django.shortcuts import render, redirect
from blog.models import Post
from user.forms import UserCreateForm, UserLoginForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':  # check connection method if found or not.
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username, password = form.cleaned_data['username'], form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            user.profile = UserProfileForm()
            if user is not None:
                login(request, user)
                messages.success(request, 'تمت عملية التسجيل بنجاح، {} تم توجيهك للصفحة الرئيسية!'.format(username))
                return redirect('home')
            else:
                messages.success(request, 'تمت عملية التسجيل بنجاح، {} قم بتسجيل الدخول!'.format(username))
                return redirect('home')
    else:
        form = UserCreateForm()

    content = {
        'title': 'تسجيل عضو جديد',
        'form': form
    }
    return render(request, 'user/register.html', content)


# first way to login we'll use [LoginView] in urls.py

# second way
def login_user(request):
    """
        second way to login we'll use UserLoginForm class that we creation in user/forms.py file
        this the code of the second way using our Model & request.method
    """
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = UserLoginForm()
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'إسم المستخدم او كلمة المرور غير صحيحة!')
    else:
        form = UserLoginForm()

    return render(request, 'user/login.html', {
        'title': 'تسجيل الدخول',
        'form': form
    })


# third way
# def login_user(request):
#     """
#     this is the third way to login, it's depended on live HTML Form code and 'POST' request method.
#     """
#     if request.user.is_authenticated:
#         return redirect('home')
#     elif request.method == 'POST':
#         username, password = request.method['username'], request.method['password']
#         user_auth = authenticate(request, username=username, password=password)
#         if user_auth is not None:
#             login(request, user_auth)
#             messages.success(request, 'تم تسجيل دخولك بنجاح!')
#             return redirect('home')
#         else:
#             messages.warning(request, 'تأكد من اسم المستخدم او كلمة المرور')
#
#     return render(request, 'user/login.html', {'title': 'تسجيل الدخخول'})


def logout_user(request):
    logout(request)
    return redirect('home')


def profile_user(request, username):
    user = User.objects.filter(username=username).first()
    user_posts = Post.objects.filter(author=user)
    page = request.GET.get('page')
    paginator = Paginator(user_posts, 5)
    try:
        user_posts = paginator.page(page)
        if int(page) > paginator.num_pages:
            return render(request, 'user/profile.html',
                          {'title': 'الملف الشخصي', 'user_page': user, 'none': 'لم يتم التحديد',
                           'posts': user_posts, }, )
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)

    context = {
        'title': 'الملف الشخصي',
        'user_page': user,
        'none': 'لم يتم التحديد',
        'posts': user_posts,
    }
    if user:
        return render(request, 'user/profile.html', context)
    else:
        messages.error(request, 'لا يوجد مستخدم مسجل')
        return redirect('home', )


def edit_profile(request, username):
    if request.user.is_anonymous:
        messages.error(request, 'خطأ في تنفيذ العملية!')
        return redirect('home')

    context = {
        'title': 'تعديل الحساب',
    }

    if request.method == 'POST':
        newProfile = UserProfileForm(data=request.POST)
        if newProfile.is_valid():
            np = newProfile.save(commit=False)
            np.user = request.user
            np.save()
            messages.success(request, 'تم تحديث ملفك الشخصي!')
            return redirect('profile', request.user.username)
    elif request.user.profile.DoesNotExist:
        request.user.profile = UserProfileForm()
        context['form'] = UserProfileForm()
    else:
        context['form'] = request.user.profile

    return render(request, 'user/edit_profile.html', context)
