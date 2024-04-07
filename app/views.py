
# views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer


from django.http import HttpResponse

def simple_response(request):
    message = "Hello, User its a Backend Side PLease use a valid url <hr>1. baseUrl/api/user/register/ <br>2. baseUrl/api/user/login/ <br>3. baseUrl/api/user/logout/ <br>4. baseurl/api/product   etc. <hr> GitHub Link:- https://github.com/neerajpandit/Spacey_Assignment"  # Your message here
    return HttpResponse(message)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)



# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from app.models import Customer

# # class UserRegistrationView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         username = request.data.get('username')
# #         password = request.data.get('password')

# #         if not username or not password:
# #             return Response({'error': 'Please provide both username and password'}, status=400)

# #         if User.objects.filter(username=username).exists():
# #             return Response({'error': 'Username already exists'}, status=400)

# #         user = User.objects.create_user(username=username, password=password)
# #         return Response({'message': 'User created successfully'}, status=201)



from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Product, Customer, Order,OrderItem
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        products = request.data.get('products', [])
        total_amount = sum(product['quantity'] * Product.objects.get(pk=product['product']).price for product in products)
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save(total_amount=total_amount)
        headers = self.get_success_headers(order_serializer.data)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
