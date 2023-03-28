from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.readlistProducts, name='listProducts'),
    path('create/', views.createProduct, name='createProduct'),
    path('item/<int:id>', views.ProductView, name='viewProduct'),
    path('update/<int:id>', views.editProduct, name='editProduct'),
    path('delete/<int:id>', views.deleteProduct, name='deleteProduct'),
]