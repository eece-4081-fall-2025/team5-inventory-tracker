from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/assets/', views.api_assets_list, name='api_assets_list'),
    path('api/assets/<int:asset_id>/', views.api_asset_detail, name='api_asset_detail'),
    path('api/users/', views.api_users_list, name='api_users_list'),
]