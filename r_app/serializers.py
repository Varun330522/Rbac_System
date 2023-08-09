from rest_framework import serializers
from .models import Users, API,ApiUserMapping
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = API
        fields = "__all__"

class APIMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUserMapping
        fields= "__all__"
