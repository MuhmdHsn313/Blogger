from django import forms
from django.contrib.auth.forms import User, UserCreationForm
from .models import Profile

help_password_text = "فيما يلي ملاحظات تتعلق بكلمة المرور" \
                     "<ul>" \
                     "<li><small>يجب ان تحوي على 8 خانات فأكثر</small></li>" \
                     "<li><small>لا تجعلها أرقاماً فقط</small></li>" \
                     "<li><small>راعي عدم كونها كلمة سر شائعة</small></li>" \
                     "<li><small>راعي عدم تشابهها كثيرا لمعلوماتك الشخصية</small></li>" \
                     "</ul>"


class UserCreateForm(forms.ModelForm):
    username = forms.CharField(label='إسم المستخدم', max_length=50, help_text='مطلوب. الحد الاعلى 50 خانة (تشمل '
                                                                              'الحروف والارقام والرموز  @ . + - _ )')
    email = forms.EmailField(label='البريد الإلكتروني', required=False)
    first_name = forms.CharField(label='الإسم', required=False)
    last_name = forms.CharField(label='اللقب', required=False)
    password1 = forms.CharField(label='كلمة المرور', min_length=8, max_length=50,
                                help_text=help_password_text, widget=forms.PasswordInput())
    password2 = forms.CharField(label='تأكيد كلمة المرور', min_length=8, max_length=50, widget=forms.PasswordInput(),
                                help_text='أدخل كلمة مرور مشابهة لماقبلها.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                'كلمة المرور غير متطابقة!',
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بإسم المستخدم هذا!')
        return cd['username']


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='إسم المستخدم', max_length=50, help_text='أدخل إسم المستخدم الخاص بك!')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):

    image = forms.ImageField(required=False)
    phone_number = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('image', 'phone_number', 'small_info', 'city', 'country')
