from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from django_express.tools.cpf_validator import Cpfvalidator
from django_express.tools.cepvalidator import cepValidator
from colorama import Fore, init
init(autoreset=True)


# Is Alive ?

def index(request):
    return render(request, 'starter.html')

# READ


@login_required
def readlistProducts(request):
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(name__icontains=search)
    else:
        product_list = Product.objects.all().order_by('name')
        paginator = Paginator(product_list, 5)
        page = request.GET.get('page')
        products = paginator.get_page(page)

    return render(request, 'products/list.html', {'products': products})

# VIEW ITEM


@login_required
def ProductView(request, id):
    item = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=item)
    
    return render(request, 'forms.html', {'form': form, 'Title' : f'Product: {item.name}'})


# CREATE


@login_required
def createProduct(request):

    if request.method == 'POST': 
        print(Fore.YELLOW + 'POST')
        current_user = request.user
        print(Fore.YELLOW + f'CURRENT USER ID: {current_user.id}')
        
        form = ProductForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = current_user.id
             
            item = form.save()
            messages.info(request, 'Product Added!')
            
            return redirect('/product/read')                
            
        else:
            return render(request, 'forms.html', {'form': form})

    else:
        form = ProductForm()
        return render(request, 'forms.html', {'form': form, 'Title': 'New Product'})


# UPDATE


@login_required
def editProduct(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=product)

    if(request.method == 'POST'):
        form = ProductForm(request.POST, instance=product)

        if(form.is_valid()):

            product.save()
            messages.info(request, 'Product Edited!')
            
            return redirect('/product/read')

        else:
            return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {product.name}'})

    else:
        return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {product.name}'})

# DELETE


@login_required
def deleteProduct(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('/product/read')