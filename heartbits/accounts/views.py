from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import MyUserCreationForm, MyUserChangeForm, LoginUserForm
from heartbits_app.models import User, Test, Question
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

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

    def get_queryset(self):
        base_qs = super(UserUpdateView, self).get_queryset()
        return base_qs.filter(id=self.request.user.pk)


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('login')



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
