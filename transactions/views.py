
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from users.models import User,Person
from users.serializers import POTSPersonSerializer
from .models import Transactions
from .serializers import POTSTransactionSerializer


class TransactionView(APIView):

   permission_classes = [IsAuthenticated] 

   def post(self,request):
      try:
         serializer = POTSTransactionSerializer(data=request.data)
         if serializer.is_valid():
            data = serializer.data
            person = Person.objects.get(pk=data['person'])
            data['person'] = person
            print(person)
            print(serializer.data)
            if not person:
               return JsonResponse({'message':'Person not found'})
            tran = Transactions(**data,user=request.user)
            tran.save()
            return JsonResponse({'message':"success"})
         return JsonResponse({'message':"invalid data",'errors':serializer.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def get(self,request):
      try:
         to_give = Transactions.objects.filter(user_id=request.user,mode=1,status=False).aggregate(Sum('amount'))
         to_recive = Transactions.objects.filter(user_id=request.user,mode=0,status=False).aggregate(Sum('amount'))
         data = {
            'to_give':to_give['amount__sum'],
            'to_receive':to_recive['amount__sum']
         }
         print(to_give)
         return JsonResponse({'message':'success','data':data})
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonTransactionView(APIView):

   permission_classes = [IsAuthenticated] 
   def get(self,request,person_id):
      try:
         paid_status = request.GET.get('status', False)

         person = Person.objects.get(pk=person_id) #  get person details
         data = Transactions.objects.filter(user_id=request.user,person_id=person,status=paid_status) #  get transaction details
         data = POTSTransactionSerializer(data,many=True).data
         person = POTSPersonSerializer(person).data
         to_give = 0
         to_recieve = 0
         for i in data:
            if i['mode']==1:
               to_give+=i['amount']
            else:
               to_recieve+=i['amount']
         resp = {
            'message':'success',
            'person':person,
            'to_recieve':to_recieve,
            'to_give':to_give,
            'transactions':data
         }
         return JsonResponse(resp)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TransactionStatusView(APIView):

   permission_classes = [IsAuthenticated] 
   def put(self,request,tran_id):
      try:
         transaction = Transactions.objects.get(pk=tran_id) #  get transaction details
         if not transaction:
            return JsonResponse({'message':'Transaction not found'})
         transaction.status = not transaction.status
         transaction.save()
         return JsonResponse({'message':'Success'})
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


