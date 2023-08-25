from typing import Any

from django.views.generic import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


class HomeView(View):
    template_name = "home.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)
