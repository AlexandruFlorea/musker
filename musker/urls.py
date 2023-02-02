from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('accounts/register/', views.register_user, name='register'),
    path('create/', views.MeepCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.MeepUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MeepDeleteView.as_view(), name='delete'),
    path('search/', views.search_site, name='search')
]
