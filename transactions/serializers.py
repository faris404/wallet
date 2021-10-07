
from rest_framework import serializers
from .models import Transactions

class POTSTransactionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Transactions
      fields = ['note','amount','person','mode','status']
     
class GETTransactionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Transactions
      fields = ['id','note','amount','person','mode','status']
     