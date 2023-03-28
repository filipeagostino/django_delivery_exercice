from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerForm
from .models import Customer
from products.forms import ProductForm
from products.models import Product
from django_express.tools.cpf_validator import Cpfvalidator
from django_express.tools.cepvalidator import cepValidator
from colorama import Fore, init
init(autoreset=True)


# Is Alive ?

@login_required
def index(request):
    return render(request, 'starter.html')


# READ

@login_required
def readlistCustomers(request):
    search = request.GET.get('search')
    if search:
        customers = Customer.objects.filter(first_name__icontains=search)
    else:
        customer_list = Customer.objects.all().order_by('first_name')
        paginator = Paginator(customer_list, 5)
        page = request.GET.get('page')
        customers = paginator.get_page(page)

    return render(request, 'customers/list.html', {'customers': customers})


@login_required
def listcustomerProducts(request):
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(name__icontains=search, user=request.user)
    else:
        product_list = Product.objects.all().order_by('name').filter(user=request.user)
        paginator = Paginator(product_list, 5)
        page = request.GET.get('page')
        products = paginator.get_page(page)

    return render(request, 'products/list.html', {'products': products})


# READ CUSTOMER

@login_required
def CustomerView(request, id):
    customer = get_object_or_404(Customer, pk=id)
    form = CustomerForm(instance=customer)
    
    return render(request, 'forms.html', {'form': form, 'Title' : f'Customer: {customer.first_name}'})

# CREATE

@login_required
def createCustomer(request):

    if request.method == 'POST': 
        print(Fore.YELLOW + 'POST')
        current_user = request.user
        print(Fore.YELLOW + f'REQUEST CPF: {request.POST["cpf"]}')
        print(Fore.YELLOW + f'CURRENT USER ID: {current_user.id}')
        
        form = CustomerForm(request.POST)

        check_cpf_numbers = Cpfvalidator(request.POST['cpf'])
        valitadion_cpf_numbers = check_cpf_numbers.verifynumbers()
        print(Fore.CYAN + f'NUMBERS: {valitadion_cpf_numbers}')

        if valitadion_cpf_numbers == False:
            messages.error(request, 'Cpf must have only numbers!')
            return render(request, 'forms.html', {'form': form, 'first_name': 'New Item'})

        else:      

            if form.is_valid():
                item = form.save(commit=False)
                item.user_id = current_user.id
                
                check_cpf = Cpfvalidator(request.POST["cpf"])
                cpfvalidation = check_cpf.test()
                print(Fore.CYAN + f'cpf validation: {cpfvalidation}')

                if cpfvalidation == False:
                    messages.error(request, 'Invalid Cpf!')
                    return render(request, 'forms.html', {'form': form, 'Title': 'New Deliverer'})
                
                check_cep, zip_code_info = cepValidator(request.POST["zip_code"])
                
                if check_cep == False:
                    messages.error(request, 'Invalid Cep!')
                    return render(request, 'forms.html', {'form': form, 'Title': 'New Customer'})

                else:
                    item.address = zip_code_info['address']
                    item.city = zip_code_info['city']
                    item.district = zip_code_info['district']
                    
                    item = form.save()
                    messages.info(request, 'Customer Added!')
                    return redirect('/customer/read')                
                
            else:
                return render(request, 'forms.html', {'form': form})
    else:
        form = CustomerForm()
        return render(request, 'forms.html', {'form' : form,'Title': 'New Customer'})

# UPDATE

@login_required
def editlistCustomer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    form = CustomerForm(instance=customer)

    if(request.method == 'POST'):
        form = CustomerForm(request.POST, instance=customer)

        if(form.is_valid()):

            check_cpf = Cpfvalidator(request.POST["cpf"])
            cpfvalidation = check_cpf.test()
            print(Fore.CYAN + f'cpf validation: {cpfvalidation}')

            if cpfvalidation == False:
                messages.error(request, 'Invalid Cpf!')
                return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {customer.first_name}'})
            
            check_cep, zip_code_info = cepValidator(request.POST["zip_code"])
            
            if check_cep == False:
                messages.error(request, 'Invalid Cep!')
                return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {customer.first_name}'})

            else:
                customer.address = zip_code_info['address']
                customer.city = zip_code_info['city']
                customer.district = zip_code_info['district']
                customer.save()
                messages.info(request, 'Customer Edited!')
                return redirect('/customer/read')

            return redirect('/customer/read')

        else:
            return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {customer.first_name}'})

    else:
        return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {customer.first_name}'})


# DELETE

@login_required
def deletelistCustomer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    customer.delete()
    return redirect('/customer/read')