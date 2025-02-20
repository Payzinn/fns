from django.urls import path
from . import views
urlpatterns = [
    path("", views.submit_form, name="submit_form"),
    path("success/", views.some_success_view, name='success'),
]
