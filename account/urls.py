from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('log-out/', views.Logout.as_view(), name='log-out'),
    path('account/', views.Home.as_view(), name='account'),
    path('article-create/', views.ArticleCreate.as_view(), name='create'),
    path('article-update/<int:pk>/', views.ArticleUpdate.as_view(), name='update'),
    path('article-delete/<int:pk>/', views.DeleteArticle.as_view(), name='delete'),
    path('user-profile/', views.UserProfile.as_view(), name='profile'),
]