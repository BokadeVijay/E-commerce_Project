from django.shortcuts import redirect, render
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from seller.models import Product

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.o


def index(request):
    all_pros = Product.objects.all()
    try:
        user_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'user_data': user_obj, "all_pros": all_pros})
    except:
        return render(request, 'index.html', {'all_pros': all_pros})


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            user_obj = Buyer.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'msg': 'Entered Email Is Already Exists!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                global c_otp
                c_otp = random.randint(100_000, 999_999)
                subject = f'OTP VERIFICATION'
                message = f'Use This Code To Verifying Account Safely\n{c_otp}'
                from_mail = settings.EMAIL_HOST_USER
                r_list = [request.POST['email']]

                global user_dict
                user_dict = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'email': request.POST['email'],
                    'password': request.POST['password']


                }

                send_mail(subject, message, from_mail, r_list)
                return render(request, 'otp.html', {'msg': '*Check Your Mail-Box!'})
            else:
                return render(request, 'register.html', {'msg': '*Entered Password Is Not Same'})


def otp(request):
    if int(c_otp) == int(request.POST['u_otp']):
        Buyer.objects.create(
            first_name=user_dict['first_name'],
            last_name=user_dict['last_name'],
            email=user_dict['email'],
            password=user_dict['password']
        )
        return render(request, 'index.html')
    else:
        return render(request, 'otp.html', {'msg': 'OTP Is Not Matched!'})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            user_obj = Buyer.objects.get(email=request.POST['email'])
            if user_obj.password == request.POST['password']:
                request.session['email'] = request.POST['email']
                return render(request, 'index.html', {'user_data': user_obj})
            else:
                return render(request, 'login.html', {'msg': '*Wrong Password!'})
        except:
            return render(request, 'register.html', {'msg': '*Please Register Yourself First!'})


def logout(request):
    del request.session['email']
    return redirect('index')


def edit_profile(request):
    user_obj = Buyer.objects.get(email=request.session['email'])
    if request.method == 'GET':
        return render(request, 'edit_profile.html', {'user_data': user_obj})
    else:
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        # user_obj.email = request.POST['email']
        user_obj.address = request.POST['address']
        user_obj.phone = request.POST['phone']
        user_obj.pic = request.FILES['pic']
        user_obj.save()

        user_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'edit_profile.html', {'user_data': user_obj})


def forget(request):
    if request.method == 'POST':
        user_obj = Buyer.objects.get(email=request.POST['email'])
        subject = f'GETTING PASSWORD'
        message = f'Hello {user_obj.first_name}\nYour Password is {user_obj.password}'
        f_mail = settings.EMAIL_HOST_USER
        r_list = [request.POST['email']]
        send_mail(subject, message, f_mail, r_list)

        return render(request, 'login.html', {'msg': '*check your mail-box'})
    else:
        return render(request, 'forget.html')


def reset(request):
    s_obj = Buyer.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if s_obj.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['re_password']:
                s_obj.password = request.POST['new_password']
                s_obj.save()
                return render(request, 'edit_profile.html', {'msg': 'password changed successfully!', 'user_data': s_obj})
            else:
                return render(request, 'reset.html', {'msg': 'password is not matched', 'user_data': s_obj})
        else:
            return render(request, 'reset.html', {'msg': 'entered Password is wrong', 'user_data': s_obj})
    else:
        return render(request, 'reset.html', {'user_data': s_obj})


def add_to_cart(request, pk):
    try:
        user_obj = Buyer.objects.get(email=request.session['email'])
        pro_obj = Product.objects.get(id=pk)
        Cart.objects.create(

            buyer=user_obj,
            product=pro_obj
        )
        return redirect('index')
    except:
        return render(request, 'login.html')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def cart(request):

    user_obj = Buyer.objects.get(email=request.session['email'])
    global c_list
    c_list = Cart.objects.filter(buyer=user_obj)
    # print(c_list)
    # for i in c_list:
    #     print(i.product.product_name)
    global total
    total = 0 
    for i in c_list:
        total += i.product.price

    currency = 'INR'
    
    if total == 0:
        return render(request,'cart.html',{'user_data': user_obj, 'my_cart_data': c_list, 'total_amount': total})

    amount = total * 100 

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context.update(
        {'user_data': user_obj, 'my_cart_data': c_list, 'total_amount': total})

    return render(request, 'cart.html', context=context)


@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = total * 100  # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    session_user = Buyer.objects.get(email = request.session['email'])
                    c_obj = Cart.objects.filter(buyer = session_user)
                    for i in c_obj:
                        ViewOrders.objects.create(
                            product = i. product,
                            buyer = session_user
                        )


                    for i in c_obj:
                        MyOrder.objects.create(
                            buyer = session_user,
                            product = i.product,
                            status = 'pending'
                        )
                        i.delete()
                   

                    # capture the payemt
                    return redirect('cart')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


def del_cart_data(request, pk):
    c_item = Cart.objects.get(id=pk)
    print(c_item)
    c_item.delete()

    return redirect('cart')


def view_orders(request):
    session_user = Buyer.objects.get(email = request.session['email'])
    view_obj = ViewOrders.objects.all()
    return render(request,'view_orders.html',{'all_order':view_obj,"user_data":session_user})
