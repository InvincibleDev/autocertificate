from rest_framework import serializers
from certificate.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password','username', 'email')
        extra_kwargs={'password':{'write_only':True}}

    validate_password = make_password

class TemplateBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blanks
        fields = ('id', 'blank_no', 'start', 'end')
        depth = 1

class TemplateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    blanks = TemplateBlankSerializer(many=True)
    class Meta:
        model = Templates
        fields = ('id', 'template','title', 'user', 'blanks')
        depth = 1

class CsvSerializer(serializers.Serializer):
    headers = serializers.ListField()

class LinkSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Link
        fields = ('id','user','link','template_title')
        depth=1
