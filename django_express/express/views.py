from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DelivererForm
from .models import Deliverer
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
def readDeliverers(request):
    search = request.GET.get('search')
    if search:
        deliverers = Deliverer.objects.filter(first_name__icontains=search)
    else:
        deliverer_list = Deliverer.objects.all().order_by('first_name')
        paginator = Paginator(deliverer_list, 5)
        page = request.GET.get('page')
        deliverers = paginator.get_page(page)

    return render(request, 'express/list.html', {'deliverers': deliverers})

# VIEW ITEM


@login_required
def DelivererView(request, id):
    item = get_object_or_404(Deliverer, pk=id)
    form = DelivererForm(instance=item)
    
    return render(request, 'forms.html', {'form': form, 'Title' : f'Deliverer: {item.first_name}'})

# CREATE


@login_required
def createDeliverer(request):

    if request.method == 'POST': 
        print(Fore.YELLOW + 'POST')
        current_user = request.user
        print(Fore.YELLOW + f'REQUEST CPF: {request.POST["cpf"]}')
        print(Fore.YELLOW + f'CURRENT USER ID: {current_user.id}')
        
        form = DelivererForm(request.POST)

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
                    return render(request, 'forms.html', {'form': form, 'Title': 'New Deliverer'})

                else:
                    item = form.save()
                    messages.info(request, 'Deliverer Added!')
                    return redirect('/deliverer/read')                
                
            else:
                return render(request, 'forms.html', {'form': form})
    else:
        form = DelivererForm()
        return render(request, 'forms.html', {'form': form, 'Title': 'New Deliverer'})


# UPDATE


@login_required
def editDeliverer(request, id):
    deliverer = get_object_or_404(Deliverer, pk=id)
    form = DelivererForm(instance=deliverer)

    if(request.method == 'POST'):
        form = DelivererForm(request.POST, instance=deliverer)

        if(form.is_valid()):

            check_cpf = Cpfvalidator(request.POST["cpf"])
            cpfvalidation = check_cpf.test()
            print(Fore.CYAN + f'cpf validation: {cpfvalidation}')

            if cpfvalidation == False:
                messages.error(request, 'Invalid Cpf!')
                return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {deliverer.first_name}'})
            
            check_cep, zip_code_info = cepValidator(request.POST["zip_code"])
            
            if check_cep == False:
                messages.error(request, 'Invalid Cep!')
                return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {deliverer.first_name}'})

            else:
                deliverer.save()
                messages.info(request, 'Deliverer Edited!')
                return redirect('/deliverer/read')

            return redirect('/deliverer/read')

        else:
            return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {deliverer.first_name}'})

    else:
        return render(request, 'forms.html', {'form': form, 'Title' : f'Edit: {deliverer.first_name}'})


# DELETE


@login_required
def deleteDeliverer(request, id):
    deliverer = get_object_or_404(Deliverer, pk=id)
    deliverer.delete()
    return redirect('/deliverer/read')
