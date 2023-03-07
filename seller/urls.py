from django.urls import path
from .views import *

urlpatterns = [

    path('',seller_index,name = 'seller_index'),
    path('signup/',signup,name = 'signup'),
    path('seller_otp/',seller_otp,name = 'seller_otp'),
    path('signin/',signin,name = 'signin'),
    path('signout/',signout,name = 'signout'),
    path('profile/',profile,name = 'profile'),
    path('add_products/',add_products,name = 'add_products'),
    path('my_products/',my_products,name = 'my_products'),
    path('edit_products/<int:pk>',edit_products,name = 'edit_products'),
    path('delete_products/<int:pk>',delete_products,name = 'delete_products'),
    path('my_order/',my_order,name='my_order'),
    path('change_status/<int:pk>',change_status,name='change_status')









]