from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from main.views import ajaxcolor
urlpatterns = [
    #path('jet/' , include('jet.urls')),
    path('admin/', admin.site.urls),
    path('' , include('main.urls')),
    path('zarinpal/' , include('zarinpal.urls' , namespace='zarinpal')),
    path('accounts/' , include('django.contrib.auth.urls')),

    #path(r'^api/search_auto/' ,search_auto, name='search_auto'),
]




urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL ,document_root=settings.STATIC_ROOT)