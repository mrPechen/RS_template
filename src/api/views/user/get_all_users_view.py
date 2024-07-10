from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.conf import settings
from api.models import Account


class GetUsersView(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(ModelSerializer):
        account_id = ReadOnlyField(source='id')
        login = ReadOnlyField(source='username')
        mentor_id = ReadOnlyField(source='user.mentor.id')

        class Meta:
            model = Account
            fields = ['account_id', 'login', 'mentor_id']
            ref_name = 'Output all users serializer'

    @swagger_auto_schema(responses={
        200: OutputSerializer,
        401: 'Unauthorized',
    }, tags=['user'],
    )
    def get(self, request):
        caches = cache.get(settings.ALL_USERS_CACHE)
        if caches:
            return Response(data=caches, status=201)
        instance = Account.objects.all()
        serializer = self.OutputSerializer(instance, many=True)
        cache.set(settings.ALL_USERS_CACHE, serializer.data)
        return Response(data=serializer.data, status=200)
