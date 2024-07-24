from django.http import JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from .models import Pereval
from .serializers import PerevalSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ['user__email']

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': None,
                'id': serializer.data['id'],
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
            'id': None,
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'new':

            data = request.data.copy()
            data.pop('user', None)

            serializer = self.get_serializer(pereval, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': 1,
                    'message': 'Запись успешно изменена'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'state': 0,
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'state': 0,
                'message': f"Отклонено. Причина: {pereval.get_status_display()}"
            }, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        return Response({
            'state': 0,
            'message': 'Используйте метод partial_update для частичных обновлений'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        return Response({
            'state': 0,
            'message': 'Удаление не разрешено'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
