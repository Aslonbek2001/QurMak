from rest_framework import generics
from .models import UserLevelPage
from .serializers import UserLevelPageSerializer, ResponsePageSerializer
from rest_framework.response import Response
from rest_framework import status
from quiz.views import level_list, limit_map
from quiz.models import QuizModel
from drf_spectacular.utils import extend_schema
from django.db.models import Sum
from django.utils import timezone
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError


class UserLevelPageByLevelView(generics.ListCreateAPIView):
    serializer_class = UserLevelPageSerializer
    quizes_number_of_ticket = 20
    def get_quiz_count():
        try:
            return QuizModel.objects.count()
        except (OperationalError, ProgrammingError):
            return 0
        
    
    number_of_pages = get_quiz_count() / quizes_number_of_ticket

    def get_result_of_page(self, level, page):
        if limit_map.get(level) / self.quizes_number_of_ticket < page:
            return False
        return True
    
    def get_result_of_quiz(self, level, page, user):
        result_entry = UserLevelPage.objects.filter(level=level, page=page, user=user).only("result").first()
        if result_entry and result_entry.result is not None:
            return self.quizes_number_of_ticket - result_entry.result
        return None  
    
    def get_process(self, user):
        result_of_user = UserLevelPage.objects.filter(user=user).aggregate(Sum('result'))['result__sum'] or 0
        quiz_count = QuizModel.objects.count() or 1
        process = (result_of_user / quiz_count) * 100  
        return round(process, 2)

        
    def get_queryset(self):
        user = self.request.user
        return UserLevelPage.objects.filter(user=user).order_by("page")
    
    @extend_schema(
        tags=["extra"],
        operation_id="level_quizzes_info",
        responses=ResponsePageSerializer,
    )
    def get(self, request, *args, **kwargs):
        data = {}
        user = request.user
        devise = request.headers.get("devise")
        tickets_of_level_list = [] 

        if user.is_authenticated and timezone.now() < user.date_end and user.devise == devise:
            for level in level_list:
                level_quizes = QuizModel.objects.filter(level=level).count()
                pages, last_page = divmod(level_quizes, self.quizes_number_of_ticket)
                quizes = []  
                for page in range(1, pages + 1):
                    ticket = {
                        "page": page,
                        "count": self.quizes_number_of_ticket,
                        "free": True,
                        "incorrect": self.get_result_of_quiz(level=level, page=page, user=user)
                    }
                    quizes.append(ticket)

                # Last page if not a full page
                if last_page > 0:
                    ticket = {
                        "page": pages + 1,
                        "count": last_page,
                        "free": True,
                        "incorrect": self.get_result_of_quiz(level=level, page=pages + 1, user=user)
                    }
                    quizes.append(ticket)

                # Append ticket data for each level
                tickets_of_level_list.append({
                    "level": level,
                    "ticket": quizes
                })

            data = {
                "code": 1,
                "message": "success",
                "data": {
                    "process": self.get_process(user=user),
                    "list": tickets_of_level_list
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        
        for level in level_list:
            level_quizes = QuizModel.objects.filter(level=level).count()
            pages, last_page = divmod(level_quizes, self.quizes_number_of_ticket)
            quizes = []  
            for page in range(1, pages + 1):
                ticket = {
                    "page": page,
                    "count": self.quizes_number_of_ticket,
                    "free": self.get_result_of_page(level=level, page=page),
                    "incorrect": None
                }
                quizes.append(ticket)

            if last_page > 0:
                ticket = {
                    "page": pages + 1,
                    "count": last_page,
                    "free": self.get_result_of_page(level=level, page=(pages + 1)),
                    "incorrect": None
                }
                quizes.append(ticket)

            tickets_of_level_list.append({
                "level": level,
                "ticket": quizes
            })

        data = {
            "code": 1,
            "message": "success",
            "data": {
                "process": 0,
                "list": tickets_of_level_list
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        devise = request.headers.get("devise")
        if user.is_authenticated and timezone.now() < user.date_end and user.devise == devise:
            level = request.data.get('level')
            user = request.user
            page = request.data.get('page')
            result = request.data.get('result')

            instance, created = UserLevelPage.objects.update_or_create(
                user=user,
                level=level,
                page=page,
                defaults={'result': result}
            )

            if created:
                return Response({"message": "Natija Saqlandi", "results": UserLevelPageSerializer(instance).data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Natija o'zgartirildi", "results": UserLevelPageSerializer(instance).data}, status=status.HTTP_200_OK)

        return Response({"message": "Siz ro'yxatdan o'tmagansiz"}, status=status.HTTP_400_BAD_REQUEST)







