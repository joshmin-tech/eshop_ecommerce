from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin,name="adminlogin"),
    path('adminlogoutprocess',views.adminlogoutprocess,name="adminlogoutprocess"),
    path('adminhome',views.adminhome,name='adminhome'),
    path('userview',views.userview,name='userview'),
    path('activeuser/<int:id>',views.activeuser,name='activeuser'),
    path('category',views.category,name='category'),
    path('viewcategory',views.viewcategory,name='viewcategory'),
    path('editcategory/<int:id>',views.editcategory,name='editcategory'),
    path('deletecategory/<int:id>',views.deletecategory,name='deletecategory'),        
    path('add_product',views.add_product,name='add_product'),
    path('view_product',views.view_product,name='view_product'),
    path('editproduct/<int:id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),
    

]