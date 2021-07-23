from django.urls import path,include
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/<int:order_id>',views.payments,name='payments'),
    path('payment_method_paypal/',views.payment_method_paypal,name='payment_method_paypal'),
    path('payment_complete/',views.payment_complete,name='payment_complete'),
    
    path('invoice/<int:order_id>/',views.invoice,name='invoice'),
    path('razor_pay/',views.razor_pay,name='razor_pay'),
    path('submit_review/<int:product_id>',views.submit_review,name='submit_review'),



     
    
    
]