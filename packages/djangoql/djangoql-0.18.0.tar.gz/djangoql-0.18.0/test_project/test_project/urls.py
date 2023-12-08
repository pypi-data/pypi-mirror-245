"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin


try:
    from django.urls import re_path  # Django >= 4.0
except ImportError:
    try:
        from django.conf.urls import re_path  # Django < 4.0
    except ImportError:  # Django < 2.0
        from django.conf.urls import url as re_path

from core.admin import zaibatsu_admin_site
from core.views import completion_demo


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^zaibatsu-admin/', zaibatsu_admin_site.urls),
    re_path(r'^$', completion_demo),
]

if settings.DEBUG and settings.DJDT:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
