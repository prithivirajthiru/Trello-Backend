from rest_framework import serializers
from .models import User, Column, Card
from django.contrib.auth.models import AbstractUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #extra_kwargs = {'password': {'write_only': True}}
    def validate(self, data):
        # if data['name']:
        #     if User.objects.filter(username=data['name']).exists():
        #         raise serializers.ValidationError('name is taken')
        user_id = self.context['view'].kwargs.get('pk')  # Get user ID from URL kwargs

        if user_id:
            existing_user = User.objects.exclude(id=user_id).filter(mailId=data['mailId']).first()
            if existing_user:
                raise serializers.ValidationError('mailId is taken')    
        return data
        
    # def create(self, validated_data):
    #     user=User.objects.create(username=validated_data['username'],mailId=validated_data['mailId'])
    #     user.set_password(validated_data['password'])
    #     return validated_data
    
class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
       
    def validate(self, attrs):
        if  not attrs['title'].isalpha(): 
            raise serializers.ValidationError("Title should only contain alphabets.")
        if len(attrs['description'])>=25:
            raise serializers.ValidationError({"description length is minimum of 25 characters"})
        return attrs



class RegisterUserSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username is taken')

        if data['email']:
            if User.objects.filter(username=data['email']).exists():
                raise serializers.ValidationError('email is taken')    
        return data
    

class LoginSerializer(serializers.ModelSerializer):
    mailId=serializers.EmailField()
    password=serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'