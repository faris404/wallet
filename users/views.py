
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import POTSUserSerializer,POTSPersonSerializer
from .models import User,Person


# user signup
class UserSignup(APIView):
   authentication_classes = []
   permission_classes = [] 

   #  signup a user

   def post(self,request):
      try:

         serializer = POTSUserSerializer(data=request.data)
         
         if serializer.is_valid():
            password = serializer.data.pop('password')
            user = User(
               **serializer.data
            )
            user.set_password(password)
            user.save()
            print(user)
            refresh = RefreshToken.for_user(user)
            
            return JsonResponse({"message": "Success",'refresh':str(refresh),'access': str(refresh.access_token),})
         print(serializer.errors.values())
         return JsonResponse({"detail": "Invalid Data",'error':serializer.errors})
         
      except Exception as e:
         print(e)
         return JsonResponse({"detail": "Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Test(APIView):
   permission_classes = [IsAuthenticated] 

   def get(self,request):
      print(request.user.first_name)
      return JsonResponse({'msg':'hello'})


class PearsonView(APIView):
   # authentication_classes = []
   permission_classes = [IsAuthenticated] 
   def post(self,request):
      try:

         serializer = POTSPersonSerializer(data=request.data)
         if serializer.is_valid():
            person = Person(**serializer.data,user_id=request.user)
            person.save()
            return JsonResponse({'message':"success"})
         return JsonResponse({'message':"invalid data",'errors':serializers.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def get(self,request):
      try:
         persons = Person.objects.filter(user_id=request.user.id)
         serializer = POTSPersonSerializer(persons,many=True).data
         print(serializer)
         return JsonResponse({'message':"success",'data':serializer},status=status.HTTP_200_OK)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)