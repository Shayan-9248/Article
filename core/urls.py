from django.urls import path, include
from . import views
from . import api_views


app_name = 'core'


api_urls = [
    path('article-list/', api_views.ArticleListView.as_view(), name='list'),
    path('article-create/', api_views.ArticleCreate.as_view(), name='create'),
    path('article-update/<int:pk>/', api_views.ArticleUpdate.as_view(), name='update'),
    path('article-delete/<int:pk>/', api_views.ArticleDelete.as_view(), name='delete'),
]


urlpatterns = [
    path('', views.ArticleList.as_view(), name='list'),
    path('search/', views.ArticleList.as_view(), name='search'),
    path('article/<slug:slug>/<int:id>/', views.ArticleDetail.as_view(), name='detail'),
    path('preview/<int:pk>/', views.ArticlePreview.as_view(), name='preview'),
    path('category/<slug:slug>/', views.ArticleList.as_view(), name='category'),
    path('author/<str:username>/', views.AuthorList.as_view(), name='author'),
    path('add-to-favourite/<int:id>/', views.add_favourite, name='add'),
    path('favourite-list/', views.FavouriteList.as_view(), name='fav-list'),
    path('Bucket/', views.BucketObjects.as_view(), name='bucket'),
    path('download-bucket/<str:key>/', views.DownloadObject.as_view(), name='download'),
    path('delete-bucket/<str:key>/', views.DeleteObject.as_view(), name='delete'),
    path('api/', include(api_urls)),
]