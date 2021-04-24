from django.urls import path

from .views import UrlView, ViewerView, UrlDetailView

urlpatterns = [
    path('url', UrlView.as_view()),
    path('url/<int:pk>', UrlDetailView.as_view()),
    path('view/<short_url>', ViewerView.as_view())
]
