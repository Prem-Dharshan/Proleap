from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


from .models import (User, Batch, UserBatch, Status)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class BatchSerializer(serializers.ModelSerializer):
    # users = UserSerializer(many=True, read_only=True, source='users_set')
    class Meta:
        model = Batch
        fields = '__all__'


class UserBatchSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    batch_id = serializers.IntegerField()

    class Meta:
        model = UserBatch
        fields = ['id', 'user_id', 'batch_id', 'completed_activities', 'is_completed', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        batch_id = validated_data.pop('batch_id')

        try:
            user_batch, created = UserBatch.objects.update_or_create(
                user_id=user_id,
                batch_id=batch_id,
                defaults={
                    'completed_activities': validated_data.get('completed_activities', 0),
                    'is_completed': validated_data.get('is_completed', False),
                    'status': validated_data.get('status', Status.NOT_ATTEMPTED)
                }
            )
            return user_batch
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
    def update(self, instance, validated_data):
        # Exclude user_id and batch_id from validated_data to keep them immutable
        validated_data.pop('user_id', None)
        validated_data.pop('batch_id', None)

        instance.completed_activities = validated_data.get('completed_activities', instance.completed_activities)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.status = validated_data.get('status', instance.status)

        try:
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(str(e))