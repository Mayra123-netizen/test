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




def generatetoken(user,user_type):
    payload = {
        'user_id': user.id,
        'user_type':user_type,
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
                token = generatetoken(buyer,'buyer')
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
                token = generatetoken(seller,'seller')
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
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({'message': 'unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('user_id')
            user_type = payload.get('user_type')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            seller = models.Seller.objects.get(id=user_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if user_type == 'seller':
            serializer = serializers.ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(itemproducer=seller)
                return Response({"message": "Item created successfully", "data": serializer.data})
            else:
                return Response({"error": serializer.errors})
        else:
            return Response({"error": "Only Sellers can create item posts"}, status=status.HTTP_403_FORBIDDEN)


class Viewitem(APIView):
    def get(self, request):
        token=request.COOKIES.get('access_token')
        
        # Extract the token from the request's cookies
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message': 'unauthenticated'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            return Response({'error': str(e)})

        # Get all posts
        posts = models.Item.objects.all()

        # Serialize the posts data using the serializer
        serializer = serializers.ItemSerializer(posts, many=True)
        return Response({'message': serializer.data})
    
class Searchitem(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')
        
        # Extract the token from the request's cookies
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message': 'unauthenticated'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            return Response({'error': str(e)})

        try:
            logged_user = models.Item.objects.get(id=payload['user_id'])
        except Exception as e:
            return Response({'error': str(e)})

        # Search query code to search for items
        search_query = request.query_params.get('search')
        item = models.Item.objects.filter(Q(description__icontains=search_query))
        item2 = models.Item.objects.filter(Q(itemname__icontains=search_query))
        item3 = models.Item.objects.filter(Q(itemproducer__username__icontains=search_query))

        Theitems = item | item2 | item3

        if Theitems:
            items_toshow = serializers.ItemSerializer(Theitems, many=True)
            return Response({'data': items_toshow.data})
        return Response({'Message': 'Nothing found'})

        


class Deleteitem(APIView):
    def delete(self, request):
        # Extract the token from the request's cookies
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['user_id']
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the user is a seller
        try:
            seller = models.Seller.objects.get(id=user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        post_id = request.query_params.get('post_id')
        try:
            post = models.Item.objects.get(id=post_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        if post.itemproducer != seller:
            return Response({'error': 'You are not the owner of this item'}, status=status.HTTP_403_FORBIDDEN)

        try:
            post.delete()
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Updateitem(APIView):
    def put(self,request):
        token = request.COOKIES.get('access_token')
        
        # Extract the token from the request's cookies
        if not token:
            return Response({'message': 'unauthenticated'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            logged_user = models.Seller.objects.get(id=payload['user_id'])
        except Exception as e:
            return Response({'error': str(e)})

        post_id = request.query_params.get('post_id')
        try:
            post = models.Item.objects.get(id=post_id)
        except Exception as e:
            return Response({"error": str(e)})

        # Check if the requesting user is the owner of the post
        if post.itemproducer != logged_user:
            return Response({"error": "You are not the owner of this post"})

        serializer = serializers.ItemSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated successfully", "data": serializer.data})
        else:
            return Response({"error": serializer.errors})
            

	   
	   

class Logout(APIView):
    def delete(self,request):
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
           

        # Clear the access token cookie
        response = Response({'message': 'Successfully logged out'})
        response.delete_cookie('access_token')

        return response
    
