from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='model'),
    path('',views.home,name='home'),
    path('login/',views.auth_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_request,name='logout'),
    

]