from ast import Or
from inspect import signature
from unittest import result
from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
import razorpay

# Create your views here.
from django.http import HttpResponse

# adding payment Gateway
from ecommerce import settings
razorpay_client= razorpay.Client(auth=(settings.razorpay_id,settings.razorpay_account_id))


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() : 
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    if len(allProds) == 0 or len(query) < 4 :
        params={'msg':"Please make sure to enter relevent query"}
    return render(request, 'shop/search.html',params)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        
        try:
            order = Orders.objects.filter(razorpay_order_id=orderId, email=email)
            
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                print(update)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestep})
                    
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')




def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    thank=False
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address1=address1, address2=address2,city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request razorpay to transfer the amount to your account after payment by user
        order_currency= 'INR'
        callback_url='http://127.0.0.1:8000/shop/handlepayment'
        razorpay_order=razorpay_client.order.create(dict(amount=int(amount)*100,currency=order_currency,receipt=str(id),payment_capture='1'))
        print(razorpay_order['id'])
        order = Orders(items_json=items_json, name=name, email=email, address1=address1, address2=address2,city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount,razorpay_order_id=razorpay_order['id'])
        Orders.razorpay_order_id=razorpay_order['id']
        
        order.save()
        update = OrderUpdate(order_id=order.razorpay_order_id)
        update.save()
        thank=True
        
        
        return render(request,'shop/rozarpay.html',{'order':order,'order_id':order.razorpay_order_id,'orderId':id,'amount':amount,'razorpay_marchent_id':settings.razorpay_id,'callback_url':callback_url})
    
        

    return render(request, 'shop/checkout.html',{'thank':thank})
# adding payment Gateway


@csrf_exempt
def handlepayment(request):
    
    if request.method=="POST":
        thank=True
        payment_id = request.POST.get('razorpay_payment_id','')
        order_id = request.POST.get('razorpay_order_id','')
        signature= request.POST.get('razorpay_signature','')
        
        params_dict={
            'razorpay_order_id':order_id,
            'razorpay_payment_id':payment_id,
            'razorpay_signature':signature
            }
        
        try:
            order_db=Orders.objects.get(razorpay_order_id=order_id)
        except:
            return HttpResponse("5050000 Not found")
        
        order_db.razorpay_payment_id=payment_id
        order_db.razorpay_signature=signature
        order_db.save()
        result=razorpay_client.utility.verify_payment_signature(params_dict)
        if result==1:
            order_ub=OrderUpdate.objects.get(order_id=order_id)
            order_ub.update_desc="The order has been placed"
            order_ub.save()
           
               
            
            return render(request,'shop/paymentsuccess.html',{'thank': thank,'dict':params_dict})
        else:
            return render(request,'shop/paymentfailed.html')
    else:
        return HttpResponse("505 not found 000")
            
            
    
