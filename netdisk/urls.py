"""netdisk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from disk import views as disk_view

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', disk_view.home),
    url(r'^user/(?P<user>\w+)$', disk_view.file_list),
    url(r'^upload/$', disk_view.file_upload, name='file_up'),
    url(r'^download/$', disk_view.file_down, name='file_down'),
    url(r'^login/$', disk_view.user_login, name='user_login'),
    url(r'^logout/$', disk_view.user_logout, name='user_logout'),
    url(r'^sign/$', disk_view.user_sign, name= 'user_sign'),
]
