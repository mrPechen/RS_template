from django.shortcuts import get_object_or_404
from rest_framework.fields import CharField, ListField, IntegerField
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Account
from api.serializers.factories import GetRequestFactory
from api.serializers.base_serializers.base_patch_serializer_conf import BasePatchSerializer
from api.services.account_services import AccountService


class GetOrPatchUserView(APIView):
    class InputSerializer(BasePatchSerializer):
        login = CharField(source='username', required=False)
        password = CharField(required=False)
        mentored_users = ListField(child=IntegerField(), required=False)

        class Meta:
            model = Account
            fields = ['login', 'email', 'phone', 'role', 'password', 'mentored_users']

        def update(self, instance, validated_data):
            result = AccountService.update(instance, validated_data)
            return result

    def get(self, request, id: int):
        instance = get_object_or_404(Account, id=id)
        serializer_factory = GetRequestFactory.serializer(instance.role)
        serializer = serializer_factory(instance, context={'user_id': request.user.id, 'request_id': id})
        return Response(data=serializer.data, status=200)

    def patch(self, request, id: int):
        if request.user.id == id:
            instance = get_object_or_404(Account, id=id)
            input_serializer = self.InputSerializer(instance, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response(status=201)
        return Response(status=403)
