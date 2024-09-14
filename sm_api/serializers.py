from datetime import date

from rest_framework import serializers
from .models import Employee,User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("First Name must be at least 3 characters")
        return value

    def validate_last_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Last Name must be at least 3 characters")
        return value

    def validate_nic(self, value):
        if len(value) < 10 or len(value) > 12:
            raise serializers.ValidationError("Please enter a valid NIC address.")
        return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError("Please select a valid DOB.")
        return value

    def validate_img_url(self, value):
        if not value:
            raise serializers.ValidationError("At least one employee image must be added.")
        return value



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'img_url']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is not returned in responses
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash the new password on update
        instance.save()
        return instance