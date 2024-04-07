# api/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserLoginView, UserLogoutView
from . import views

urlpatterns = [
    path('', views.simple_response, name='simple_response'),
    path('/', views.simple_response, name='simple_response'),
    path('user/register/', UserRegistrationView.as_view(), name='register'),
    path('user/login/', UserLoginView.as_view(), name='login'),
    path('user/logout/', UserLogoutView.as_view(), name='logout'),
    # Add other API URLs
  
   path('products/', views.ProductList.as_view(), name='product-list'),
   path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
   path('customers/', views.CustomerList.as_view(), name='customer-list'),
   path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
   path('orders/', views.OrderList.as_view(), name='order-list'),
   path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
