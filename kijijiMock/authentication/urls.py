from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='authentication'

urlpatterns = [
path('', views.IndexView.as_view(), name='index'), #sets the path for the index view
path('<int:pk>/', views.DetailView.as_view(), name='detail'),#sets the path for the detail view
]+ static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )