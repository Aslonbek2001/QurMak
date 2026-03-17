from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import ClientModel
from .permissions import IsSelfOrSuperuser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from .serializers import ( 
    MessageSerializer, UserCreateSerializer, LoginSerializer, 
    ChangePasswordSerializer, UserProfileSerializer,
    TokenSerializer, LogoutSerializer, UserListSerializer, 
    ClientUpdateSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404

def create_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def logout_user(self, user):
        try:
            refresh_token = RefreshToken.for_user(user)
            refresh_token.blacklist()
        except AttributeError:
            pass 

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            devise = request.headers.get('devise')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.devise and user.devise != devise:
                    return Response({'message': 'Account faqat bitta qurilmada amal qiladi.'}, status=status.HTTP_401_UNAUTHORIZED)
                    # self.logout_user(user)
                
                current_time = timezone.now()
                if user.date_end and current_time > user.date_end:
                    return Response({'message': 'Sizga berilan 1 yillik mudat tugagan'}, status=status.HTTP_401_UNAUTHORIZED)

                if user.devise and user.devise == devise:
                    tokens = create_tokens_for_user(user) 
                    return Response(TokenSerializer(tokens).data, status=status.HTTP_200_OK)
            
                user.devise = devise
                user.save()
                tokens = create_tokens_for_user(user)
                return Response(TokenSerializer(tokens).data, status=status.HTTP_200_OK)

            return Response({"message": "Hisob maʼlumotlari yaroqsiz"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer

    def get_queryset(self):
            queryset = ClientModel.objects.all().order_by("id")
            search_query = self.request.GET.get('q', '')
            if search_query:
                queryset = queryset.filter(
                    Q(username__icontains=search_query) |
                    Q(phone__icontains=search_query) |
                    Q(date_start__icontains=search_query) |
                    Q(date_end__icontains=search_query)
                )

            ordering = self.request.GET.get('ordering', 'id')
            queryset = queryset.order_by(ordering)
            return queryset

    @extend_schema(
        summary="User list and search",
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
        responses=UserListSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({"message": "User topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'message': 'You are not SuperUser'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                data = {
                    'message': 'User registered successfully',
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'date_start': user.date_start,
                    'date_end': user.date_end,
                    'password': request.data.get("password")
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                error_message = str(e).lower()
                if 'unique constraint' in error_message:
                    return Response({'message': 'Foydalanuvchi allaqachon mavjud'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Foydalanuvchi yaratish jarayonida xatolik yuzaga keldi'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientUpdateSerializer
    permission_classes = [IsSelfOrSuperuser]

    def get_object(self):
        if self.request.user.is_superuser:
            return ClientModel.objects.get(id=self.kwargs['pk'])
        return self.request.user
        

class UserProfileView(APIView):
    serializer_class = UserProfileSerializer

    @extend_schema(
        responses=UserProfileSerializer,
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            response = {
                "username": user.username,
                "date_start": user.date_start,
                "date_end": user.date_end,
                "phone": user.phone
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        response = {
            "message": "Sizda hech qanday Profile mavjud emas! Admin bilan bog'laning"
        }
        return Response(data=response, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=ChangePasswordSerializer,
        responses= MessageSerializer
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                old_password = request.data.get("password")
                if user.check_password(old_password):
                    new_password = serializer.validated_data["new_password"]
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
            
                return Response({"message": "Eski parol noto'g'ri."},status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Siz Ro'yxatdan o'tmagansiz"}, status=status.HTTP_401_UNAUTHORIZED)

                

       
        
        

