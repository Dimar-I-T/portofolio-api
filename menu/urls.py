from django.urls import path
from .views import login_admin_view
from .views import dashboard_view

urlpatterns = [
    path('login-admin/', login_admin_view, name='login_admin'),
    path('dashboard/', dashboard_view, name='dashboard')
]