from .models import User, PerevalAdded, Level, Coord, Image
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin
from rest_framework import serializers


class UserSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fam', 'name', 'otc', 'phone']

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        return user


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    level = LevelSerializer()
    image = ImageSerializer(many=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PerevalAdded
        fields = ['id', 'beautyTitle', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'image', 'status']
