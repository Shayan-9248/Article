from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
    path('', include('core.urls', namespace='core')),
    path('', include('account.urls', namespace='account')),
    path('', include('payment.urls', namespace='payment')),
]
