from django.urls import path, include
from .views import (
    Regression_view,
)

app_name = 'regression'

urlpatterns = [
    path("", Regression_view.as_view(), name="regression"),
]
