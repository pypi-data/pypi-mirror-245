from django.urls import path
from django.conf import settings

from .views import Versions

patterns = []
if getattr(settings, "DEBUG", False):
    patterns.append(path("versions/", Versions.as_view(), name="versions"))

urlpatterns = patterns
