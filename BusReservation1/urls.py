"""
URL configuration for BusReservation1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app2 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_view, name='login'),
    path('signup/',views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_signup/', views.admin_signup_view, name='admin_signup'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin_dashboard/add_user/', views.add_user_view, name='add_user'),
    path('admin_dashboard/update_user/<int:user_id>/', views.update_user_view, name='update_user'),
    path('admin_dashboard/delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('manage-buses/', views.manage_buses_view, name='manage_buses'),
    path('add-bus/', views.add_bus_view, name='add_bus'),
    path('update-bus/<int:bus_id>/', views.update_bus_view, name='update_bus'),
    path('delete-bus/<int:bus_id>/', views.delete_bus_view, name='delete_bus'),
    path('user_search/', views.search_buses_view, name='user_search'),
     path('book_bus/<int:bus_id>/', views.book_bus_view, name='book_bus'),
    path('booking_confirmation/', views.booking_confirmation_view, name='booking_confirmation'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin_view_users/', views.admin_view_users, name='admin_view_users'),
    path('admin_view_bookings/', views.admin_view_bookings, name='admin_view_bookings'),
    

]
