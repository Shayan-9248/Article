from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.ArticleList.as_view(), name='list'),
    path('search/', views.ArticleList.as_view(), name='search'),
    path('article/<slug:slug>/<int:id>/', views.ArticleDetail.as_view(), name='detail'),
    path('preview/<int:pk>/', views.ArticlePreview.as_view(), name='preview'),
    path('category/<slug:slug>/', views.ArticleList.as_view(), name='category'),
    path('author/<str:username>/', views.AuthorList.as_view(), name='author'),
    path('add-to-favourite/<int:id>/', views.add_favourite, name='add'),
    path('favourite-list/', views.FavouriteList.as_view(), name='fav-list'),
]