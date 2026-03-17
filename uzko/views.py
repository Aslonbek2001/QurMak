from .models import VocabModel
from .serializers import VocabularySerializer
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response


class VocabularySearchView(generics.ListAPIView):
    serializer_class = VocabularySerializer
    pagination_class = PageNumberPagination 
    

    def get_queryset(self):
        queryset = VocabModel.objects.all().order_by("id")
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(korean__icontains=search_query) |
                Q(uzb__icontains=search_query) |
                Q(krill__icontains=search_query)
            )
        return queryset
    
    @extend_schema(
        summary="Vocabulary list and search",
        description="Retrieve a list of all vocabulary or search the vocabulary model using Korean, Uzbek, or Krill terms.",
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Search term to filter results by Korean, Uzbek, or Krill text"
            ),
        ],
        responses=VocabularySerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({"message": "So'z topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)