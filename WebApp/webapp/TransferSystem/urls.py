from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.Home, name = 'home' ),
    url(r'^login/$', login, {'template_name':'login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name = 'logout' ),
    url(r'^registered-users/$', views.Registered_Users, name = 'registered-users'),
    url(r'^transfered-articles/$', views.Transfered_Articles, name = 'transfered-articles'),
    url(r'^saved-articles/$', views.Saved_Articles, name = 'saved-articles'),
]
 