from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
import json
# Create your views here.
def index(request):
    # Fetch All Products
    products = Product.objects.all()

    #Fetch all Products in which Category is Apple
    apple_category = Product.objects.filter(category = 'Apple')

    params = {'product': products,'apple_category':apple_category}
    return render(request, 'shop/index.html', params)
    #return HttpResponse('This is the Shop Page')
    
def about(request):
    return render(request, 'shop/about.html')


def productView(request, myid):
    product = Product.objects.filter(id = myid)
    params = { 'product':product[0] }
    return render(request, 'shop/prodView.html', params)

def contactUs(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone,desc=desc)
        contact.save()
        print(name,email,phone,desc)
    return render(request, 'shop/contact.html')


def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('item_json', '')
        name = request.POST.get('name', '')
        email =request.POST.get('email', '')
        address =request.POST.get('address', '') +" "+ request.POST.get('address2', '')
        city =request.POST.get('city', '')
        state =request.POST.get('state', '')
        zip_code =request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(item_json=item_json, name=name, email=email, address=address, city=city, state=state, 
                zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank, 'id':id})
    return render(request,'shop/checkout.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')
        