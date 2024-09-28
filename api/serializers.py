from rest_framework import serializers
from .models import User,Tasks


class AuthSerializer(serializers.Serializer):
    phone_number=serializers.IntegerField()
    password=serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    task_count=serializers.SerializerMethodField()

    def get_task_count(self,obj):
        
        task=Tasks.objects.filter(user=obj)
        return task.count()
    class Meta:
        model=User
        fields=["first_name","last_name","phone_number","last_login","is_staff","task_count"]


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        read_only_fields=['created_at','updated_at','user']
        fields='__all__'