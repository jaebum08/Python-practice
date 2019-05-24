from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.log_out),
    url(r'^quotes', views.quotes),
    url(r'^add_quote$', views.add_quotes),
    url(r'^user/(?P<user_id>\d+)$', views.user_index),
    url(r'^myaccount/(?P<user_id>\d+)$', views.myaccount_index),
    url(r'^edit/(?P<user_id>\d+)$', views.edit_account),
    url(r'^delete/(?P<quote_id>\d+)$', views.delete),
    url(r'^like/(?P<quote_id>\d+)$', views.like),
]
