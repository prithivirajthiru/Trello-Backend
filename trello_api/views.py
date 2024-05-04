import json
from rest_framework import generics,status
from .models import User, Column, Card
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from django.contrib.auth import authenticate, login,logout
from .models import User
from .serializers import *
from rest_framework.authtoken.models import Token
###DataUser
class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')  # Retrieve user ID from URL kwargs
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({"message": "delete successful"},status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    def get(self,request,*args, **kwargs):
        user = User.objects.all()
        serializer=UserSerializer(user,many=True)
        return Response({'data':serializer.data,'status':True,
                'message':'successful'},status.HTTP_201_CREATED)

class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   
###DataColumn
class ColumnCreate(generics.ListCreateAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    
    def delete(self, request, *args, **kwargs):
        column_id = kwargs.get('pk')  # Retrieve user ID from URL kwargs
        try: 
            column = Column.objects.get(pk=column_id)
            column.delete()
            return Response({"message": "delete successful"},status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ColumnUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer  

###DataCard
class CardCreate(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    def delete(self, request, *args, **kwargs):
        column_id = kwargs.get('pk')  # Retrieve user ID from URL kwargs
        try:
            column = Column.objects.get(pk=column_id)
            column.delete()
            return Response({"message": "delete successful"},status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
class CardUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer 


##Login
# class LoginApi(APIView):

#     def post(self,request):
#         data=request.data
#         serializer=LoginSerializer(data=data)
#         if not serializer.is_valid():
#             return Response({
#                 'status':False,
#                 'message':serializer.errors,
#                 },status.HTTP_401_UNAUTHORIZED)
#         user =authenticate(mailId=serializer.data['mailId'],password=serializer.data['password'])
#         print(user,serializer.data['mailId'],serializer.data['password'])
#         if not user :
#            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         token,_=Token.objects.get_or_create(user=user)
#         return Response({'data':serializer.data,'status':True,
#                 'message':'user created'},status.HTTP_201_CREATED)
    

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('mailId')
        password = request.data.get('password')      
        try:
            user = User.objects.get(mailId=email)
            if user.password==password:
               serializer=UserSerializer(user)
               return Response({'data':serializer.data,'detail': 'Login successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:   
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                             
@api_view(['GET'])
def getCardBasedOnColumn(self,id):
   
    try:                          
        cards = Card.objects.filter(column=id)  
        serializer=CardSerializer(cards,many=True)         
    except Exception as e:
        print(f"Error occurred: {e}")
        
    return Response({'data':serializer.data,'status':True,})


@api_view(['GET'])
def getColumnWithCardBasedOnUser(self,id):
    column_cards_dict = {}
    try:        
        columns = Column.objects.filter(userId=id)
        #print("-----------------",len(columns))      
        for column in columns:            
            cards = Card.objects.filter(column=column.id)
            card_list = [{'title': card.title, 'description': card.description} for card in cards]
            column_cards_dict[column.title] = card_list
    except Exception as e:
        print(f"Error occurred: {e}")
        column_cards_dict = {}
    return Response({'data':column_cards_dict},status=status.HTTP_200_OK)

@api_view(['PUT'])
def reorder_cards_in_column(request, column_id):
    try:
        column = Column.objects.get(id=column_id)                
        ordered_card_ids = request.data.get('card_ids', [])
        existing_card_ids = list(column.cards.values_list('id', flat=True))
        if not set(ordered_card_ids).issubset(existing_card_ids):
            return Response({'error': 'Invalid card IDs provided'}, status=status.HTTP_400_BAD_REQUEST)      
        for index, card_id in enumerate(ordered_card_ids):
            card = Card.objects.get(id=card_id)
            card.order = index  
            card.save()
        return Response({'message': 'Cards reordered successfully'}, status=status.HTTP_200_OK)
    except Column.DoesNotExist:
        return Response({'error': 'Column not found'}, status=status.HTTP_404_NOT_FOUND)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
