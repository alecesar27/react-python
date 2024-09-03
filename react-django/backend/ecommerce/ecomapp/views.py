from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
# from .products import products
from .models import Products, Orders,Address
from .serializer import ProductsSerializer, OrdersSerializer,AddressSerializer, UserSerializer,UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# for sending mails and generate token
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


import threading


class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message= email_message
        threading.Thread.__init__(self)
   
    def run(self):
        self.email_message.send()


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    return Response('Hello Alex')


class ProductView(APIView):

    @api_view(['GET'])
    def getProducts(request):
        products=Products.objects.all()
        serializer=ProductsSerializer(products,many=True)
        return Response(serializer.data)


    @api_view(['GET'])
    def getProduct(request,pk):
        product=Products.objects.get(_id=pk)
        serializer=ProductsSerializer(product,many=False)
        return Response(serializer.data)

    @api_view(['PUT'])
    def updateProduct(request, pk):
        product = Products.objects.get(_id=pk)
        serializer = ProductsSerializer(product, data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

        

class OrderView(APIView):

    @api_view(['POST'])
    def createOrder(request):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        

    @api_view(['GET'])
    def getOrderProduct(request,id):
        orders=Orders.objects.filter(id_prod=id)      
        serializer=OrdersSerializer(orders,many=True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def openedOrderClient(request,id):
        orders=Orders.objects.filter(user=id,status=True)      
        serializer=OrdersSerializer(orders,many=True)
        return Response(serializer.data)
    

    @api_view(['GET'])
    def getOrders(request):
        orders=Orders.objects.all()
        serializer=OrdersSerializer(orders,many=True)
        return Response(serializer.data)
    
    @api_view(['PUT'])
    def updateOrder(request, pk):
        order = Orders.objects.get(_id=pk)
        serializer = OrdersSerializer(order, data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)    




class AddressView(APIView):

    
    @api_view(['POST'])
    def createAddress(request):
        
        print(request.data)
        
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @api_view(['GET'])
    def clientAddress(request,id):
        address=Address.objects.filter(user=id)      
        serializer=AddressSerializer(address,many=True)
        return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v       
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  getUserProfiles(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data=request.data
    try:
        user= User.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['email'],email=data['email'],password=make_password(data['password']),is_active=False)
      
        # generate token for sending mail
        email_subject="Activate Your Account"
        message=render_to_string(
            "activate.html",
           {
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
           }

        )
        print(message)
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[data['email']])
        EmailThread(email_message).start()     
 
        message={'details':'Activate your account please check the link in email for account activation'}
        return Response(message)
    
    except Exception as e:
        message={'details':'User with this email already exists or something went wrong'}
        
        return Response(message)



class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,"activatesuccess.html")
        else:
            return render(request,"activatefail.html")  