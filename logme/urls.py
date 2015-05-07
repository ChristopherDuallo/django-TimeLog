from django.conf.urls import patterns, url

from logme import views

urlpatterns = patterns('',
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^home/$', views.Home_Page.as_view(), name='home'),
	url(r'^register/$', views.Register.as_view(), name='register'),
)