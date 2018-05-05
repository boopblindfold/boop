from django.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='Home'),
    url(r'^Survey/', include('Survey.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^Outlook/', include('Outlook.urls')),
    url(r'^aboutUs/', views.aboutUs, name='aboutUs'),
    url(r'^contactUs/', views.contactUs, name='contactUs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)