from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

#Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email is already registered.Please try another")],
        error_messages={'blank': 'The email field is required.', 'required': 'The email field is required.'}
    ) 

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message="This username is already taken. Please choose another."),
            RegexValidator(regex=r'^[a-zA-Z0-9]+$',
            message='The username can only contain letters and numbers (no dots or hyphens).')
        ],
        error_messages={'blank': 'The username field cannot be empty.', 'required': 'The username field is required.'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


##Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={'blank': 'The email field is required.', 'required': 'The email field is required.'}
    )
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'},
        error_messages={'blank': 'The password field cannot be empty.', 'required': 'The password field is required.'}
    )

    def validate_email(self, value):
        """
        Check if the email exists in the database.
        """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value
