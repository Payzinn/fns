from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.submit_form, name="submit_form"),
    path("success/", views.some_success_view, name='success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
