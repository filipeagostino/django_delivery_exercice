from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.readlistshippings, name='listshippings'),
    path('create/', views.createShipping, name='createShipping'),
    path('item/<int:id>', views.ShippingView, name='viewPShipping'),
    path('update/<int:id>', views.editShipping, name='editShipping'),
    path('delete/<int:id>', views.deleteShipping, name='deleteShipping'),
    path('read/customer', views.readshippingCustomer, name='readshippingCustomer'),
    path('read/<int:id>', views.readshippingId, name='readshippingId'),
    path('djangowebservice/<data>', views.test, name='test'),
]