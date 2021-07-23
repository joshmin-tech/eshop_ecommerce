from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),  
    path('carts/',views.carts,name='carts'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('testcart/',views.testcart,name='testcart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('collect_address/',views.collect_address,name='collect_address'),
     
    
    
]