from django.urls import path
from . import views
urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

#WHO IS LOGGED IN, WILL BE SENT TO THE DASHBOARD
    path('dashboard/', views.dashboard, name="dashboard"),

]