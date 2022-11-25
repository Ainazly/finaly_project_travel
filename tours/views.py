from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .serializers import TourSerializer, CategorySerializer
from .models import Tour, Category
from rest_framework.permissions import AllowAny


# Для просмотра всех туров
class TourListView(ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [AllowAny]


# для детального просмотра
class TourDetailView(RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [AllowAny]


#
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]



