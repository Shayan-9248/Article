from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('log-out/', views.Logout.as_view(), name='log-out'),
    path('account/', views.Account.as_view(), name='account'),
]