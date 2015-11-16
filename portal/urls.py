from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^base/', TemplateView.as_view(template_name="login.html")),
]
