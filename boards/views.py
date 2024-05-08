from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets

from core.paginations import CustomPagination
from boards.serializers import boardsSerializers
from boards.models import Board


class boardsViewsets(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = boardsSerializers
    pagination_class = CustomPagination

    @swagger_auto_schema(tags=["게시물"])
    def create(self, request, *args, **kwargs):
        """
        게시물 생성
        ---
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["게시물"])
    def list(self, request, *args, **kwargs):
        """
        게시물 목록
        ---
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["게시물"])
    def retrieve(self, request, *args, **kwargs):
        """
        게시물 상세 보기
        ---
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["게시물"])
    def update(self, request, *args, **kwargs):
        """
        게시물 부분 수정
        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["게시물"])
    def partial_update(self, request, *args, **kwargs):
        """
        게시물 전체 수정
        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["게시물"])
    def destroy(self, request, *args, **kwargs):
        """
        게시물 삭제
        ---
        """
        return super().destroy(request, *args, **kwargs)
