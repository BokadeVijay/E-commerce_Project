from django.urls import path
from .views import *



urlpatterns = [

    path('',index,name = 'index'),
    path('about/',about,name = 'about'),
    path('register/',register,name = 'register'),
    path('login/',login,name = 'login'),
    path('otp/',otp,name = 'otp'),
    path('logout/',logout,name = 'logout'),
    path('edit_profile/',edit_profile,name = 'edit_profile'),
    path('forget/',forget,name = 'forget'),
    path('reset/',reset,name = 'reset'),
    path('add_to_cart/<int:pk>',add_to_cart,name = 'add_to_cart'),
    path('cart/',cart,name = 'cart'),
    path('del_cart_data/<int:pk>',del_cart_data,name = 'del_cart_data'),
    path('cart/paymenthandler/',paymenthandler,name = 'paymenthandler'),
    path('view_orders/',view_orders,name = 'view_orders')











    

]