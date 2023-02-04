from rest_framework import serializers
from .models import Department, Personnel
from django.utils import timezone


class DepartmentSerializer(serializers.ModelSerializer):
    personnel_count = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ("id", "name", "personnel_count")

    def get_personnel_count(self, obj):
        return obj.personals.count()

class PersonnelSerializer(serializers.ModelSerializer):
    create_user = serializers.StringRelatedField()
    create_user_id = serializers.IntegerField(required=False)
    days_since_joined = serializers.SerializerMethodField()
    class Meta:
        model = Personnel
        fields = ("id", "create_user", "create_user_id", "first_name", "last_name", "title", "gender", "salary", "department", "days_since_joined")

    # def create(self, validated_data):
    #     validated_data["create_user_id"] = self.context["request"].user.id
    #     personnel = Personnel.objects.create(**validated_data)
    #     personnel.save()
    #     return personnel
    
    def get_days_since_joined(self, obj):

        return (timezone.now() - obj.start_date).days


class DepartmentPersonnelSerializer(serializers.ModelSerializer):
    personnel_count = serializers.SerializerMethodField()
    personals = PersonnelSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = ("id", "name", "personnel_count", "personals")

    def get_personnel_count(self, obj):
        return obj.personals.count()