from api.serializers.role_serializers.mentor_serializers import OutputMentorSerializer
from api.serializers.role_serializers.user_serializers import OutputUserSerializer


class GetRequestFactory:
    _map = {'user': OutputUserSerializer, 'mentor': OutputMentorSerializer}

    @classmethod
    def serializer(cls, role: str):
        serializer_class = cls._map.get(role)
        return serializer_class
