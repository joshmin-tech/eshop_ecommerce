from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from .forms import *
from django.contrib import messages
from store.models import Product
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache

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
        return render(request,'admin/base_template.html')

@never_cache
def userview(request):
    if request.session.get('logedin') != True:
        return redirect('adminlogin')
    else:
        userdetails=Account.objects.all()
        return render(request,'admin/adminuserview.html',{'userdata':userdetails})

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
          

@never_cache
def add_product(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        if request.method=='POST':
            forms=ProductForms(request.POST,request.FILES)
            if forms.is_valid():
                forms.save()
        forms=ProductForms()
        context={'add_product_form':forms,'heading': 'Create Product'}
        return render(request,'admin/productadd.html',context)

@never_cache
def view_product(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:        
        product=Product.objects.all()
        return render(request,'admin/productview.html',{'product':product})


def editproduct(request,id):    
    if request.session.get('logedin') !=True:
        return redirect('adminlogin')
    else:
        if request.method=='POST':
            print("hello")
            product_view = Product.objects.get(id=id)
            form = ProductForms(request.POST, instance = product_view)
            if form.is_valid():
                print("inside if")
                form.save()
                return redirect('view_product')
        else:
            product_view = Product.objects.get(id=id)
            form = ProductForms(instance=product_view)
            context = {'add_product_form': form,
                       'heading': 'Edit Product'}
        return render(request,'admin/productadd.html',context)
        
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
            





# # Create your views here.
