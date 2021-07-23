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
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('view_order/',views.view_order,name='view_order'),
    path('order_status/<int:id>',views.order_status,name='order_status'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('monthly_report/',views.monthly_report,name='monthly_report'),
    path('yearly_report/',views.yearly_report,name='yearly_report'),
    path('datewise_report/',views.datewise_report,name='datewise_report'),
    path('offer_add/',views.offer_add,name='offer_add'),
    path('offer_category/',views.offer_category,name='offer_category'), 
    path('offer_product/',views.offer_product,name='offer_product'),
    path('offer_view/',views.offer_view,name='offer_view'),
    path('delete_category_offer/<int:id>',views.delete_category_offer,name='delete_category_offer'),
    path('delete_product_offer/<int:id>',views.delete_product_offer,name='delete_product_offer'), 
    path('coupon_view/',views.coupon_view,name='coupon_view'),  
    path('coupon_add/',views.coupon_add,name='coupon_add'),
    path('coupon_delete/<int:id>',views.coupon_delete,name='coupon_delete'),
    path('rating/',views.rating,name='rating'),
    path('rating_block/<int:id>',views.rating_block,name='rating_block'), 
    path('rating_unblock/<int:id>',views.rating_unblock,name='rating_unblock'), 
    # path('apply_coupon/',views.apply_coupon,name='apply_coupon'), 
    
    
    

    

]