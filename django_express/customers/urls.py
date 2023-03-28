from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.readlistCustomers, name='listCustomers'),
    path('create/', views.createCustomer, name='createlistCustomer'),
    path('item/<int:id>', views.CustomerView, name='viewlistCustomer'),
    path('update/<int:id>', views.editlistCustomer, name='editlistCustomer'),
    path('delete/<int:id>', views.deletelistCustomer, name='deletelistCustomer'),
    path('products/', views.listcustomerProducts, name='listcustomerProducts'),
]