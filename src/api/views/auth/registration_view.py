import re

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.views import APIView

from api.models import Account


class RegistrationView(APIView):
    class InputSerializer(ModelSerializer):
        email = EmailField(required=False)
        phone = CharField(required=False)

        class Meta:
            model = Account
            fields = ['username', 'password', 'email', 'phone']

        def validate_phone(self, value):
            pattern = re.compile(r'^7\d{10}$')
            if not pattern.match(value):
                raise ValidationError('Phone number must be in the format 7XXXXXXXXXX')
            return value

        def create(self, validated_data):
            user = Account.objects.create_user(**validated_data)
            user.set_encrypted_password(validated_data['password'])
            return user

    def post(self, request):
        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
