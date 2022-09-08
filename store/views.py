from django import forms
from django.core import paginator
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import product, Order
from users.models import Account
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def index(request):
    item = product.objects.all().filter(claimed = False).order_by('-date_added')

    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        item = item.filter(name__icontains = item_name) | item.filter(category__icontains = item_name)      

    #paginator code
    paginator = Paginator(item, 8)
    page = request.GET.get('page')
    item = paginator.get_page(page)

    return render(request, 'store/index.html', {'item':item})

def detail(request, id):    
    item = product.objects.get(id=id)
    user = Account.objects.get(id = item.added_by)

    #search code
    items = product.objects.all()
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        items = items.filter(name__icontains = item_name) | items.filter(category__icontains = item_name) 
        return render(request, 'store/index.html', {'item':items}) 

    context = {
        'item':item,
        'user':user 
    }

    return render(request, 'store/detail.html', context)

def allitems(request, cat=None):
        
    item = product.objects.all().filter(claimed = False)
    categories = product.objects.values('category').filter(claimed = False).order_by('category').distinct()
    

    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        item = item.filter(name__icontains = item_name) | item.filter(category__icontains = item_name)      

    if cat is not None:
        item = item.filter(category = cat)

    #paginator code
    paginator = Paginator(item, 9)
    page = request.GET.get('page')
    item = paginator.get_page(page)
    
    context = {
        'item':item,
        'categories':categories,
    }

    return render(request, 'store/all.html', context)


def additem(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            prod = product()
            prod.name = request.POST.get('name')
            prod.description = request.POST.get('description')
            prod.category = request.POST.get('category')

            if len(request.FILES) != 0:
                prod.image = request.FILES['image']

            prod.added_by = request.user.id

            prod.save()
            return redirect('index')
        
        return render(request, 'store/additem.html')
    else:
        return redirect('login')

def checkout(request):
    item = product.objects.all()

    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        item = item.filter(name__icontains = item_name) | item.filter(category__icontains = item_name) 
        return render(request, 'store/index.html', {'item':item}) 

    if request.method == "POST":
        items = request.POST.get('items', "")
        name = request.POST.get('name', "")
        address = request.POST.get('address', "")
        email = request.POST.get('email', "")
        city = request.POST.get('city', "") 
        state = request.POST.get('state', "")
        zip = request.POST.get('zip', "")
        total = request.POST.get('total', "")
        
        order = Order(items=items, name=name, address=address, email=email, city=city, state=state, zip=zip, total=total)
        order.save() 

    return render(request, 'store/checkout.html') 