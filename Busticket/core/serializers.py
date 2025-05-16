from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Profile, Bus, Schedule, Booking

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['user', 'profile_image', 'mobile', 'birthdate', 'gender', 'address', 'pincode', 'state']

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            role = validated_data['role']

        )
        profile = Profile.objects.create(user=user)

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'bus', 'schedule', 'seat_numbers', 'total_amount', 'booking_time']
        read_only_fields = ['passenger', 'total_amount', 'booking_time']

