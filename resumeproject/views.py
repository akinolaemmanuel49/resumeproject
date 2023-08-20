from typing import Any

from django.views.generic import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


class HomeView(View):
    template_name = "home.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            print("DUMMY SIDE RESUME ID:", request.session["resume_id"])
        except Exception:
            print("DUMMY SIDE RESUME ID NOT SET")
        print("REMOTE IP ADDR: ", request.META["REMOTE_ADDR"])
        return render(request, self.template_name)
