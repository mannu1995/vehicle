from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate
from .models import Checkout,Vehicle
from .models import Vendor
from .forms import VehicleForm,QualityCheckForm
from django.http import JsonResponse
from .emails import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class LoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email = email,password=password)
                if user is None:
                    return Response({
                        'status':400,
                        'messages':'Invalid password',
                        'data': {},
                    })
                refresh = RefreshToken.for_user(user)

                return Response({
                
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })    


            return Response({
                'status':400,
                'messages':'Somthing went wrong!',
                'data': serializer.errors,
            })    
        except Exception as e:
            print(e)

class RegiserAPI(APIView):

    def  post(self,request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response({
                    'status':200 ,
                    'massage': 'registration successfully.',
                    'data': serializer.data,
                })
            return Response({
                'status': 400 ,
                'massage': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)  

# class VerifyOTP(APIView):
    def post(self,request):
        try:
            data = request.data 
            serializer = VerifyAccountSerializer(data=data)
            if serializer.is_vaild():
                email = serializer.data['email']
                otp = serializer.data['otp']
                
                user = User.objects.filter(email=email)

                if not user.exists():
                    return Response({
                'status': 400 ,
                'massage': 'something went wrong',
                'data': 'Invailed Email'
            })
                if user[0].otp != otp:
                    return Response({
                'status': 400 ,
                'massage': 'something went wrong',
                'data': 'Wrong Otp!'
            })
                
                user = user.first()
                user.is_verified = True
                user[0].save()        

                return Response({
                    'status':200 ,
                    'massage': 'account verified',
                    'data': {},
                })
            
            return Response({
                'status': 400 ,
                'massage': 'something went wrong',
                'data': serializer.errors
            })



        except Exception as e:
            print(e)    
            


def add_vehicle_api(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            
            # Retrieve vendor and product information based on P.O. number
            po_number = form.cleaned_data.get('purchase_order_number')
            vendor = Vendor.objects.filter(purchase_order_number=po_number).first()
            if vendor:
                vehicle.vendor = vendor
                vehicle.save()
                return JsonResponse({'message': 'Vehicle added successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Vendor not found for the provided P.O. number'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def conduct_quality_check_api(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    if request.method == 'POST':
        form = QualityCheckForm(request.POST)
        if form.is_valid():
            quality_check = form.save(commit=False)
            quality_check.vehicle = vehicle
            quality_check.save()
            return JsonResponse({'message': 'Quality check successfully conducted'}, status=201)
        else:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def initiate_checkout_api(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    if request.method == 'POST':
        checkout = Checkout.objects.create(vehicle=vehicle)
        checkout.save()
        return JsonResponse({'message': 'Checkout initiated successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_vehicle_details(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    serializer = VehicleSerializer(vehicle)
    return Response(serializer.data) 
@api_view(['GET'])
def get_vehicle_quality(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    serializer = QualityCheckSerializer(vehicle)
    return Response(serializer.data)
@api_view(['GET'])
def get_checout(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    serializer = CheckoutSerializer(vehicle)
    return Response(serializer.data)   