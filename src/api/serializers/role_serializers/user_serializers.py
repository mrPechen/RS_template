from rest_framework.serializers import ReadOnlyField

from api.models import Account
from api.serializers.base_serializers.base_get_serializer_conf import BaseGetSerializer


class OutputUserSerializer(BaseGetSerializer):
    login = ReadOnlyField(source='username')
    mentor = ReadOnlyField(source='user.mentor.account.username')
    password = ReadOnlyField(source='get_decode_password')

    class Meta:
        model = Account
        fields = ['id', 'login', 'email',
                  'phone', 'role', 'mentor', 'password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        mentor = representation.get('mentor', None)
        if mentor is None:
            representation.pop('mentor', None)

        return representation
