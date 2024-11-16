from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from chocolate.models import ChocolateTable,CartTable
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
# def home(request):   
#    return render(request,'base.html')



def user_login(request):
   data ={}
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/admin")
      else:
         return redirect("/")           
      
   if request.method=="POST":
      uname=request.POST['username']
      upass=request.POST['password']
      
      if (uname=="" or upass==""):
         data['error_msg']="Fields cant be empty"
      elif(not User.objects.filter(username=uname).exists()):
         data['error_msg']=uname + " user does not exist"
      else:
         user=authenticate(username=uname,password=upass)
         if user is None:
            data['error_msg']="Wrong Password"
         else:
            login(request,user)
            if user.is_superuser:
               return redirect("/admin")
            else:
               return redirect("/")
   return render(request,'user/login.html',context=data)

def user_signup(request):
   data ={}
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/admin")
      else:
         return redirect("/")
   if request.method=="POST":
      username=request.POST['username']
      password=request.POST['password']
      password2=request.POST['password2']
      
      if (username=="" or password=="" or password2==""):
         data['error_msg']="Fields cant be empty"
      elif(password!=password2):
         data['error_msg']="Password does not matched"
      elif(User.objects.filter(username=username).exists()):
         data['error_msg']=username + " already exist"
      else:
         user=User.objects.create(username=username)
         user.set_password(password)
         user.save()
         return redirect("/login")
   return render(request,'user/signup.html',context=data)


def user_logout(request):
   logout(request)
   return redirect('/')

def admin_panel(request):
   if request.user.is_authenticated and request.user.is_superuser:
      return render(request,'admin/admin.html')
   else:  
      return redirect("/")

      


   
# ----------------------- all logics ---------------------------------

def home(request):
   
   return render(request,'base.html')


chocolates=ChocolateTable.objects.none()

def variety(request):
      if request.user.is_authenticated:
         data={}
         global chocolates
         global filtered_chocolates
         chocolates=ChocolateTable.objects.filter(is_available=True)
         filtered_chocolates=chocolates
         data['chocolates']=chocolates
         #getting cart count specific to logged in user
         user_id = request.user.id
         cart=CartTable.objects.filter(user_id=user_id)
         print(cart.count())
         data['cartvalue']=cart.count()
         cart_count=find_cart_value(request)
         data['cartvalue']=cart_count

         return render(request,'home/variety.html',context=data)
      else:
         return redirect('/login')
   

def forgot_password(request):
   if request.user.is_authenticated:
      if request.method == "POST":
         uname = request.POST['username']
         if User.objects.filter(username=uname).exists():
            user = User.objects.get(username=uname)
            url = "forgotpassword/update/" + user.username
            global otp
            otp = random.randint(1111,9999)
            send_mail(
   #          "OTP for Password Change - Decadence Chocolate",
   # "OTP is " + str(otp),
   # settings.EMAIL_HOST_USER,
   # [user.email],
   # fail_silently=True,   
  
         'OTP for Password Change - Decadence Chocolate',
         'OTP is ' + str(otp),
         settings.EMAIL_HOST_USER,
         ['pppshivbaba@gmail.com'],
         #  ['shr.paw.rt19@rait.ac.in'],
         fail_silently=False,
      )
         
         return redirect(url)
      return render(request,"user/forgotpassword.html")
   else:
      return redirect('/login')
   
def passotp(request,uname):
   if request.user.is_authenticated:
      user = User.objects.get(username=uname)
      data = {}
      if request.method == "POST":
         uotp = request.POST['otp'] 
         uotp = int(uotp)
         password = request.POST['password']
         confpass = request.POST['confpass']
         global otp
         if uotp != otp :
            print(uotp,type(uotp),otp,type(otp))
            data['error'] = "OTP does not match"
         elif password != confpass :
            data['error'] = "Password do not match" 
         elif uotp == otp and password == confpass:
            user.set_password(password)
            user.save()
            otp = None
            return redirect("/login")
      return render(request,"user/otppassword.html",context=data)
   else:
      return redirect('/login')


          

def filter_by_flavour(request,flavour_value):
   if request.user.is_authenticated:
      data={}
      q1 = Q(is_available=True)
      q2 = Q(chocolate_flavour=flavour_value)
      global chocolates
      global filtered_chocolates
      filtered_chocolates=chocolates.filter(q1 & q2)
      data['chocolates']=filtered_chocolates
      return render(request,'home/variety.html',context=data)
   else:
      return redirect('/login')


def filter_by_weight(request,weight_value):
   if request.user.is_authenticated:
      data={}
      q1 = Q(is_available=True)
      q2 = Q(chocolate_weight=weight_value)
      global chocolates
      global filtered_chocolates
      filtered_chocolates=chocolates.filter(q1 & q2)
      data['chocolates']=filtered_chocolates
      return render(request,'home/variety.html',context=data)
   else:
      return redirect('/login')

def filter_by_event(request,event_value):
   if request.user.is_authenticated:
      data={}
      q1 = Q(is_available=True)
      q2 = Q(chocolate_event=event_value)
      global chocolates
      global filtered_chocolates
      filtered_chocolates=chocolates.filter(q1 & q2)
      data['chocolates']=filtered_chocolates
      return render(request,'home/variety.html',context=data)
   else:
      return redirect('/login')

