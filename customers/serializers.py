from rest_framework import serializers
from .models import Customer
import re
from rest_framework.validators import UniqueValidator

#Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Customer.objects.all(), message="This email is already registered.Please try another")],
        error_messages={'blank': 'The email field is required.', 'required': 'The email field is required.'}
    )
    
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_mobile(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value
