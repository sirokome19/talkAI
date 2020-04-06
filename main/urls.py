from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
app_name = "main"

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
]
urlpatterns += staticfiles_urlpatterns()
