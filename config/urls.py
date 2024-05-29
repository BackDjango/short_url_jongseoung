"""
URL configuration for short_url_jongseoung project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os

from django.conf import settings

from django.contrib import admin
from django.urls import path, include

from config.settings.swagger.setup import get_swagger_urls

directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "api", "versions"
)

api_urls = []
version_map_dict = {}

for (
    _path,
    _,
    _files,
) in os.walk(directory):
    depth = _path[len(directory) + len(os.path.sep) :].count(os.path.sep)
    if _path != directory and depth == 1 and "urls.py" in _files:
        version, api_name = _path.split(os.path.sep)[-2:]

        if not version_map_dict.get(version, None):
            version_map_dict[version] = []

        _include = "api.versions.{}.{}.urls".format(version, api_name)

        api_urls.append(path(f"{version}/", include(_include)))


urlpatterns = [
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += get_swagger_urls()
