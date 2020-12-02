from django.urls import path
from . import views
app_name='itemSale'

urlpatterns = [
path('', views.IndexView.as_view(), name='index'), #sets the path for the index view
path('<int:pk>/', views.DetailView.as_view(), name='detail'),#sets the path for the detail view
]