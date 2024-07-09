import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api.models import Account


class BasePatchSerializer(ModelSerializer):

    def validate_phone(self, value):
        pattern = re.compile(r'^7\d{10}$')
        if not pattern.match(value):
            raise ValidationError('Phone number must be in the format 7XXXXXXXXXX')
        return value

    def validate_password(self, value):
        pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$')
        if not pattern.match(value):
            raise ValidationError(
                'Password must be len > 6, contain at least one digit, one lowercase letter, and one uppercase letter.'
            )
        return value

    def validate_login(self, value):
        check_login = Account.objects.filter(username=value).exists()
        if check_login:
            raise ValidationError('This username is already taken.')
        return value
