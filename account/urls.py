from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('log-out/', views.Logout.as_view(), name='log-out'),
    path('account/', views.Home.as_view(), name='account'),
    path('article-create/', views.ArticleCreate.as_view(), name='create'),
    path('article-delete/<slug:slug>/<int:id>/', views.DeleteArticle.as_view(), name='delete')
]