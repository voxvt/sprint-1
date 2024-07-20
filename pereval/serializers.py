from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'fam', 'name', 'pat', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'spring', 'summer', 'autumn']


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Images
        fields = ['image', 'title']


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coord_id = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField()

    class Meta:
        model = Pereval
        depth = 1
        fields = (
            'id',
            'status',
            'beauty_title',
            'title',
            'other_titles',
            'add_time',
            'user',
            'connect',
            'coord_id',
            'level',
            'images'
        )

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coord_id = validated_data.pop('coord_id')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = Users.object.get_or_create(**user)

        coord_id = Coords.objects.create(**coord_id)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coord_id=coord_id, level=level, status="NW")

        for image in images:
            data = image.pop('data')
            image = image.pop('image')
            title = image.pop('title')
            Images.objects.create(data=data, image=image, pereval=pereval, title=title)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.patronymic != data_user['pat'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],

            ]

            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Отклонено': 'Нельзя изменять данные пользователя'})
        return data
