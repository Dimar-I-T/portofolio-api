from django.urls import path
from .views import skill_view
from .views import skill_tools_view
from .views import links_view

urlpatterns = [
    path('skills/', skill_view, name='skills'),
    path('skills-tools/', skill_tools_view, name='skills-tools'),
    path('links/', links_view, name='links')
]