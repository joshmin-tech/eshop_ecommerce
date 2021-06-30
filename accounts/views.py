from django.contrib import messages,auth
from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import RegistrationForms
from .models import Account
from rest_framework.views import APIView
from twilio.rest import Client
import random



def register(re):
    if re.method=='POST':
        # form=RegistrationForms(re.POST)
        # if form.is_valid():
        # first_name=form.cleaned_data['first_name']
        # last_name = form.cleaned_data['last_name']
        # phone_number = form.cleaned_data['phone_number']
        # email= form.cleaned_data['email']
        # password= form.cleaned_data['password']

        # username=email.split('@')[0]
        # user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        # user.phone_number=phone_number
        # user.save()
        # messages.success(re,'registration success')
        # return redirect('index')
        
        first_name=re.POST.get('first_name')
        last_name=re.POST.get('last_name')
        email=re.POST.get('email')
        user_password=re.POST.get('user_password')
        phone_number=re.POST.get('phone_number')
        username=email.split('@')[0]
        
        
        
        user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=user_password,phone_number=phone_number)
        user.save()
        messages.success(re,"New User Successfully Registered")
        return render(re,'user/register.html')
        
    else:
        # form = RegistrationForms()
        # context={
        # 'form':form,
        #     }
        return render(re,'user/register.html')

def login(re):
    if re.method=="POST":
        email=re.POST.get('email')
        password=re.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(re,user)
            return redirect('index')
        else:
            messages.info(re,"Credentials not correct")
            return redirect('login')
    return render(re,'user/login.html')

def logout(re):
    return render(re,'user/login.html')

def otp_login(request):
    if request.method=='POST':
        phone=request.POST['phone_number']
        if Account.objects.filter(phone_number=phone).exists():
            otp = random.randint(100000,999999)
            strotp=str(otp)
            account_sid ='ACffc8f9e4b26715c4a91262f4668ff25e'
            auth_token ='b2a44034dd470aba26331aafe6899633'
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
