from rest_framework import serializers
from .models import Tour, Category, Types, Comment


class TourSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")
    types = serializers.CharField(source="types.title")

    class Meta:
        model = Tour
        fields = "__all__"

        def get(self, request, format=None):
            serializer = TourSerializer(Tour.objects.all(), many=True)


class CategorySerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField()

    def get_tours(self, obj):
        return TourSerializer(obj.tours.all(), many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'tours')


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = "__all__"








