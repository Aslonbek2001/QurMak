from django.shortcuts import render
from .models import BookTwo, BookOne
from .serializers import BookOneSerializer, BookTwoSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from quiz.permissions import IsActiveClient

# class CustomPagination(PageNumberPagination):
#     page_size = 10 
#     page_size_query_param = 'page_size'
#     max_page_size = 30

class BookOneView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookOneSerializer
    pagination_class = None
    queryset = BookOne.objects.all().order_by("number")

class BookTwoView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookTwoSerializer
    pagination_class = None
    queryset = BookTwo.objects.all().order_by("number")



