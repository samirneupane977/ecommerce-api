from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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

class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        email= attrs.get('email')
        password= attrs.get('password')

        user = authenticate(
        request=self.context.get("request"),
        email=email,
        password=password,)
        
        if not user:
            raise serializers.ValidationError(
            {"detail": "Invalid email or password."}
        )
        if not user.is_active:
            raise serializers.ValidationError(
            {"detail": "This account is inactive."}
        )
        
        attrs["user"] = user
        return attrs
    
    def get_token_for_user(self,user):
        refresh=RefreshToken.for_user(user)

        return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

       