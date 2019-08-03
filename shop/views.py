from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,orderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    # allprods = [
    #     [products,range(1,nSlides),nSlides],
    #     [products,range(1,nSlides),nSlides],
    # ]
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nSlides),nSlides])

    params = {'allprods':allprods}
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        print(n)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if n != 0:
            allprods.append([prod,range(1,nSlides),nSlides])
                
    params = {'allprods':allprods}
    if len(allprods)==0:
        return render(request,'shop/error.html')
    return render(request,'shop/index.html',params)

def about(request):
    return render(request,'shop/about.html')


def contact(request):
    
    if request.method == 'POST':
        if request.POST['email'] and request.POST['name'] and request.POST['message'] and request.POST['phone']:
            contact = Contact()
            contact.name = request.POST['name']
            contact.email =request.POST['email']
            contact.phone = request.POST['phone']
            contact.message = request.POST['message']
            contact.save()
            # print(name,email,phone,mssg)
            msg='we will get back to you soon.'
            return render(request,'shop/contact.html',{'mssg':msg})
        else:
            msg='please fill all the required fields.'
            return render(request,'shop/contact.html',{'mssg':msg})
    else:
        return render(request,'shop/contact.html')

def tracker(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['name']:
            name = request.POST.get('name','')
            email = request.POST.get('email','')
            try:
                oder = Order.objects.filter(name= name,email = email).all()
                # print(oder[0].items_json)
                if oder:
                    item = json.loads(oder[0].items_json)
                    #print(item)
                    # odr = []
                    # for i in item.values():
                        
                    
                    upd = orderUpdate.objects.filter(update_name=name)
                    
                    return render(request,'shop/tracker.html',{'info':upd,'odr':item.values()})
                else:
                    err = "Please enter correct details"
                    return render(request,'shop/tracker.html',{'err':err})
            except Exception as e:
                return HttpResponse(f'{e}')
        else:
            mssg = "please fill all required fields."
            return render(request,'shop/tracker.html',{'mssg':mssg})
    else:          
        return render(request,'shop/tracker.html')



def productview(request,id):
    prod = {}
    prod = Product.objects.get(id = id)
    # print(prod.desc)
    cat = prod.subcategory
    similar = Product.objects.filter(subcategory = cat)
    # print(similar.all())
    # mylist ={} 
    return render(request,'shop/prodview.html',{'prod':prod, 'similar':similar.all()})

def checkout(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['name'] and request.POST['city'] and request.POST['phone']:
            oder = Order()
            oder.name = request.POST['name']
            oder.email =request.POST['email']
            oder.phone = request.POST['phone']
            oder.address = request.POST['address1'] + "," + request.POST['address2'] + "," + request.POST['city'] + "," + request.POST['state'] + "," + request.POST['zip']
            oder.items_json = request.POST['itemsJson']
            oder.amount =request.POST['amount']
            # print(oder.name,oder.phone,oder.email,oder.address,oder.items_json)
            
            update = orderUpdate()
            update.update_desc = "the order is placed successfully"
            update.update_name = oder.name
            print(update.update_name,update.update_desc)
            oder.save()
            update.save()
            thank = True
            mssg=""
            return render(request,'shop/checkout.html',{'thank':thank})
        else:
            mssg = "Please Fill all the required Feilds"
            return render(request,'shop/checkout.html',{'mssg':mssg})
    else:
        return render(request,'shop/checkout.html')
