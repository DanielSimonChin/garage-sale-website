"""kijijiMock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from authentication.views import(
	register,
    logout_view,
    login_view,
    account_view,
    password_view,
    comment,
    reply,
    like,
)

from itemManagement.views import(
    createItemView,
    updateItem,
    deleteItem,
)

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
	path('', include('itemManagement.urls'),name='home'),
	path('register/',register,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('account/',account_view,name='account'),
    path('password/',password_view,name='password'),
    path('<int:pk>/comment/', comment, name ='add_comment'),
    path('<int:pk>/comment/reply/', reply, name ='add_reply'),
    path('<int:pk>/like/', like, name = 'like_item'),
    path('create/',createItemView,name='itemCreate'),
    path('update/<int:pk>/',updateItem,name='itemUpdate'),
    path('delete/<int:pk>/',deleteItem,name='itemDelete'),
]
