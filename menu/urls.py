from django.urls import path
from menu.views import IndexView

app_name = 'menu'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
