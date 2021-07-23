from django.http.response import HttpResponse
from store.utils import generate_ref_code
from category.models import Category
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import RegistrationForms
from .models import Account
from rest_framework.views import APIView
from twilio.rest import Client
import random
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from cart.models import Cart, CartItem
from store.models import Product, Referal, ReferalCoupen, UserPropic
from order.models import OrderProduct, UserAddress
import requests
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg, Count
import base64
from django.core.files.base import ContentFile



def register(re):
  
    if re.method == "POST":        
        first_name=re.POST.get('first_name')
        last_name=re.POST.get('last_name')
        email=re.POST.get('email')
        user_password=re.POST.get('user_password')
        phone_number=re.POST.get('phone_number')
        ref_code=re.POST.get('ref_code')
        username=email.split('@')[0]
        user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=user_password,phone_number=phone_number)
        user.save()
        
        user_code=generate_ref_code()
        
        if Referal.objects.filter(code=ref_code).exists():
            recomm=Referal.objects.get(code=ref_code)
            ref_user=Referal()
            ref_user.user=user
            ref_user.code=user_code
            ref_user.recommended_by=recomm.user
            ref_user.save()
            Ref_Coup=ReferalCoupen()
            Ref_Coup.coupon_code=user_code
            Ref_Coup.user=user
            Ref_Coup.discount=10
            Ref_Coup.save()
            Ref_Coup=ReferalCoupen()
            Ref_Coup.coupon_code=recomm.code
            Ref_Coup.user=recomm.user
            Ref_Coup.discount=10
            Ref_Coup.save()
        else:      
            ref_user=Referal()
            ref_user.user=user
            ref_user.code=user_code
            ref_user.save()
            messages.success(re,"New User Successfully Registered")
            return render(re,'user/register.html')  
                  
        messages.success(re,"New User Successfully Registered")
        return render(re,'user/register.html')
    else:
        return render(re,'user/register.html')
        

def login(re):
    if re.method=="POST":
        email=re.POST.get('email')
        password=re.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(re))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user = user
                        item.save()                
            except:
                pass               
            
            auth.login(re,user)
            messages.success(re,"Successfully Logged in.")
            url=re.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
              
                
            except:
                return redirect('index')
            
        else:
            messages.info(re,"Credentials not correct")
            return redirect('login')
    return render(re,'user/login.html')


@login_required(login_url = 'login')
def logout(re):
    auth.logout(re)
    messages.success(re,"Successfully Logged out")
    return render(re,'user/login.html')


def otp_login(request):
    if request.method=='POST':
        phone=request.POST['phone_number']
        if Account.objects.filter(phone_number=phone).exists():
            otp = random.randint(100000,999999)
            strotp=str(otp)
            account_sid ='ACffc8f9e4b26715c4a91262f4668ff25e'
            auth_token ='5a9fe2e0cf2bad337583862c074f851e'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                     body="Eshop plus login OTP is"+strotp,
                     from_='+18646598904',
                     to='+91'+phone
                 )
            request.session['otp']=otp           
            request.session['phone']=phone 
            messages.success(request,"OTP Sended Successfully")
            return redirect('otp_login')  
        messages.error(request,"enter valid phone number")    
        return redirect('otp_login')      
    
    return render(request,'user/otplogin.html')




def otp_verify(request):
    if request.method=='POST':
        enter_otp=request.POST['otp']
        otp=int(enter_otp)
        if request.session.has_key('otp'):
            sended_otp=request.session['otp']
            
            if sended_otp == otp :
                phone=request.session['phone']
                user=Account.objects.get(phone_number=phone)
                auth.login(request,user)
                del request.session['otp']
                del request.session['phone']
                return redirect('index')
            else:    
                messages.error(request,"entered OTP is wrong")
                return redirect('otp_login') 
        else:
            return redirect('otp_login')          
    return render(request,'user/otplogin.html')

def user_profile_dashboard(request):
    user = request.user.id
    account=Account.objects.get(id=user)
    address = UserAddress.objects.filter(user=user)
    # address_new=address[0]
    order_product=OrderProduct.objects.filter(user=request.user)
    try:
        pro=UserPropic.objects.get(user=request.user)
        propic=pro.pro_pic
    except:
        propic="https://bootdey.com/img/Content/avatar/avatar7.png"
    
    
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    context = {
        'account': account,
        'address': address,
        'order_products': order_product,
        'propic': propic,
    }      
    return render(request,'user/user_profile_dashboard.html',context)


