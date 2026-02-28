from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'address', 'gender',
            'bio', 'profile_picture', 'date_joined', 'tailor_type',
            'is_active', 'is_staff', 'is_approved', 'is_superuser'
        ]
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    is_tailor = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            'email', 'full_name', 'phone', 'address', 'gender',
            'password', 'password2', 'is_tailor', 'tailor_type'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Neno la siri hazilingani'})
        if data.get('is_tailor') and not data.get('tailor_type'):
            raise serializers.ValidationError({'tailor_type': 'Tafadhali chagua aina ya nguo unazoshona'})
        return data

    def create(self, validated_data):
        is_tailor = validated_data.pop('is_tailor', False)
        validated_data.pop('password2')
        password = validated_data.pop('password')
        tailor_type = validated_data.pop('tailor_type', None)

        user = User(**validated_data)
        user.set_password(password)

        if is_tailor:
            user.is_staff = True
            user.is_approved = False
            user.tailor_type = tailor_type
        else:
            user.is_staff = False
            user.is_approved = True
            user.tailor_type = None

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
