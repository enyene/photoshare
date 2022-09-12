from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
# Create your views here.

class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')


    def form_valid(self,form):
        view = super(SignUpView,self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request,user)
        return view


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('core:list')