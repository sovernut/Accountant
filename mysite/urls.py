from django.conf.urls import include, url
from django.contrib import admin

from . import views # for index
urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', admin.site.urls),
]