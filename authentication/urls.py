from django.urls import path

from .views import FacebookLoginView, ValidateUserTokenView

urlpatterns = [
    path('fb-login', FacebookLoginView.as_view()),
    path('validate-token', ValidateUserTokenView.as_view())
]
