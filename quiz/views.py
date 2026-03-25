from .models import QuizModel
from .serializers import QuizModelSerializer
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .permissions import IsActiveClient
import random

ONE, TWO, THREE, FOUR, FIVE = 1, 2, 3, 4, 5
limit_map = {
            ONE: 40,
            TWO: 40,
            THREE: 40,
            FOUR: 40,
            FIVE: 20,
        }

exam_map = {
            ONE: 7,
            TWO: 6,
            THREE: 5,
            FOUR: 4,
            FIVE: 3,
        }
level_list = [ONE, TWO, THREE, FOUR, FIVE]

@extend_schema(tags=['Marafon'])
class MarathonView(generics.ListAPIView):
    serializer_class = QuizModelSerializer
    queryset = QuizModel.objects.all().order_by("number")
    permission_classes = [IsActiveClient]


@extend_schema(tags=['Imtixon'])
class ExamView(generics.ListAPIView):
    permission_classes = [IsActiveClient]
    serializer_class = QuizModelSerializer
    def get_random_quizzes_by_level(self):
        exam = []
        for i in level_list:
            count = exam_map.get(i, 3)
            quizzes = QuizModel.objects.filter(level=i).order_by("number")
            if quizzes.count() > count:
                random_quizzes = random.sample(list(quizzes), count)
            else:
                random_quizzes = list(quizzes)
            
            exam.extend(random_quizzes)  

        random.shuffle(exam)  
        return exam
    
    def get(self, request, *args, **kwargs): 
        exam_quiz = self.get_random_quizzes_by_level()
        serializer = QuizModelSerializer(exam_quiz, many=True, context={'request': request})
        response_data = serializer.data  # serializer.data natijasini o‘qing
        response_data = {"time": 30, "data": response_data}  # qo'shimcha maydon bilan yangi javob formatini tuzing
        return Response(response_data)
      
    
class AllQuiz(generics.ListAPIView):
    serializer_class = QuizModelSerializer
    pagination_class = PageNumberPagination  

    def get_queryset(self):
        level = self.kwargs.get('level')
        current_time = timezone.now()
        devise = self.request.headers.get("devise")
        user = self.request.user

        if level not in level_list:
            return QuizModel.objects.none()

        limit = limit_map.get(level, 40)
        queryset = QuizModel.objects.filter(level=level).order_by('number')  # Tartiblash qo'shildi

        if user.is_authenticated:
            if user.is_superuser:
                self.message = None
                return queryset

            if current_time > user.date_end:
                self.message = f"Muddat tugagan."
                return queryset[:limit]
            
            if devise and devise != user.devise:
                self.message = "Bu account boshqa qurilmada ishlamoqda"
                return queryset[:limit]

            self.message = None
            
            return queryset
        
        self.message = None
        return queryset[:limit]

    @extend_schema(
        tags=["Level quizzes"],
        operation_id='level_quizzes',
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            
            if self.message:
                serializer["message"] = self.message

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if self.message:
            serializer["message"] = self.message
        
        return Response(serializer, status=status.HTTP_200_OK)
    
