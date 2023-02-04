from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import TokenSerializer
from rest_framework.authtoken.models import Token
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password], required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, validators=[validate_password], required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', "password", "password2")

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"Password":"Password fields didnt match!"})
        return data
    
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        
class CustomTokenSerializer(TokenSerializer):

    user = UserTokenSerializer()
    class Meta(TokenSerializer.Meta):
        model = Token
        fields = ("user", 'key')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(required=False)
    class Meta:
        model = Profile
        fields = ('id', 'user', 'user_id',  'display_name', 'bio', "avatar")
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.user_id = self.context['request'].user.id
        # instance.save()
        return instance