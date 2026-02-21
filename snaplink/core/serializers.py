from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ShortURL,ClickAnalytics

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ShortURLSerializer(serializers.ModelSerializer):
    short_url= serializers.SerializerMethodField()

    class Meta:
        model=ShortURL
        fields=['id','original_url','short_code','short_url','created_at']
        read_only_fields=['short_code','short_url']

    def get_short_url(self,obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_code}/')
        return f'/{obj.short_code}/'
