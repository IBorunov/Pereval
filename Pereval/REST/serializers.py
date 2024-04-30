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
    data = serializers.URLField()

    class Meta:
        model = Image
        fields = ['title', 'data']


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images', 'status']


    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.name != data_user['name'],
                instance_user.fam != data_user['fam'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'отклонено': 'у пользователя нельзя изменить данные'})
        return data