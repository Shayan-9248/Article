from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import *
from .models import *


class ArticleListView(APIView):
    def get(self, request):
        article = Article.objects.filter(status='p')
        ser_data = ArticleSerializer(instance=article, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ArticleCreate(APIView):
    def post(self, request):
        ser_data = ArticleSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdate(APIView):
    def put(self, request, pk):
        article = Article.objects.get(pk=pk)
        ser_data = ArticleSerializer(instance=article, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDelete(APIView):
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(article.data, status=status.HTTP_204_NO_CONTENT)