from django.conf.urls import patterns, include, url
from django.contrib import admin
from feedback import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentFeedback.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addcourse/$', views.addCourse, name='addCourse'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^addfeedback/$', views.addFeedback, name='addFeedback'),
    url(r'^otp/$', views.otp, name='otp')
)