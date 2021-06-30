from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('otp_login/',views.otp_login,name="otp_login"),
    path('otp_verify/',views.otp_verify,name="otp_verify"),
    
    
    # path('sentotp/',views.sentotp,name="sentotp"),
    
]