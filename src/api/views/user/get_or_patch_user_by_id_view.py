from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.fields import CharField, ListField, IntegerField
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from api.models import Account
from api.serializers.factories import GetRequestFactory
from api.serializers.base_serializers.base_patch_serializer_conf import BasePatchSerializer
from api.serializers.role_serializers.mentor_serializers import OutputMentorSerializer
from api.serializers.role_serializers.user_serializers import OutputUserSerializer
from api.services.account_services import AccountService


class GetOrPatchUserView(APIView):
    class InputSerializer(BasePatchSerializer):
        login = CharField(source='username', required=False)
        password = CharField(required=False)
        mentored_users = ListField(child=IntegerField(), required=False)

        class Meta:
            model = Account
            fields = ['login', 'email', 'phone', 'role', 'password', 'mentored_users']
            ref_name = 'Patch user serializer'

        def update(self, instance, validated_data):
            result = AccountService.update(instance, validated_data)
            cache.delete(settings.ALL_USERS_CACHE)
            return result

    @swagger_auto_schema(responses={
        200: OutputMentorSerializer,
        2000: OutputUserSerializer,
        401: 'Unauthorized',
        404: 'Not found',
    }, tags=['user'],
    )
    def get(self, request, id: int):
        instance = get_object_or_404(Account, id=id)
        serializer_factory = GetRequestFactory.serializer(instance.role)
        serializer = serializer_factory(instance, context={'user_id': request.user.id, 'request_id': id})
        return Response(data=serializer.data, status=200)

    @swagger_auto_schema(request_body=InputSerializer, tags=['user'], responses={
        201: 'Success',
        401: 'Unauthorized',
        403: 'Not allowed',
        404: 'Not Found'
    })
    def patch(self, request, id: int):
        if request.user.id == id:
            instance = get_object_or_404(Account, id=id)
            input_serializer = self.InputSerializer(instance, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response(status=201)
        return Response(status=403)
