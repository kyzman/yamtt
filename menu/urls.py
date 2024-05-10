from django.urls import path
from menu import views

app_name = 'menu'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('expanded', views.ExpandedView.as_view(), name='expanded'),
    path('<path:url>', views.IndexView.as_view(), name='other'),
]
