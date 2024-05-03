from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class user_serializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name']