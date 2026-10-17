from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, TokenResponseSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RegisterView(APIView):
    @extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterSerializer},
)
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(
             serializer.errors,
             status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @extend_schema(
    request=LoginSerializer,
    responses={200: TokenResponseSerializer},
)
    def post(self,request):
        serializer=LoginSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        tokens=serializer.get_token_for_user(user)
        return Response(tokens,status=status.HTTP_200_OK)

class MeView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": request.user.role,
        })
    

     



