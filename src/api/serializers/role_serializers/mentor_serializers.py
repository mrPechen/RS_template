from rest_framework.serializers import ReadOnlyField, RelatedField

from api.models import Account
from api.serializers.base_serializers.base_get_serializer_conf import BaseGetSerializer


class OutputMentorSerializer(BaseGetSerializer):
    class RepresentationMentoredUsersField(RelatedField):
        def to_representation(self, value):
            return value.account.username

    login = ReadOnlyField(source='username')
    password = ReadOnlyField(source='get_decode_password')
    mentored_users = RepresentationMentoredUsersField(many=True, read_only=True, source='mentor.mentored_users')

    class Meta:
        model = Account
        fields = ['id', 'login', 'email',
                  'phone', 'role', 'password', 'mentored_users']
