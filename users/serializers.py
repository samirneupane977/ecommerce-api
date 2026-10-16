from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs


    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user= User.objects.create_user(**validated_data)
        return user
        

    class Meta:
        model=User
        fields=['email','first_name','last_name','password','confirm_password']
    
       