def user_propic(request):
    if request.method=='POST':
        image=request.POST['pro_img1']
        format, img1 = image.split(';base64,')
        ext = format.split('/')[-1]
        img_data1 = ContentFile(base64.b64decode(img1), name="propic" + '1.' + ext)
        if UserPropic.objects.filter(user=request.user).exists():
            propic=UserPropic.objects.get(user=request.user)
            propic.pro_pic=img_data1
            propic.save()
        else:    
            propic=UserPropic(user=request.user,pro_pic=img_data1) 
            propic.save()
        return redirect('user_profile_dashboard')

def user_profile_refer(request):
    user = request.user.id
  
    refer=Referal.objects.get(user=user)
    # reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
    succes_referals=Referal.objects.filter(recommended_by=user).count()
    refer_code=refer.code
    available_coupon=ReferalCoupen.objects.filter(coupon_code=refer_code).count()
    context = {
        'refer_code': refer_code,
        'succes_referals': succes_referals,
        'available_coupon': available_coupon,
        
    }      
    return render(request,'user/user_profile_refer.html',context)

def user_profile_address(request):
    user=request.user
    address=UserAddress.objects.filter(user=user)
    print(address)
    context = {
        'address': address
        }    
    
    return render(request,'user/user_profile_address.html',context)     
       

       
       

        
def user_profile_add_address(request):
    user = request.user
    address =UserAddress()
    if request.method=='POST':
        if UserAddress.objects.filter(user=user.id,first_name=request.POST['first_name'],last_name=request.POST['last_name'],phone=request.POST['phone'],email=request.POST['email'],address_line1=request.POST['address_line1'],address_line2=request.POST['address_line2'],city=request.POST['city'],state=request.POST['state']).exists():
            messages.info(request,"Address Already exist")
           
            
        else:
            address.first_name=request.POST['first_name']
            address.last_name=request.POST['last_name']
            address.phone=request.POST['phone']
            address.email=request.POST['email']
            address.address_line1=request.POST['address_line1']
            address.address_line2=request.POST['address_line2']
            address.city=request.POST['city']
            address.state=request.POST['state']
            address.user=user
            address.save()
            messages.info(request,"Address Added Successfully")
            return redirect('user_profile_address')
            
    return render(request,'user/user_profile_add_address.html') 




def user_profile_edit_address(request,id):
    address =UserAddress.objects.get(id=id)
    user = request.user
    if request.method=='POST':
        if UserAddress.objects.filter(user=user.id,first_name=request.POST['first_name'],last_name=request.POST['last_name'],phone=request.POST['phone'],email=request.POST['email'],address_line1=request.POST['address_line1'],address_line2=request.POST['address_line2'],city=request.POST['city'],state=request.POST['state']).exists():
            messages.info(request,"Address Already exist")
        else:            
            address.first_name=request.POST['first_name']
            address.last_name=request.POST['last_name']
            address.phone=request.POST['phone']
            address.email=request.POST['email']
            address.address_line1=request.POST['address_line1']
            address.address_line2=request.POST['address_line2']
            address.city=request.POST['city']
            address.state=request.POST['state']
            address.save()
            messages.info(request,"Address Added Successfully")
            return redirect('user_profile_address')
    
    context={
        'address':address
    }
            
    return render(request,'user/user_profile_edit_address.html',context)

def user_profile_delete_address(request,id):
    address =UserAddress.objects.get(id=id)
    address.delete()
    messages.info(request,"Address Deleted")
    return redirect('user_profile_address')
    
    

def user_profile_order(request):
    user = request.user.id
    address = UserAddress.objects.filter(user=user)
    address_new=address[0]
    order_product=OrderProduct.objects.filter(user=request.user)
    
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    context = {
        'address': address_new,
        'order_products': order_product,
        
        
    }      
    return render(request,'user/user_profile_order.html',context)

def user_profile_order_details(request,id):    
    order_product=OrderProduct.objects.get(id=id)   
    
    context = {
       
        'order_product': order_product,        
        
    }      
    return render(request,'user/user_profile_order_details.html',context)

def user_cancelled_product(request,id):
    order_product=OrderProduct.objects.get(id=id)  
    order_product.user_cancelled=True
    order_product.status = 'Cancelled'
    order_product.save()
    order_product.product.stock = order_product.quantity+order_product.product.stock
    order_product.product.save()
    
    return redirect('user_profile_order_details',id) 

def forgotpassword(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
   
    # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('user/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')
    return render(request, 'user/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'user/resetPassword.html')


    




    
