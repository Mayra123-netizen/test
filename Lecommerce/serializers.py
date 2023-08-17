from rest_framework import serializers
from . import models

#creating my serializers
class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
     model= models.Buyer
     fields = ('id','username','password')
     read_only_fields=('id',)
     
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
     model=models.Seller
     fields = ('id','username','password')
     read_only_fields=('id',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Item
        fields = (
            'id',
            'description',
            'itemname',  
        )
        read_only_fields=('id',)