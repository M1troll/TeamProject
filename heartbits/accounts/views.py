from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.db.models.fields import Field
from .forms import MyUserCreationForm, MyUserChangeForm, MyPasswordChangeForm
from heartbits_app.models import User, Test, Question
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.utils.translation import gettext
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView


# Create your views here.


class SignUp(generic.CreateView):
    model = User
    form_class = MyUserCreationForm
    success_url = reverse_lazy('test-render')
    template_name = 'accounts/register.html'


class Login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class Logout(LogoutView):
    next_page = 'main'
    template_name = 'accounts/logout.html'


class UserUpdateView(generic.UpdateView):
    model = User
    slug_field = 'user_url'
    template_name = 'accounts/user_update.html'
    form_class = MyUserChangeForm
    pw_form_class = MyPasswordChangeForm

    def get_queryset(self):
        base_qs = super(UserUpdateView, self).get_queryset()
        return base_qs.filter(id=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        form_initial = dict()
        for field in self.request.user._meta.fields:
            key = field.__str__().split('.')[-1]
            form_initial[key] = field.value_from_object(self.request.user)
        form_initial.pop('password')
        form = self.form_class(initial=form_initial)
        pw_form = self.pw_form_class(self.request.user)
        return self.render_to_response(context={'form': form, 'pw_form': pw_form})


    # def form_valid(self, form):
    #     form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
    #     form.save()
    #     return HttpResponseRedirect(self.get_success_url())


class MyPasswordChangeView(PasswordChangeView):
    success_url = '/user/%s/'
    form_class = MyPasswordChangeForm

    def get(self, request, *args, **kwargs):
        return redirect('user_update', slug=self.request.user.user_url)

    def get_success_url(self):
        self.success_url = self.success_url % self.request.user.user_url
        return str(self.success_url)

# def change_user(request, slug):
#     if request.method == 'POST':
#         form = MyUserChangeForm(request.POST, request.FILES)
#         if form.is_valid():
#             if form.cleaned_data.get('old_password') == request.user.password and \
#                     form.cleaned_data.get('password') == form.cleaned_data.get('password2'):
#                 form.password = make_password(form.cleaned_data.get('password'))
#                 form.save()
#                 print('here')
#                 return render(request, 'accounts/user_update.html', {'user': request.user, 'form': form})
#             return render(request, 'accounts/user_update.html', {'user': request.user, 'form': form})
#     else:
#         user = request.user
#         form_initial = dict()
#         for field in user._meta.fields:
#             key = field.__str__().split('.')[-1]
#             form_initial[key] = field.value_from_object(user)
#         form = MyUserChangeForm(initial=form_initial)
#         return render(request, 'accounts/user_update.html', {'user': user, 'form': form})

# def user_detail(request, slug):
#     if request.method == 'POST':
#         form = MyUserChangeForm(request.POST, request.FILES)
#         if form.is_valid():
#             if form.cleaned_data['password'] == form.cleaned_data['password2']:
#                 user_data = form.save(commit=False)
#                 user_data.password = make_password(form.cleaned_data['password2'])
#                 user_data.save()
#                 form = MyUserChangeForm(form.cleaned_data)
#         context = {'user': request.user,
#                    'form': form}
#         return reverse_lazy('user_detail', kwargs=context)
#     else:
#         form = MyUserChangeForm()
#         return reverse_lazy('user_detail', kwargs={'form': form})


# def login(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['username'],
#                                 password=form.cleaned_data['password'])
#             if user is not None:
#                 return redirect('index', {'user': user})
#             else:
#                 return HttpResponseRedirect('index')
#         return HttpResponseRedirect('index')
#     else:
#         form = LoginUserForm()
#         return render(request, 'accounts/login.html', context={'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             if form.cleaned_data['password'] == form.cleaned_data['password2']:
#                 userdata = form.save(commit=False)
#                 userdata.password = make_password(form.cleaned_data['password2'])
#                 userdata.save()
#                 form.clean()
#         return render(request, 'index')
#     if request.method == 'GET':
#         form = RegisterUserForm()
#         return render(request, 'accounts/register.html', context={'reg_form': form})
#
#