def filter_by_shape(request,shape_value):
   if request.user.is_authenticated:
      data={}
      q1 = Q(is_available=True)
      q2 = Q(chocolate_shape=shape_value)
      global chocolates
      global filtered_chocolates
      filtered_chocolates=chocolates.filter(q1 & q2)
      data['chocolates']=filtered_chocolates
      return render(request,'home/variety.html',context=data)
   else:
      return redirect('/login')


def sort_by_price(request,sort_value):
   if request.user.is_authenticated:
      data={}
      global filtered_chocolates
      #select * from product where is_available=True order by price desc
      if(sort_value=='asc'):
         sorted_chocolates=filtered_chocolates.filter(is_available=True).order_by('chocolate_price')
      else:
         sorted_chocolates=filtered_chocolates.filter(is_available=True).order_by('-chocolate_price')
      data['chocolates']=sorted_chocolates
      return render(request,'home/variety.html',context=data)
   else:
      return redirect('/login')
   

def search_by_price_range(request):
   if request.user.is_authenticated: 
      print("in search")
      # data={}
      min=request.POST['min']
      max=request.POST['max']
      q1 = Q(is_available=True)
      q2 = Q(chocolate_price__gte=min)
      q3 = Q(chocolate_price__lte=max)
      searched_chocolates = filtered_chocolates.filter(q1 & q2 & q3)
      context = {
         'chocolates' : searched_chocolates
      }
      return render(request,'home/variety.html',context)
   else:
      return redirect('/login')
  

def add_to_cart(request,chocolate_id):
   if request.user.is_authenticated:
      user=request.user
      chocolate=ChocolateTable.objects.get(chocolate_id=chocolate_id)
      q1=Q(user_id=request.user.id)
      q2=Q(chocolate_id=chocolate_id)
      cart_value=CartTable.objects.filter(q1 & q2)
      if(cart_value.count()>0):
         messages.error(request, "Chocolate is already in the bag")
      else:
         cart = CartTable.objects.create(user_id=user,chocolate_id=chocolate,quantity=1)
         cart.save()
         messages.success(request,"Chocolate is added to the bag")
      return redirect('/variety')
   else:
      return redirect('/login')
   
def find_cart_value(request):
   if request.user.is_authenticated:
      user_id = request.user.id
      cart=CartTable.objects.filter(user_id=user_id)
      cart_count=cart.count()
      return cart_count 
   else:
      return redirect('/login')

def show_cart(request):
   if request.user.is_authenticated:
      data1={}
      total_items=0
      total_price=0
      cart_count=find_cart_value(request)
      data1['cartvalue']=cart_count
      chocolates_in_cart=CartTable.objects.filter(user_id=request.user.id)
      data1['cartchocolates']=chocolates_in_cart
      for chocolate in chocolates_in_cart:
         total_items+=chocolate.quantity
         total_price+=(chocolate.chocolate_id.chocolate_price*chocolate.quantity)
      data1['total_items']=total_items
      data1['total_price']=total_price
      if total_price>1 :
        client = razorpay.Client(auth=("rzp_test_97GJ2rvcYmtUV6", "N0lPf0ifPlzeBdQRyueMNDOJ"))
        data = { "amount": int((total_price)*100), "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
      return render(request,'home/show_cart.html',context=data1)
      
   else:
      return redirect('/login')

def delete_cart(request,cart_id):
   if request.user.is_authenticated:
      cart=CartTable.objects.get(id=cart_id)
      cart.delete()
      return redirect("/cart")
   else:
      return redirect('/login')

def update_cart_quantity(request,flag,cart_id):
   if request.user.is_authenticated:
      cart=CartTable.objects.filter(id=cart_id)
      actual_qunatity=cart[0].quantity
      if flag=='inc':
         cart.update(quantity=actual_qunatity+1)
      else:
         if(cart[0].quantity==1):
            pass
         else:
            cart.update(quantity=actual_qunatity-1)
      return redirect("/cart")
   else:
      return redirect('/login')

def show_order(request):
   if request.user.is_authenticated:
      data={}
      total_items=0
      total_price=0
      cart_count=find_cart_value(request)
      data['cartvalue']=cart_count
      chocolates_in_cart=CartTable.objects.filter(user_id=request.user.id)
      data['cartchocolates']=chocolates_in_cart
      for chocolate in chocolates_in_cart:
         total_items+=chocolate.quantity
         total_price+=(chocolate.chocolate_id.chocolate_price*chocolate.quantity)
      data['total_items']=total_items
      data['total_price']=total_price
      return render(request,'home/show_order.html',context=data)
   else:
      return redirect('/login')




def search(request):
    
    query = request.GET.get('q')
    results = []
    if query:
        results = ChocolateTable.objects.filter(title__icontains=query)  # Modify according to your model fields
    return render(request, 'search_results.html', {'results': results, 'query': query})




import razorpay

def make_payment(request):
   if request.user.is_authenticated:
      total_price=0
      chocolates_in_cart=CartTable.objects.filter(user_id=request.user.id)
      for chocolate in chocolates_in_cart:
         total_price+=(chocolate.chocolate_id.chocolate_price*chocolate.quantity)
         
      client = razorpay.Client(auth=("rzp_test_vpBEZ88VkNDmkU", "0rH7iKnJFHclCNXdZXFFYeeg"))
      data = { "amount": total_price*100, "currency": "INR", "receipt": "order_rcptid_11" }
      payment = client.order.create(data=data)
      print(payment)
      return render(request,'home/pay.html',context=data)
   else:
      return redirect('/login')