from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
    path('', include('core.urls', namespace='core')),
    path('', include('account.urls', namespace='account')),
    path('', include('payment.urls', namespace='payment')),
]


AdminSite.site_header = 'Max Admin'
admin.site.site_title = 'Admin Panel'
admin.site.index_title = 'Welcome To Admin Panel'
