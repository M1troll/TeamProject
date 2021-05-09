from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import MyUserCreationForm, MyUserChangeForm, MyPasswordChangeForm
from heartbits_app.models import User, UserRating
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


class MyPasswordChangeView(PasswordChangeView):
    success_url = '/user/%s/'
    form_class = MyPasswordChangeForm

    def get(self, request, *args, **kwargs):
        return redirect('user_update', slug=self.request.user.user_url)

    def get_success_url(self):
        self.success_url = self.success_url % self.request.user.user_url
        return str(self.success_url)
