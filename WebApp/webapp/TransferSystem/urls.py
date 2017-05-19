from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.Home_View.as_view(), name = 'home' ),
    url(r'^login/$', login, {'template_name':'login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name = 'logout' ),

    url(r'^registered-users/$', views.Registered_Users.as_view(), name = 'registered-users'),

    url(r'^registered-users/delete/(?P<pk>\d+)/$', views.Delete_User.as_view(), name = 'delete-user'),

    url(r'^registered-users/register/$', views.Register_User.as_view(), name = 'register-user'),

    url(r'^transfered-articles/$', views.Transfered_Articles.as_view(), name = 'transfered-articles'),

    url(r'^transfered-articles/transfer/$', views.Transfer_Article.as_view(), name = 'transfer-article'),

    url(r'^transfered-articles/confirm/(?P<article_ids>[&0-9+]+)/$', views.Confirm_Article.as_view(), name = 'confirm-article'),

    url(r'^saved-articles/$', views.Saved_Articles.as_view(), name = 'saved-articles'),	

	url(r'^saved-articles/save/$', views.Save_Article.as_view(), name = 'save-article'),

	url(r'^saved-articles/modify/(?P<article_id>\d+)/$', views.Modify_Article.as_view(), name = 'modify-article'),

    url(r'^saved-articles/delete/(?P<article_id>\d+)/$', views.Delete_Article.as_view(), name = 'delete-article'),
]
 