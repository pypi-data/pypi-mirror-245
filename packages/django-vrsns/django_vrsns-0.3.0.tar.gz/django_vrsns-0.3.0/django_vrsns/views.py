from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

import pkgutil
import importlib


class Versions(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        versions = {}
        for _, name, ispkg in pkgutil.iter_modules():
            if ispkg:
                try:
                    versions[name] = importlib.metadata.version(name)
                except Exception:
                    pass
        return JsonResponse(dict(sorted(versions.items())))
