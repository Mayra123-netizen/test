from django.shortcuts import render
from rest_framework.views import APIView   
from django.http import HttpResponse
from rest_framework.response import Response  #importing response so as to use the get and post method in our code
from rest_framework import status
from . import serializers #making sure to import serializers from serializers.py
from . import models #making sure to import our models form models.py
from django.contrib.auth.hashers import make_password,check_password #importing these functions to help improve security of the passwords stored in our database by hashing them.
from datetime import datetime,timedelta
import jwt
from django.db.models import Q


#make your views logic


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
import jwt

def generatetoken(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=5),
        'iat': datetime.utcnow()
    }
    accesstoken = jwt.encode(payload, 'secret', algorithm='HS256')
    return accesstoken 

class Buyersignup(APIView):
    def post(self, request):
        serializer = serializers.BuyerSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')

            if models.Buyer.objects.filter(username=user_name).exists():
                return Response({'error': 'Username already exists'})
            else:
                serializer.save(password=make_password(pass_word))
                return Response({'message': 'User has signed up successfully'})
        else:
            return Response({'error': serializer.errors})

class Sellersignup(APIView):
    def post(self, request):
        serializer = serializers.SellerSerializer(data=request.data)

        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')
            
            if models.Seller.objects.filter(username=user_name).exists():
                return Response({'error': 'User already exists'})
            else:
                serializer.save(password=make_password(pass_word))
                return Response({'message': 'User signup successful'})
        else:
            return Response({'error': serializer.errors})

class Buyerlogin(APIView):
    def post(self, request):
        serializer = serializers.BuyerSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')
            
            try:
                buyer = models.Buyer.objects.get(username=user_name)
            except Exception as e:
                return Response({'error': str(e)})
            
            if check_password(pass_word, buyer.password):
                token = generatetoken(buyer)
                response = Response()
                response.set_cookie('access_token', value=token, httponly=True)
                response.data = {
                    'message': 'Buyer login successful',
                    'access_token': token
                }
                return response
            else:
                return Response({"message": "Invalid credentials"})
        else:
            return Response(serializer.errors)

			  
			   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   
	   

        

        

                         
class BuyerLogin(APIView):
    def post(self,request):
        serializer=serializers.BuyerSerializer(data=request.data)

        if serializer.is_valid(): 
            user_name=serializer.validated_data.get('username')
            pass_word=serializer.validated_data.get('password')
            try:
                 buyer=models.Buyer.objects.get(user_name=user_name)
            except Exception as e:
               return Response({'errors':str(e)})
            if check_password(pass_word,buyer.password):
               token = generatetoken(buyer)
               response=Response()
               response.set_cookie( 'access_token',value=token,httponly=True)
               response.data= {
                   'message':'Buyer login successful',
                   'access_token':token 
               }
               return response
            else:
                return Response({'error':'invalid credentials'})
        else:
            return Response({'error':'Login unsuccessful'})
        
        

class Sellerlogin(APIView):
    def post(self, request):
       
        serializer =serializers.SellerSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')
            
            try:
                seller = models.Seller.objects.get(username=user_name)
            except Exception as e:
                return Response({"error": str(e)})
            
            if check_password(pass_word, seller.password):
                token = generatetoken(seller)
                response = Response()
                response.set_cookie('access_token', value=token, httponly=True)
                response.data = {
                    'message': 'Seller login successful',
                    'access_token': token
                }
                return response
            else:
                return Response({"message": "Invalid credentials"})
        return Response({'errors':serializer.errors})
    

class Uploaditem(APIView):
    def post(self,request):
        #extracting our token
        token= request.COOKIES.get('access_token')
        if not token:
            return Response({'error':'aunthenticated'})
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except Exception as e:
            return Response({'error':str(e)})
        

        serializer=serializers.ItemSerializer(data=request.data)
        if serializer.is_valid():
               item_name=serializer.validated_data.get('itemname')
               seller=models.Seller.objects.get(id=payload['user_id'])
               serializer.save(itemproducer=seller,itemname=item_name)
               return Response({'message':'Item has been uploaded succesfully','data':serializer.data})
        else:
               return Response({'error':serializer.errors})
        
