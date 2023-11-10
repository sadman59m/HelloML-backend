from django.urls import path, include
from .views import (
    Regression_view,
    file_download_view,
)

app_name = 'regression'

urlpatterns = [
    path("", Regression_view.as_view(), name="regression"),
    path("download/", file_download_view, name="download-file"),
]
