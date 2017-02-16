from django.conf.urls import url

from . import views
app_name = 'account'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addaccount$', views.add_account, name='add_account'),
    url(r'^acc/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^acc/add_trans/(?P<account_id>[0-9]+)$',views.add_trans,name='addtrans'),
    url(r'^acc/editname/(?P<account_id>[0-9]+)$',views.editname,name='editname'),
]