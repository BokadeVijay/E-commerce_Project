from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.core.mail import send_mail
import random
from django.conf import settings

# Create your views here.

def seller_index(request):
    try:
        seller_obj = Seller.objects.get(email = request.session['s_email'])
        return render(request,'seller_index.html',{'seller_data':seller_obj})
    except:
        return render(request,'signin.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request,'signup.html',{'msg':'*Email Is Already Exists!!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
               global c_otp
               c_otp = random.randint(100000,999999)
               subject = f'Account Creation'
               message = f'Hello {request.POST["user_name"]}\n Your OTP Is {c_otp}'
               fmail = settings.EMAIL_HOST_USER
               r_list = [request.POST['email']]
               send_mail(subject,message,fmail,r_list)

               global seller_dict
               seller_dict = {
                   'user_name':request.POST['user_name'],
                   'email':request.POST['email'],
                   'password':request.POST['password']
               }
               return render(request,'seller_otp.html',{'msg':'Check Your Mail-Box.'})
            else:
                return render(request,'signup.html',{'msg':'*Entered Password Is Not Same'})
            
def seller_otp(request):
    if int(c_otp) == int(request.POST['s_otp']):
        seller_obj = Seller.objects.create(
            user_name = seller_dict['user_name'],
            email = seller_dict['email'],
            password = seller_dict['password']
        )
        return render(request,'seller_index.html',{'seller_data':seller_obj})
    else:
     return render(request,'seller_otp.html')
    

def signin(request):
    if request.method  == 'GET':
        return render(request,'signin.html')
    else:
        try:
            seller_obj = Seller.objects.get(email = request.POST['email'])
            if seller_obj.password == request.POST['password']:
                request.session['s_email'] = request.POST['email']
                return render(request,'seller_index.html',{'seller_data':seller_obj})
            else:
                return render(request,'signin.html',{'msg':'Entered Password is wrong'})
        except:
            return render(request,'signup.html',{'msg':'Register Yourself  first!'})
        
def signout(request):
    del request.session['s_email']
    return redirect('seller_index')


def profile(request):
    seller_obj = Seller.objects.get(email = request.session['s_email'])
    if request.method == 'GET':
        return render(request,'profile.html',{'seller_data':seller_obj})
    else:
        seller_obj.user_name = request.POST['user_name']
        # seller_obj.email = request.POST['email']
        seller_obj.gst = request.POST['gst']
        seller_obj.phone = request.POST['phone']
        # seller_obj.password = request.POST['password']
        seller_obj.pic = request.FILES['pic']
        seller_obj.save()
        return render(request,'profile.html',{'seller_data':seller_obj,'msg':'Data Upadated Successfully!!!'})
    
def add_products(request):
    seller_obj = Seller.objects.get(email = request.session['s_email'])
    if request.method =='GET':
        return render(request,'add_products.html',{'seller_data':seller_obj})
    else:
        Product.objects.create(
                product_name = request.POST['product_name'],
                des = request.POST['des'],
                price = request.POST['price'],
                product_stock = request.POST['product_stock'],
                pic = request.FILES['pic'],
                seller = seller_obj
        )
    return render(request,'add_products.html',{'seller_data':seller_obj})

def my_products(request):
    seller_obj = Seller.objects.get(email = request.session['s_email'])
    product_obj = Product.objects.filter(seller = seller_obj)
    return render(request,'my_products.html',{'seller_data':seller_obj,'my_all_products':product_obj})



def edit_products(request,pk):
    p_obj = Product.objects.get(id = pk)
    if request.method == 'GET':
        seller_obj = Seller.objects.get(email = request.session['s_email'])
        return render(request,'edit_products.html',{'seller_data':seller_obj,'product_data':p_obj})
    else:
        p_obj.product_name  = request.POST['product_name']
        p_obj.price = request.POST['price']
        p_obj.des = request.POST['des']
        p_obj.product_stock = request.POST['product_stock']
        p_obj.pic = request.FILES['pic']
        p_obj.save()
        return redirect('my_products')

    
def delete_products(request,pk):
    pro_obj = Product.objects.get(id = pk)
    pro_obj.delete()
    return redirect('my_products') 


        
            

