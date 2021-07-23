from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    
    path('otp_login/',views.otp_login,name="otp_login"),
    path('otp_verify/',views.otp_verify,name="otp_verify"),
    path('user_profile_dashboard/',views.user_profile_dashboard,name='user_profile_dashboard'),
    path('user_profile_address/',views.user_profile_address,name='user_profile_address'),
    path('user_profile_add_address/',views.user_profile_add_address,name='user_profile_add_address'),
    path('user_profile_edit_address/<int:id>/',views.user_profile_edit_address,name='user_profile_edit_address'),
    path('user_profile_delete_address/<int:id>/',views.user_profile_delete_address,name='user_profile_delete_address'),    
    path('user_profile_order/',views.user_profile_order,name='user_profile_order'),  
    path('user_profile_order_details/<int:id>/',views.user_profile_order_details,name='user_profile_order_details'),
    path('user_cancelled_product/<int:id>/',views.user_cancelled_product,name='user_cancelled_product'),
    path('user_profile_refer/',views.user_profile_refer,name='user_profile_refer'),  
    path('user_propic/',views.user_propic,name='user_propic'),  
    
    # password reset
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),  
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),      
    path('resetPassword/',views.resetPassword,name='resetPassword'),  

   
    
]