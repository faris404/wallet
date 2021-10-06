from django.urls import path

from .views import UserSignup,Test,PearsonView

urlpatterns = [
    path('signup/',UserSignup.as_view()),
    path('test/',Test.as_view()),
    path('test/',Test.as_view()),
    path('persons/',PearsonView.as_view())
]
