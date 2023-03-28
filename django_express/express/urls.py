from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deliverer/read', views.readDeliverers, name='listDeliverers'),
    path('deliverer/create/', views.createDeliverer, name='createDeliverer'),
    path('deliverer/item/<int:id>', views.DelivererView, name='viewDeliverer'),
    path('deliverer/update/<int:id>', views.editDeliverer, name='editDeliverer'),
    path('deliverer/delete/<int:id>', views.deleteDeliverer, name='deleteDeliverer'),
]