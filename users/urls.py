from django.urls import path
from .views import LoginView,  SignUpView,UserLoginView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LoginView.as_view(), name='logout'),
]