from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'interface.views.home_page', name='index'),
    url(r'^sign_up', 'interface.views.sign_up', name='sign_up'),
    url(r'^user_login', 'interface.views.user_login', name='user_login'),
    url(r'^home', 'interface.views.user_home', name='home'),
    url(r'^logout', 'interface.views.user_logout', name='logout'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
