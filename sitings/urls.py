from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)