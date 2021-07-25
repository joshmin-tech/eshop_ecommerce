from store.models import CategoryOffer, ProductOffer,coupon,UsedOffer, ReviewRating
from order.forms import OrderStatus
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from accounts.models import Account
from order.models import Order, OrderProduct
from category.models import Category
from .forms import *
from django.contrib import messages
from store.models import Product
from order.models import Payment
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.core.files.base import ContentFile
import base64
from django.db.models import Sum
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

securename='joshmin'
password1='1234'

@never_cache
def adminlogin(request):
    if request.session.get('logedin'):
        return redirect('adminhome')
    else:
        if request.method=="POST":
            adminname=request.POST['username']
            password=request.POST['password']
            
            if adminname==securename and password==password1:
                request.session['logedin']=True
                return redirect('adminhome')
            elif adminname!=securename:
                messages.info(request,'credential not correct')
                return redirect('adminlogin')
    
        return render(request,"admin/adminlogin.html")

@never_cache
def adminlogoutprocess(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return HttpResponseRedirect(reverse("adminlogin"))

@never_cache
def adminhome(request):
    if request.session.get('logedin') != True:
        return redirect('adminlogin')
    else:
        total_order=Order.objects.all().count()
        order=Order.objects.all()
        sales=0
        for i in order:
            sales=sales+i.order_total
      
    
      

        
        
        sum_paypal = Payment.objects.filter(payment_method='PayPal').aggregate(sum_paypal=Sum('amount_paid'))['sum_paypal']
        sum_cod = Payment.objects.filter(payment_method='cod').aggregate(sum_cod=Sum('amount_paid'))['sum_cod']
        sum_razor = Payment.objects.filter(payment_method='razorpay').aggregate(sum_razor=Sum('amount_paid'))['sum_razor']
        
        pend=OrderProduct.objects.filter(status='Pending',user_cancelled=False).count()
        accept=OrderProduct.objects.filter(status='Accepted').count()
        cancelled=OrderProduct.objects.filter(status='Cancelled').count()
        deliver=OrderProduct.objects.filter(status='Completed').count()
        user_cancelled=OrderProduct.objects.filter(user_cancelled=True).count()
        
        
        
        
        
       
        context={
            'total_order': total_order,
            'sales':sales,
            
            'sum_paypal': sum_paypal,
            'sum_cod': sum_cod,
            'sum_razor': sum_razor,
            
            'pend': pend,
            'accept': accept,
            'cancelled': cancelled,
            'deliver': deliver,
            'user_cancelled': user_cancelled,
        }
        return render(request,'admin/base_template.html',context)

@never_cache
def userview(request):
    if request.session.get('logedin') != True:
        return redirect('adminlogin')
    else:
        userdetails=Account.objects.all()
        paginator=Paginator(userdetails,10)
        page=request.GET.get('page')
        paged_users=paginator.get_page(page)
        return render(request,'admin/adminuserview.html',{'userdata':paged_users})

def activeuser(request,id):
    if request.session.get('logedin') !=True:
        return redirect('loginadmin')
    else:
        status = Account.objects.get(id=id)
        if status.is_active:
            status.is_active = False
        else:
            status.is_active = True
        status.save()
        return redirect('userview')
    

@never_cache
def category(request):
    if request.session.get('logedin') !=True:
        return redirect('adminlogin')
    else:
        if request.method=='POST':
            form=CategoryForms(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'Category added successfully!')
        forms=CategoryForms()
        return render(request,'admin/addcategory.html',{'form':forms})

@never_cache
def viewcategory(request):
    cat_view = Category.objects.all()
    return render(request,'admin/viewcategory.html',{'catview':cat_view})



def editcategory(request,id):
    if request.session.get('logedin') !=True:
        return redirect('adminlogin')
    else:
        if request.method=='POST':
            cat_view = Category.objects.get(id=id)
            form = CategoryForms(request.POST, instance = cat_view)
            if form.is_valid():
                form.save()
                return redirect('viewcategory')
        else:
            cat_view = Category.objects.get(id=id)
            form = CategoryForms(instance=cat_view)
            context = {'heading': 'Edit category','form': form}
            return render(request,'admin/editcategory.html',context)
        
def deletecategory(request, id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        categorylist = Category.objects.get(id=id)
        if Category.objects.filter(id=id).exists():
            categorylist.delete()
            return redirect("viewcategory")
        else:
            return redirect("viewcategory")
          

# @never_cache
# def add_product(request):
#     if request.session.get('logedin') != True:
#         return redirect('loginadmin')
#     else:
#         if request.method=='POST':
#             forms=ProductForms(request.POST,request.FILES)
#             if forms.is_valid():
#                 forms.save()
#         forms=ProductForms()
#         context={'add_product_form':forms,'heading': 'Create Product'}
#         return render(request,'admin/productadd.html',context)

@never_cache
def view_product(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:        
        product=Product.objects.all()
        return render(request,'admin/productview.html',{'product':product})


# def editproduct(request,id):    
#     if request.session.get('logedin') !=True:
#         return redirect('adminlogin')
#     else:
#         if request.method=='POST':
#             product_view = Product.objects.get(id=id)
#             form = ProductForms(request.POST, instance = product_view)
#             if form.is_valid():
#                 form.save()
#                 return redirect('view_product')
#         else:
#             product_view = Product.objects.get(id=id)
#             form = ProductForms(instance=product_view)
#             context = {'add_product_form': form,
#                        'heading': 'Edit Product'}
#         return render(request,'admin/productadd.html',context)
        
def deleteproduct(request, id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        product_view = Product.objects.get(id=id)
        if Product.objects.filter(id=id).exists():
            product_view.delete()
            return redirect("view_product")
        else:
            return redirect("view_product")
        


def add_product(request):
    if request.session.get('logedin'):

        form = ProductForms()
        print("session cleared-------------------")
        if request.method == 'POST':
            form = ProductForms(request.POST, request.FILES)
            print("POST cleared------------------")

            if form.is_valid():
                print("Form valid-------------------")
                cat = form.cleaned_data['category']
                product_name = form.cleaned_data['product_name']
                price = form.cleaned_data['price']
                stock = form.cleaned_data['stock']
                description = form.cleaned_data['description']
                slug = form.cleaned_data['slug']
                avail = form.cleaned_data['is_available']
                image1 = request.POST['pro_img1']
                image2 = request.POST['pro_img2']
                image3 = request.POST['pro_img3']
                image4 = request.POST['pro_img4']

                format, img1 = image1.split(';base64,')
                ext = format.split('/')[-1]
                img_data1 = ContentFile(base64.b64decode(
                img1), name=product_name + '1.' + ext)

                format, img2 = image2.split(';base64,')
                ext = format.split('/')[-1]
                img_data2 = ContentFile(base64.b64decode(
                img2), name=product_name + '2.' + ext)

                format, img3 = image3.split(';base64,')
                ext = format.split('/')[-1]
                img_data3 = ContentFile(base64.b64decode(
                img3), name=product_name + '3.' + ext)

                format, img4 = image4.split(';base64,')
                ext = format.split('/')[-1]
                img_data4 = ContentFile(base64.b64decode(
                img4), name=product_name + '4.' + ext)

                product = Product(category=cat, product_name=product_name, price=price, stock=stock, description=description,
                slug=slug, is_available=avail, images1=img_data1, images2=img_data2, images3=img_data3, images4=img_data4)
                print("hgfhgfghfgfh")
                product.save()
                messages.info(request,'Product Successfully Added')
            
         
                # form.save()
                
        form = ProductForms()
        context={'add_product_form':form,'heading': 'Create Product'}

        print("page rendering-------------------------")
        return render(request, 'admin/productadd.html', context)
    else:
        return redirect('adminlogin')


def editproduct(request, id):
    if request.session.get('logedin'):

        if request.method == 'POST':
            product_instance = Product.objects.get(id=id)
            form = ProductForms(request.POST, request.FILES,instance=product_instance)
            if form.is_valid():
                cat = form.cleaned_data['category']
                product_name = form.cleaned_data['product_name']
                price = form.cleaned_data['price']
                stock = form.cleaned_data['stock']
                description = form.cleaned_data['description']
                slug = form.cleaned_data['slug']
                avail = form.cleaned_data['is_available']
                
                if request.POST.get('pro_img1'):
                    image1 = request.POST['pro_img1']
                    format, img1 = image1.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data1 = ContentFile(base64.b64decode(img1), name=product_name + '1.' + ext)
                    product_instance.images1 = img_data1
                    
                if request.POST.get('pro_img2'):
                    print("image2")
                    image2 = request.POST['pro_img2']
                    format, img2 = image2.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data2 = ContentFile(base64.b64decode(img2), name=product_name + '2.' + ext)
                    product_instance.images2 = img_data2
                    
                if request.POST.get('pro_img3'):
                    print("image3")
                    image3 = request.POST['pro_img3']
                    format, img3 = image3.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data3 = ContentFile(base64.b64decode(img3), name=product_name + '3.' + ext)
                    product_instance.images3 = img_data3
                    
                if request.POST.get('pro_img4'):
                    print("image4")
                    image4 = request.POST['pro_img4']
                    format, img4 = image4.split(';base64,')
                    ext = format.split('/')[-1]
                    img_data4 = ContentFile(base64.b64decode(img4), name=product_name + '4.' + ext)
                    product_instance.images4 = img_data4

                product_instance.category = cat
                product_instance.product_name = product_name
                product_instance.price = price
                product_instance.stock = stock
                product_instance.description = description
                product_instance.slug = slug
                product_instance.is_available = avail
                product_instance.save()
                messages.info(request,'Product Edited Successfully')
                return redirect('view_product')

        else:
            product_instance = Product.objects.get(id=id)
            form = ProductForms(instance=product_instance)

        context = {'add_product_form': form,
                'heading': 'Edit Product'}
        return render(request, 'admin/productadd.html', context)
    else:
        return redirect('adminlogin')
def admin_logout(request):
    del request.session['logedin']
    return redirect('adminlogin')

@never_cache
def view_order(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:        
        orders=OrderProduct.objects.all().order_by('id') 
        paginator=Paginator(orders,10)
        page=request.GET.get('page')
        paged_orders=paginator.get_page(page)
        forms=OrderStatus()
        
        
        context={
            
            'orders': paged_orders,
            'forms': forms,
            
        }           
        return render(request,'admin/orderview.html',context)
            
def order_status(request, id):    
        orders=OrderProduct.objects.get(id=id) 
        
        if request.method == 'POST':
            forms=OrderStatus(request.POST)
            if forms.is_valid():
                status=forms.cleaned_data.get("status")
                orders.status=status
                if orders.status == 'Cancelled':
                    orders.product.stock = orders.product.stock+orders.quantity
                orders.save()
                orders.product.save()
        return redirect('view_order')
    
@never_cache  
def sales_report(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:  
        deliver=OrderProduct.objects.filter(status='Accepted')
        total=0
        for delive in deliver:
            total+=delive.product_price
       
        context={
            'ordered':deliver,
            'total':total
        }
        # orders = Order.objects.filter(is_ordered=True)
        # context ={
        #     'ordered': orders
        # }      
        return render(request,'admin/admin_report.html',context)
    
    

def monthly_report(request):
    if request.method == 'POST':
        month = request.POST['month']
        x=[]
        x = month.split("-")
        mo=int(x[1])
        deliver=OrderProduct.objects.filter(status='Accepted',created_at__month=mo)
        total=0
        for delive in deliver:
            total+=delive.product_price
        context={
            'ordered':deliver,
            'total':total
        }
        
        return render(request,'admin/admin_report.html',context)
    total_order=OrderProduct.objects.filter(status='Accepted') 
    total=0 
    for delive in total_order:
            total+=delive.product_price
  
    context={
            'ordered':total_order,
             'total':total
        }
         
    return render(request,'admin/admin_report.html',context)  



def yearly_report(request):
    if request.method=='GET':
        year=request.GET['year']
        print(year)
        total_order=OrderProduct.objects.filter(created_at__year=year,status='Accepted')
        total=0
        print(total_order)
        for delive in total_order:
            total+=delive.product_price
        context={
            'ordered':total_order,
             'total':total
        }
        return render(request,'admin/admin_report.html',context)     



def datewise_report(request):
    if request.method=="GET":
        start=request.GET['start']           
        end=request.GET['end']   
        total_order=OrderProduct.objects.filter(created_at__range=[start,end],status='Accepted')
        print(total_order)
        print(start,end) 
        total=0
        for delive in total_order:
            total+=delive.product_price
        context={
            'ordered':total_order,
             'total':total
        }

        return render(request,'admin/admin_report.html',context)     
    


def offer_add(request):
    product=Product.objects.all()
    category=Category.objects.all()
    context={
        'product' : product,
        'category' : category,
    }
    return render(request,'admin/offer_add.html',context)

def offer_category(request):
    if request.method =='POST':
        cat=int(request.POST['category'])
        offer=request.POST['offer']
        start=request.POST['start']
        end=request.POST['end']
        category=Category.objects.get(id=cat)
        if CategoryOffer.objects.filter(category__category_name=category).exists():
            cats=CategoryOffer.objects.get(category=category)
            cats.category=category
            cats.offer=offer
            cats.offer_start=start
            cats.offer_end=end
            cats.save()
        else:
            category1=CategoryOffer(category=category,offer=offer,offer_start=start,offer_end=end)
            category1.save()
        product=Product.objects.filter(category=category.id)
        for pro in product:
            discount=pro.price*(int(offer)/100)
            pro.offer_price=pro.price-discount
            pro.offer_percentage=offer
            pro.save(update_fields=['offer_price','offer_percentage'])
            
        return redirect('offer_view')
    
def offer_product(request):
    if request.method =='POST':
        prod=int(request.POST['product'])
        offer=request.POST['offer']
        start=request.POST['start']
        end=request.POST['end']
        product=Product.objects.get(id=prod)
        
        if ProductOffer.objects.filter(product__id=prod).exists():
            pro=ProductOffer.objects.get(product=prod)
            pro.product=product
            pro.offer=offer
            pro.offer_start=start
            pro.offer_end=end
            pro.save()
        else:
            product=ProductOffer(product=product,offer=offer,offer_start=start,offer_end=end)
            product.save()
        product=Product.objects.get(id=prod)
        discount=product.price*(int(offer)/100)
        product.offer_price=product.price-discount
        product.offer_percentage=offer
        product.save()
        return redirect('offer_view')
    
def offer_view(request):
    product_offer=ProductOffer.objects.all()
    category_offer=CategoryOffer.objects.all()
    context={
        'product_offer':product_offer,
        'category_offer':category_offer,
    }           
    return render(request,'admin/offer_view.html',context)

def delete_category_offer(request,id):
    offer=CategoryOffer.objects.get(id=id)
    pro=Product.objects.filter(category=offer.category)
    for pro in pro:
        pro.offer_price=None
        pro.offer_percentage=None
        pro.save(update_fields=['offer_price','offer_percentage'])
    offer.delete()
    return redirect('offer_view')

def delete_product_offer(request,id):
    offer=ProductOffer.objects.get(id=id)
    pro=Product.objects.filter(product_name=offer.product)
    for pro in pro:
        pro.offer_price=None
        pro.offer_percentage=None
        pro.save(update_fields=['offer_price','offer_percentage'])
    offer.delete()
    return redirect('offer_view')

def coupon_view(request):
    coup=coupon.objects.all()
    context={
        'coup': coup,
    }
    return render(request,'admin/coupon_view.html',context)

def coupon_add(request):
    if request.method=='POST':
        coupon_code=request.POST['coupon_code']
        coupon_rate=request.POST['coupon_rate']
        coupon_start=request.POST['coupon_start']
        coupon_end=request.POST['coupon_end']
        if coupon.objects.filter(coupon_code=coupon_code).exists():
            co=coupon.objects.get(coupon_code=coupon_code)
            co.coupon_code=coupon_code
            co.coupon_rate=coupon_rate
            co.coupon_start=coupon_start
            co.coupon_end=coupon_end
            co.save()
            messages.info(request,"Coupon Updated Successfully")
            return redirect('coupon_view')
        else:
            coup=coupon(coupon_code=coupon_code,coupon_rate=coupon_rate,coupon_start=coupon_start,coupon_end=coupon_end)
            coup.save()
            messages.info(request,"Coupon Added Successfully")
            return redirect('coupon_view')
    return render(request,'admin/coupon_add.html')

def coupon_delete(request,id):
    coup=coupon.objects.get(id=id)
    coup.delete()
    messages.info(request,"Coupon Deleted")
    return redirect('coupon_view')

# def apply_coupon(request):
#     if request.method =='POST':
#         coupon_code=request.POST['coupon_code']
       
#         user=request.user
#         print(coupon_code)
        
#         if coupon.objects.filter(coupon_code=coupon_code).exists():
#             coupon1=coupon.objects.get(coupon_code=coupon_code)
#             if UsedOffer.objects.filter(coupon=coupon1,user=user).exists():
#                 messages.info(request,"Coupon Already Used")
#             else:
#                 used=UsedOffer(user=user,coupon=coupon1)
#                 # used.user=user
#                 # used.coupon=coupon1
#                 used.save()
#                 # user1=coupon_code
#                 request.session[coupon_code]=True 
                    
#         else:
#             messages.info(request,"Invalid Coupon")
#     return redirect('carts')
    
            
            
            
        
        
        
        
        
        
        

def rating(request):
    rating=ReviewRating.objects.all().order_by('id')
    context={
        'rating': rating,
    }
    return render(request,'admin/rating.html',context)

def rating_block(request,id):
    review=ReviewRating.objects.get(id=id)
    review.status=False
    review.save()   
    return redirect('rating')   


def rating_unblock(request,id):
    review=ReviewRating.objects.get(id=id)
    review.status=True
    review.save()   
    return redirect('rating')


    
    
    
        

                
    
    
    

    
    


            





# # Create your views here.
