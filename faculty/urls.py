from django.conf.urls import patterns, include, url
from django.contrib import admin
from faculty import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentFeedback.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^otp/$', views.otp, name='otp'),
    url(r'^addQuestion/$', views.addQuestion, name='addQuestion'),
  #  url(r'^getFeedback/$',views.getFeedback,name='getFeedback')

)