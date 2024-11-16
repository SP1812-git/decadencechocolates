from django.shortcuts import render,redirect
from chocolate.models import ChocolateTable
# Create your views here.



def view_chocolates(request):
   if request.user.is_authenticated and request.user.is_superuser: 
      data={}
      chocolates=ChocolateTable.objects.all()
   # print(products.count())
      data['chocolates']=chocolates
      
      return render(request,'admin/chocolate/view_chocolate.html',context=data)
   else:
      redirect("/login")

def add_chocolate(request):
   if request.user.is_authenticated and request.user.is_superuser:
      if request.method=='POST':
         name=request.POST.get('name')
         price=request.POST.get('price')
         description=request.POST.get('description')
         quantity=request.POST.get('quantity')
         flavour=request.POST.get('flavour')
         weight=request.POST.get('weight')
         event=request.POST.get('event')
         shape=request.POST.get('shape')
         image = request.FILES.get('image')
         is_available=(request.POST.get('is_available',False)) and ('is_available' in request.POST)
         
         chocolate=ChocolateTable.objects.create(chocolate_name=name,chocolate_price=price,chocolate_description=description,chocolate_quantity=quantity,chocolate_flavour=flavour,chocolate_weight=weight,chocolate_event=event,chocolate_shape=shape,image=image,is_available=is_available)
         
         chocolate.save()
      
         return redirect("/admin/chocolate/view/")
   
      return render(request,'admin/chocolate/add_chocolate.html')
   
   else:
      redirect("/login")

def update_chocolate(request,chocolateid):
   if not request.user.is_superuser:
      return redirect("/login")
   data={}
   chocolate=ChocolateTable.objects.get(chocolate_id=chocolateid)
   data['chocolate']=chocolate   
   if request.method=="POST":
      chocolate.chocolate_name=request.POST.get('name')
      chocolate.chocolate_price=request.POST.get('price')
      chocolate.chocolate_description=request.POST.get('description')
      chocolate.chocolate_quantity=request.POST.get('quantity')
      chocolate.chocolate_flavour=request.POST.get('flavour')
      chocolate.chocolate_weight=request.POST.get('weight')
      chocolate.chocolate_event=request.POST.get('event')
      chocolate.chocolate_shape=request.POST.get('shape')
      chocolate.save()
      if request.FILES['image']:
         chocolate.image = request.FILES.get('image')
         chocolate.is_available=(request.POST.get('is_available',False))and('is_available' in request.POST)   
         chocolate.save()
         return redirect("/admin/chocolate/view/")
      return render(request,'admin/chocolate/update_chocolate.html',context=data)
   else:
      redirect("/login")
   return render(request,'admin/chocolate/update_chocolate.html',context=data)



def delete_chocolate(request,chocolateid):
   if request.user.is_authenticated and request.user.is_superuser:
      chocolate=ChocolateTable.objects.get(chocolate_id=chocolateid)
      chocolate.delete()
      return redirect("/admin/chocolate/view/")
   else:
         redirect("/login")
   

