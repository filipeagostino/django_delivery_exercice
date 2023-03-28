from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ShippingForm
from .models import Shipping
from express.models import Deliverer
from customers.models import Customer
from products.models import Product
from django_express.tools.cpf_validator import Cpfvalidator
from django_express.tools.cepvalidator import cepValidator
from django_express.tools.deliverycheck import getInfo
import json
from colorama import Fore, init
init(autoreset=True)


# Is Alive ?

@login_required
def index(request):
    return render(request, 'starter.html')


# READ


@login_required
def readlistshippings(request):
    search = request.GET.get('search')
    if search:
        shippings = Shipping.objects.filter(receiver__icontains=search)
    else:
        shipping_list = Shipping.objects.all().order_by('id')
        paginator = Paginator(shipping_list, 5)
        page = request.GET.get('page')
        shippings = paginator.get_page(page)

    return render(request, 'shipping/list.html', {'shippings': shippings})


# READ SHIPPING BY ID

@login_required
def readshippingId(request, id):
    search = request.GET.get('search')
    if search:
        shippings = Shipping.objects.filter(receiver__icontains=search, customer_id=id)
    else:
        shipping_list = Shipping.objects.all().order_by('customer_id').filter(customer_id=id)
        paginator = Paginator(shipping_list, 5)
        page = request.GET.get('page')
        shippings = paginator.get_page(page)

    return render(request, 'shipping/list.html', {'shippings': shippings})

# READ CUSTOMER ID

@login_required
def readshippingCustomer(request):
    search = request.GET.get('search')
    if search:
        customers = Customer.objects.filter(first_name__icontains=search)
    else:
        customer_list = Customer.objects.all().order_by('first_name')
        paginator = Paginator(customer_list, 5)
        page = request.GET.get('page')
        customers = paginator.get_page(page)

    return render(request, 'shipping/list_shipping_id.html', {'customers': customers})

# VIEW ITEM

@login_required
def ShippingView(request, id):
    item = get_object_or_404(Shipping, pk=id)
    form = ShippingForm(instance=item)
    
    return render(request, 'forms.html', {'form': form, 'Title' : f'Shipping: {item.id}'})


# Necessario ajustes

@login_required
def createShipping(request):

    if request.method == 'POST': 
        print(Fore.YELLOW + 'POST')
        current_user = request.user
        print(Fore.YELLOW + f'CURRENT USER ID: {current_user.id}')
        
        form = ShippingForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = current_user.id
             
            item = form.save()
            messages.info(request, 'Shipping Added!')
            
            return redirect('/shipping/read')                
            
        else:
            return render(request, 'forms.html', {'form': form})

    else:
        form = ShippingForm()
        return render(request, 'forms.html', {'form': form, 'Title': 'New Shipping'})

# Necessario ajustes

@login_required
def editShipping(request, id):
    shipping = get_object_or_404(Shipping, pk=id)
    form = ShippingForm(instance=shipping)

    if(request.method == 'POST'):
        form = ShippingForm(request.POST, instance=shipping)

        if(form.is_valid()):

            shipping.save()
            messages.info(request, 'Shipping Edited!')
            
            return redirect('/shipping/read')

        else:
            return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {shipping.receiver.id}'})

    else:
        return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {shipping.receiver.id}'})


@login_required
def deleteShipping(request, id):
    shipping = get_object_or_404(Shipping, pk=id)
    shipping.delete()
    return redirect('/shipping/read')


@login_required
def test(request, data):
    print(Fore.YELLOW + f'Data received: {data}')
    
    deliverer_zip_code = get_object_or_404(Deliverer, pk=data)
    customer_zip_code = get_object_or_404(Customer, pk=data)
    product_weight = get_object_or_404(Product, pk=data)

    print(Fore.GREEN + f'Deliverer Db zip code: {deliverer_zip_code.zip_code}')
    print(Fore.GREEN + f'Customer Db zip code: {customer_zip_code.zip_code}')
    print(Fore.GREEN + f'Product Db weight: {product_weight.weight}')

    converted_weight = product_weight.weight * 1000

    getinfos = getInfo(deliverer_zip_code.zip_code,
    customer_zip_code.zip_code, converted_weight)

    print(Fore.MAGENTA + f'Informations: {getinfos}')
    
    json_data = json.dumps(getinfos)


    print(Fore.MAGENTA + f'TESTE: {json_data}')

    return HttpResponse(json_data, content_type="application/json")