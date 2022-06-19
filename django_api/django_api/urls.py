from django.contrib import admin
from django.urls import path, re_path
from db import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/orders/$', views.orders_list),
    re_path(r'^api/orders/([0-9])$', views.orders_detail),
]